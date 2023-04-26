import spotipy
import random
import pygame
import os
from spotipy.oauth2 import SpotifyClientCredentials
from plugin import plugin


# Authenticate with Spotify API using your own credentials
client_id = "8befa2ab1c824b38838f90f69e2813ce"
client_secret = "2fe92c4947a543a2885993586923106f"
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@plugin('songquiz')
def songquiz(jarvis, s):
    while True:
        game_mode = jarvis.input("Select game mode (1 for single player, 2 for multiplayer): ")

        if game_mode == "1":
            single_player(jarvis)
            break
        elif game_mode == "2":
            multi_player(jarvis)
            break
        else:
            jarvis.say("Invalid input. Please enter 1 or 2.")

# refactored method for input of genre of music
def _get_query(jarvis, theme):
    if theme == "1":
        return "genre:hip-hop"
    elif theme == "2":
        return "genre:rock"
    elif theme == "3":
        return "genre:pop"
    else:
        return None

# refactored method for playing 30 second music sample
def _play_preview(jarvis, track):
    preview_url = track["preview_url"]
    if preview_url:
        preview_file = f"{track['id']}.mp3"
        os.system(f"curl -o {preview_file} {preview_url}")

        pygame.mixer.init()
        pygame.mixer.music.load(preview_file)
        pygame.mixer.music.play()

    # Clean up the downloaded preview file
    if preview_url:
        os.remove(preview_file)

def _stop_preview(jarvis):
    pygame.mixer.music.stop()

def _get_guess(jarvis, player_num):
    jarvis.say(f"Player {player_num}, guess the name and artist of song:")
    guess_name = jarvis.input("Name: ")
    guess_artist = jarvis.input("Artist: ")
    return guess_name, guess_artist

def _check_answer(jarvis, guess_name, guess_artist, track):
    correct_name = track["name"]
    correct_artist = track["artists"][0]["name"]
    if guess_name.lower() == correct_name.lower() and guess_artist.lower() == correct_artist.lower():
        return True
    else:
        return False

def single_player(jarvis):
    while True:
        theme = jarvis.input("Choose a Spotify Theme by Selecting a #: \n"
                      "1. Hip-Hop \n"
                      "2. Rock \n"
                      "3. Pop \n")

        query = _get_query(jarvis, theme)
        if query is None:
            jarvis.say("Invalid input. Please enter 1, 2, or 3.")
        else:
            break

    score = 0
    for i in range(6):
        results = sp.search(q=query, type="track", limit=50)
        tracks = results["tracks"]["items"]

        track = random.choice(tracks)
        correct_name = track["name"]
        correct_artist = track["artists"][0]["name"]
        #jarvis.say(f"Now playing: {track['name']} by {track['artists'][0]['name']}")

        _play_preview(jarvis, track)

        guess_name, guess_artist = _get_guess(jarvis, 1)

        jarvis.say(f"The correct answer was {correct_name} by {correct_artist}.")

        _stop_preview(jarvis)

        if _check_answer(jarvis, guess_name, guess_artist, track):
            score += 1

        jarvis.say(f"Your score is {score}.")

    jarvis.say("Game over!")

def multi_player(jarvis):
    player_scores = [0, 0]

    while True:
        # Search for tracks based on theme
        theme = jarvis.input("Choose a Spotify Theme by Selecting a #: \n"
                      "1. Hip-Hop \n"
                      "2. Rock \n"
                      "3. Pop \n")

        query = _get_query(jarvis, theme)
        if query is None:
            jarvis.say("Invalid input. Please enter 1, 2, or 3.")
        else:
            break

    for i in range(6):
        results = sp.search(q=query, type="track", limit=50)
        tracks = results["tracks"]["items"]

        track = random.choice(tracks)
        correct_name = track["name"]
        correct_artist = track["artists"][0]["name"]
        #jarvis.say(f"Now playing: {track['name']} by {track['artists'][0]['name']}")

        _play_preview(jarvis, track)

        for i in range(2):
            guess_name, guess_artist = _get_guess(jarvis, i + 1)
            if _check_answer(jarvis, guess_name, guess_artist, track):
                player_scores[i] += 1

        jarvis.say(f"The correct answer was {correct_name} by {correct_artist}.")

        _stop_preview(jarvis)

    if player_scores[0] > player_scores[1]:
        jarvis.say("Player 1 wins!")
    elif player_scores[1] > player_scores[0]:
        jarvis.say("Player 2 wins!")
    else:
        jarvis.say("Tie game!")

    jarvis.say("Game over!")