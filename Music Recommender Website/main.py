from pywebio.output import *
from pywebio.pin import *
from pywebio.platform import start_server

import numpy as np
import pandas as pd

df = pd.read_csv('preprocessed data.csv')
num_tracks = 30
partial_url = 'https://open.spotify.com/track/'

def parse_song_id(song_url):
    separated_1 = song_url.split('track/')
    separated_2 = separated_1[1].split('?')
    return separated_2[0]


def rec_songs(song_url, new_df):
    song_id = parse_song_id(song_url)
    with use_scope('output', clear=True):
        given_track_df = new_df.loc[new_df['id'] == song_id]
        given_track_array = np.array(given_track_df.drop(['id', 'name', 'artist'], axis=1)).reshape(-1,)

        put_text('Track Entered: ')
        put_link(given_track_df['name'].to_list()[0] + ' - ' + given_track_df['artist'].to_list()[0], url=partial_url+given_track_df['id'].to_list()[0])
        put_text('\n')
            
        track_distances = []

        for i in range(len(new_df)):
            track_id = new_df.iloc[i]['id']
            track_array = np.array(new_df.iloc[i].drop(['id', 'name', 'artist']))
            euclid_dist = np.linalg.norm(given_track_array - track_array)
            track_distances.append((track_id, euclid_dist))

        sorted_tracks = sorted(track_distances, key=lambda x: x[1])

        described_songs = []
        for i in range(len(sorted_tracks)-1):
            song_df = new_df[new_df['id']==sorted_tracks[i+1][0]]
            described_song = (song_df.iloc[0]['name'], song_df.iloc[0]['artist'], song_df.iloc[0]['id'])
            described_songs.append(described_song)
        
        put_text('Recommended Songs:')

        i = 0
        j = 0
        while i < num_tracks:
            if (described_songs[j][0] == given_track_df['name'].to_list()[0]):
                j += 1
                continue
            put_link(described_songs[j][0] + ' - ' + described_songs[j][1], url=partial_url+described_songs[j][2])
            put_text()
            i += 1
            j += 1


def main():
    put_html('<h1>Music Recommender</h1>')
    put_input('song_url', label='Enter a Spotify song URL.')
    put_button('Recommend Songs', lambda: rec_songs(pin.song_url, df))


if __name__ == '__main__':
    start_server(main, port=8080, debug=True)