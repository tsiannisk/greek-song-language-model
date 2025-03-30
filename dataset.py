import lyricsgenius
genius = lyricsgenius.Genius("")

def remove_bracket_lines(lyrics):

    lines = lyrics.splitlines()

    filtered_lines = [line for line in lines if not line.lstrip().startswith(('(', '['))]  # avoid refrens or couple stating

    return '\n'.join(filtered_lines)


def save_song(song_artist: str, song_name: str, lyrics: str, newname:str, fl:bool):

    filename = "NameOfArtist.txt"

    with open(filename, "a", encoding="utf-8") as file:
        for i in range(len(song_name)):
            if ((song_name[i]>='a' and song_name[i]<='z') or (song_name[i]>='A' and song_name[i]<='Z') or (song_name[i]>='0' and song_name[i]<='9') or (song_name[i] == '(' or song_name[i] == ')' or song_name[i] == ' ') or (song_name[i] == '[' or song_name[i] == ']' or song_name[i] == '-' or song_name[i] == '’' or song_name[i] == '-' or song_name[i] == '!' or song_name[i] == '.' or song_name[i] == ',') ):
                continue
            fl = 1
            while (i<len(song_name) and song_name[i]!= '(' and song_name[i] != ')' and song_name[i] != '[' and song_name[i] != ']' ):
                newname +=song_name[i]
                i+=1
            break
        if (fl):
            file.write("Τίτλος: "+ newname + "\n\n")
            file.write(remove_bracket_lines(lyrics) + "\n\n\n\n\n\n\n") # put 7 endlines between the songs



artist = genius.search_artist("Theodoridou", sort="title")
print(artist.songs)
newname=''
for a in artist.songs:
    songtemp = artist.song(a.title)
    newname = ''
    fl = 0
    save_song(a.artist, a.title, artist.song(a.title).lyrics,newname,fl)
