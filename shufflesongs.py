import random

def extract_and_shuffle_songs(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()

        songs = content.split('\n' * 6)
        random.shuffle(songs)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write('\n\n\n\n\n\n\n'.join(songs))  # Add 7 newlines between songs in the output file

        print(f"Songs have been extracted, shuffled, and saved to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


input_file = "concatsongs.txt"
output_file = "songs.txt"

extract_and_shuffle_songs(input_file, output_file)