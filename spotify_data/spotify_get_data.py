from pandas.core.interchange import dataframe
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pandas as pd
import os
import spotipy

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def get_track_uri(pickle_file: str) -> list[str]:
    df = pd.read_pickle(pickle_file)
    uri_list = list(df['uri'].unique())
    return uri_list


def get_track_ids(pickle_file: str) -> list[str]:
    df = pd.read_pickle(pickle_file)
    id_list = list(df['song_id'].unique())
    return id_list


class SpotifyAPI:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def get_audio_features(self, uri_list: list[str]) -> dataframe:
        audio_list = []
        counter = 0
        while True:
            print(counter, counter + 100)
            if counter + 100 < len(uri_list):
                uri = uri_list[counter: counter + 100]
                counter += 100
            elif counter < len(uri_list):
                uri = uri_list[counter: len(uri_list)]
                counter = len(uri_list)
                print('last loop')
            else:
                break

            results = self.spotify.audio_features(uri)

            audio_features_list = []
            for audio_features in results:
                try:
                    audio_features_list.append([
                        audio_features.get('acousticness'),
                        audio_features.get('danceability'),
                        audio_features.get('duration_ms'),
                        audio_features.get('energy'),
                        audio_features.get('instrumentalness'),
                        audio_features.get('key'),
                        audio_features.get('liveness'),
                        audio_features.get('loudness'),
                        audio_features.get('mode'),
                        audio_features.get('speechiness'),
                        audio_features.get('tempo'),
                        audio_features.get('time_signature'),
                        audio_features.get('uri'),
                        audio_features.get('valence')
                    ])

                    audio_list.extend(audio_features_list)
                except:
                    print("Failed to fetch audio features")
                    print(audio_features)

        result_df = pd.DataFrame(
            audio_list,
            columns=['acousticness',
                     'danceability',
                     'duration_ms',
                     'energy',
                     'instrumentalness',
                     'key',
                     'liveness',
                     'loudness',
                     'mode',
                     'speechiness',
                     'tempo',
                     'time_signature',
                     'uri',
                     'valence']
        )
        return result_df


def main():
    spotify = SpotifyAPI(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    id_list = get_track_ids('/Users/kohtaasakura/PyDev/grad_thesis/billboard/billboard_weekly_1960.pkl')
    df = spotify.get_audio_features(id_list)
    df.to_pickle('billboard_audio_features_1960.pkl')
    print()


if __name__ == '__main__':
    main()
