import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials

# Authenticate with Spotify API
client_id = "your_client_id_here"
client_secret = "your_client_secret_here"
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Step 5: Search for tracks based on theme
# Need to figure out if you want to only have the option of one
# type or have multiple playlists options
results = sp.search(q="90s pop hits", type="track", limit=50)
tracks = results["tracks"]["items"]

# this is supposed to loop for 6 songs
for x in range(6):
    # Step 6: Play a short preview of a random track

    track = random.choice(tracks)
    print(f"Now playing: {track['name']} by {track['artists'][0]['name']}")
    print(f"Preview: {track['preview_url']}")

    # Step 7: Prompt user to guess the name and artist
    guess_name = input("Guess the name of the song: ")
    guess_artist = input("Guess the name of the artist: ")

    # Need to keeping track of the points
    # also need to figure out way to separate player 1 and player 2
    # if there is a player 2


    # Step 8: Check user's answer
    correct_name = track["name"]
    correct_artist = track["artists"][0]["name"]
    if guess_name.lower() == correct_name.lower() and guess_artist.lower() == correct_artist.lower():
        print("Correct!")


    else:
        print(f"Incorrect. The correct answer was {correct_name} by {correct_artist}.")
