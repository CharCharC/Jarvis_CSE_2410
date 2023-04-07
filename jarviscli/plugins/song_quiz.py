import spotipy
import random
import pygame
import os
from spotipy.oauth2 import SpotifyClientCredentials
from plugin import plugin

@plugin('song_quiz')
def song_quiz(jarvis,s):

    # Authenticate with Spotify API using your own credentials
    client_id = "8befa2ab1c824b38838f90f69e2813ce"
    client_secret = "2fe92c4947a543a2885993586923106f"
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Search for tracks based on theme
    theme = input("Choose a Spotify Theme by Selecting a #: \n"
                       "1. Hip-Hop \n"
                       "2. Rock \n"
                       "3. Pop \n")

    if theme == "1":
        query = "genre:hip-hop"
    elif theme == "2":
        query = "genre:rock"
    elif theme == "3":
        query = "genre:pop"

    score = 0

    for i in range(6):
        results = sp.search(q=query, type="track", limit=50)
        tracks = results["tracks"]["items"]

        # Play a short preview of a random track
        track = random.choice(tracks)
        print(f"Now playing: {track['name']} by {track['artists'][0]['name']}")

        # Use pygame to play the preview of the track
        preview_url = track['preview_url']
        if preview_url:
            # Download the preview file from Spotify
            preview_file = f"{track['id']}.mp3"
            os.system(f"curl -o {preview_file} {preview_url}")

            # Initialize Pygame mixer and play the preview file
            pygame.mixer.init()
            pygame.mixer.music.load(preview_file)
            pygame.mixer.music.play()

        # Prompt user to guess the name and artist
        guess_name = input("Guess the name of the song: ")
        guess_artist = input("Guess the name of the artist: ")

        # Check user's answer
        correct_name = track["name"]
        correct_artist = track["artists"][0]["name"]
        if guess_name.lower() == correct_name.lower() and guess_artist.lower() == correct_artist.lower():
            print("Correct!")
            score += 1  # increment score by 1
        else:
            print(f"Incorrect. The correct answer was {correct_name} by {correct_artist}.")

        # Clean up the downloaded preview file
        if preview_url:
            os.remove(preview_file)

        print(f"Your score is {score}.")  # show the score to the user

    print("Game over!")
