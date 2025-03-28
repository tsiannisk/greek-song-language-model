import lyricsgenius
genius = lyricsgenius.Genius("")


def save_song(song_artist: str, song_name: str, lyrics: str):

    # Create a valid filename
    filename = "songs.txt"

    # Save the lyrics to the file
    with open(filename, "a", encoding="utf-8") as file:
        file.write(song_name + " by " + song_artist + "\n\n")
        file.write(lyrics + "\n\n")


artist = genius.search_artist("Snik",max_songs = 40, sort="title")
print(artist.songs)

for a in artist.songs:
    songtemp = artist.song(a.title)
    save_song(a.artist, a.title, artist.song(a.title).lyrics)
