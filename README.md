# Greek Song Lyrics Language Model

This project builds a character-level language model based on a Transformer architecture to generate Greek song lyrics. The dataset consists of lyrics from various Greek artists, collected from Genius and processed for training and testing.

## Project Overview

### 1. Data Collection & Processing
- **`dataset.py`**: Collects lyrics from Greek artists from Genius and stores them in separate files.
- **`concat.py`**: Combines all the individual files into a single dataset (`songs.txt`).
- **`shuffle_songs.py`**: Mixes the songs to ensure diversity across training and test data.

### 2. Transformer Model
- **`TransformerFromScratch.py`**: Implements a Transformer model from scratch based on the paper *Attention is All You Need*.
- The model is designed for character-level prediction to generate Greek lyrics.

### 3. Training the Language Model
- The model is trained on `songs.txt` to learn patterns in Greek song lyrics and generate new lyrics.

## Installation & Usage

### Prerequisites
Make sure you have Python installed along with the necessary dependencies:
```bash
pip install torch numpy
```

### Running the Project
1. **Collect Lyrics:**
   ```bash
   python dataset.py
   ```
2. **Concatenate Files:**
   ```bash
   python concat.py
   ```
3. **Shuffle Songs:**
   ```bash
   python shuffle_songs.py
   ```
4. **Train the Model:**
   ```bash
   python TransformerFromScratch.py
   ```

## Results & Future Improvements
- The model can generate Greek lyrics based on learned patterns.
- Future improvements include training on larger datasets and fine-tuning hyperparameters for better text generation.

## Contributions
Feel free to fork this repository, submit pull requests, or open issues if you have suggestions!

## License
This project is open-source under the MIT License.

