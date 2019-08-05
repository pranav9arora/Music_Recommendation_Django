import spotipy
import spotipy.oauth2

spotify = spotipy.Spotify()
import spotipy.util as util

scope = "user-read-private,user-read-birthdate,user-read-email,user-library-read,playlist-read-private,playlist-read-collaborative"
username = 'n7t4dng4pvzdkugceo7qesjfg'
# for authorization
token = util.prompt_for_user_token(username, scope, client_id='066360a187c24dd2be5d73968eeba346',
                                   client_secret='99b2bdda7fee47d4ac169dbfe4c6a8e5', redirect_uri='http://localhost/')

features_list = []


# token = util.prompt_for_user_token(username, scope)
def process(filewriter):
    if token:
        sp = spotipy.Spotify(auth=token)
        getUsersPlaylist(filewriter)

    else:
        print("Can't get token for", username)


import csv


# call to get particular track details. it will be used for svm classification
def getFeatures(track_id, track_name, artist_name,artist_id,filewriter):
    print('getting feature of each track')
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.audio_features(track_id)
        print(results)
        acousticness = results[0]['acousticness']
        danceability = results[0]['danceability']
        energy = results[0]['energy']
        instrumentalness = results[0]['instrumentalness']
        key = results[0]['key']
        liveness = results[0]['liveness']
        loudness = results[0]['loudness']
        speechiness = results[0]['speechiness']
        tempo = results[0]['tempo']
        print(str(acousticness) + ':' + str(danceability))
        features_list.append(str(artist_name))
        features_list.append(str(artist_id))
        features_list.append(str(track_name))
        features_list.append(str(acousticness))
        features_list.append(str(danceability))
        features_list.append(str(energy))
        features_list.append(str(instrumentalness))
        features_list.append(str(key))
        features_list.append(str(liveness))
        features_list.append(str(loudness))
        features_list.append(str(speechiness))
        features_list.append(str(tempo))

        print(features_list)
        check_commas = 0
        check_commas = str(features_list).count(',')
        print('commas=' + str(check_commas))
        if check_commas < 12:
            filewriter.writerow(features_list)
        features_list.clear()


def getUsersPlaylist(filewriter):
    if (token):
        sp = spotipy.Spotify(auth=token)
        # print(sp.current_user())
        playlist = sp.user_playlists('vdgey9z8uecchcrb3xl6wsv73')
        # print(playlist)
        print('getting users playlist')
        for item in playlist['items']:
            print(item['name'])
            print(item['id'])
            getArtistsFromTrack(item['id'],filewriter)


#        6Rl6mV4WtHGTQRjyp5zLDu,2B8XWcHME4UePquOU6QDPh


artist_id = []


# now get each and every songs in that playlist with artist name
def getArtistsFromTrack(track_id,filewriter):
    if (token):
        sp = spotipy.Spotify(auth=token)
        # print(sp.current_user())
        playlist = sp.user_playlist_tracks(username, track_id)
        # print(playlist)
        print('getting artists from users track')
        for item in playlist['items']:
            print('Track name:' + item['track']['name'])
            # print(item['track']['album']['artists'])
            artists = item['track']['album']['artists']
            # print(item['track']['album']['artists'][0]['name'])
            # print(item['track']['album']['artists'][0]['id'])
            for artist in artists:
                print(artist['name'])
                print(artist['id'])
                aid = artist['id']
                #  Get an Artist's Related Artists
                try:
                    b = artist_id.index(str(aid))
                    print('artist found at index '+str(b))
                except Exception as e:
                    print(e)
                    getTopTracksOfArtist(artist['id'], artist['name'],filewriter)
                    artist_id.append(str(aid))
                    getRelatedArtists(aid,filewriter)


artists_id = []


def getRelatedArtists(artist_id,filewriter):
    if (token):
        sp = spotipy.Spotify(auth=token)
        # print(sp.current_user())
        artists = sp.artist_related_artists(artist_id)
        # print(playlist)
        print('getting artists from users track')
        for artist in artists['artists']:
            print(artist['name'])
            print(artist['id'])

            try:
                b = artists_id.index(str(artist['id']))
                print('artist found at index ' + str(b))
            except ValueError:
                try:
                    getTopTracksOfArtist(artist['id'], artist['name'],filewriter)
                    artists_id.append(str(artist['id']))
                except Exception as e:
                    print(e)




def getTopTracksOfArtist(artist_id, artist_name,filewriter):
    if (token):
        sp = spotipy.Spotify(auth=token)
        # print(sp.current_user())

        tracks = sp.artist_top_tracks(artist_id, 'ES')
        # print(tracks)
        print('getting tracks of single artist')
        for track in tracks['tracks']:
            print('Track name:' + track['name'])
            print('Track name:' + track['id'])
            track_name = track['name']
            getFeatures(track['id'], track_name, artist_name,artist_id,filewriter)


def callableFun():
    with open('source/content/media/train.csv', 'a') as csvFile:
        filewriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(
            ['Artist', 'Track', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness',
             'loudness', 'speechiness', 'tempo'])
        process(filewriter)
    csvFile.close()


if __name__ == '__main__':
    callableFun()
