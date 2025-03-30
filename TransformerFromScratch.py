import torch
import torch.nn as nn
from torch.nn import functional as F

torch.manual_seed(1337)
cores = 6
heads = 6
head_sze = 20
total_chr = 1
embedding_size = 120
context = 64
inf = 1e12
p = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'


# I will build a single head of attention

class Head(nn.Module):
    def __init__(self, head_sze):
        super().__init__()
        self.key = nn.Linear(embedding_size, head_sze, bias=False)  # projecting embedding to head size
        self.query = nn.Linear(embedding_size, head_sze, bias=False)  # projecting embedding to head size
        self.value = nn.Linear(embedding_size, head_sze, bias=False)  # projecting embedding to head size
        self.register_buffer('tril', torch.tril(torch.ones(context, context)))
        self.dropout = nn.Dropout(p)

    def forward(self, num):
        B, T, C = num.shape  # B:batches T:number of characters C:channels(every character of every batch has an embedding table)

        keys = self.key(num)  # is what i have (B,T,head_sze)
        queries = self.query(num)  # is what i need (B,T,head_sze)
        values = self.value(num)  # is what i get (B,T,head_sze)

        tmp = queries @ keys.transpose(-2, -1) * keys.shape[-1] ** -0.5

        tmp = tmp.masked_fill(self.trill[:T, :T] == 0, float(-inf))

        tmp = F.softmax(tmp, dim=-1)

        tmp = self.dropout(tmp)

        out = tmp @ values

        return out


# now I will produce multiple heads of attention

class Multiple_Heads_of_Attention(nn.Module):
    def __init__(self, heads, head_sze):
        super().__init__()
        self.list_of_heads = nn.ModuleList(Head(head_sze) for _ in range(heads))
        self.proj = nn.Linear(head_sze * heads, embedding_size)
        self.dropout = nn.Dropout(p)

    def forward(self, num):
        ans = torch.cat([hd(num) for hd in self.list_of_heads])
        ans = self.dropout(self.proj(ans))
        return ans


# now linearity with non-linearity(RELU) Feed Forward

class FF(nn.Module):
    def __init__(self, embedding_size):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(embedding_size, 4 * embedding_size),
            nn.ReLU(),
            nn.Linear(4 * embedding_size, embedding_size),
            nn.Dropout(p),
        )

    def forward(self, num):
        return self.network(num)


class Core(nn.Module):
    def __init__(self, embedding_size, heads):
        super().__init__()
        self.mha = Multiple_Heads_of_Attention(heads, embedding_size // heads)
        self.ff = FF(embedding_size)
        self.ln1 = nn.LayerNorm(embedding_size)
        self.ln2 = nn.LayerNorm(embedding_size)

    def forward(self, num):
        num = num + self.mha(self.ln1(num))  # residual connection
        num = num + self.ff(self.ln2(num))  # residual connection
        return num


class Transformer(nn.Module):
    def __init__(self):
        super().__init__()

        self.chr_emb = nn.Embedding(total_chr, embedding_size)
        self.pos_emb = nn.Embedding(context, embedding_size)
        self.cores = nn.Sequential(*[Core(embedding_size, heads) for _ in range(cores)])
        self.final_ln = nn.LayerNorm(embedding_size)
        self.final_proj = nn.Linear(embedding_size, total_chr)

        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, index, t=None):
        B, T = index.shape
        emb_char = self.chr_emb(index)
        emb_pos = self.pos_emb(torch.arange(T, device=device))
        num = emb_char + emb_pos
        num = self.cores(num)
        num = self.final_ln(num)
        logits = self.final_proj(num)

        if t is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B * T, C)
            t = t.view(B * T)
            loss = F.cross_entropy(logits, t)

    def generate(self, ans, max_chars):

        for _ in range(max_chars):
            ans_croped = ans[:, -context:]
            logits, loss = self(ans_croped)
            logits = logits[:, -1, :]
            probabilities = F.softmax(logits, dim=-1)
            nxt = torch.multinomial(probabilities, 1)
            ans = torch.cat((ans, nxt), 1)
        return ans