from flask import Flask
from flask import request
import json
from generateRecs import generateRecs
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import numpy as np
from identify import detection

from river import compose
from river import linear_model
from river import optim
from river import metrics

app = Flask(__name__)

optimizer = optim.SGD(lr=0.01)
model = linear_model.LogisticRegression(optimizer)
metric = metrics.Accuracy()
    
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

goodIDs = [] #running list of songs deemed good by DJ




@app.route('/songRated', methods=['POST']) #it's going to be a post only
def getRecs():
    data = request.get_json() #data posted is going to be currSongName, currArtist, opinion
    print(data)
    recs = generateRecs(goodIDs, sp, model, metric, data["learned"], data["currSong"], data["currArtist"], data["opinion"])
    return recs
    
@app.route('/detectSong', methods=['POST']) #it's going to be a post only
def getSong():
    song = detection()
    return song



#What this all does. You have a list of songs that have been recommended to the DJ. 
# The DJ can rate the songs as good or bad. You also have songs that the DJ has rated as good. 
#The app will recommend songs based on "good songs" and add this to the user recommendations that the 
#algorithm has deemed are worth listening to.

#Plans for GUI:
#1. Just get the rate a song and receive recommendations working.
#2. Get the recommendations to show up in most similar BPM to least
#3. Shazam API to detect songs instead of user typing songs 

#Once Shobini gets the app working, and saving the data to a database or something. we can work on leaderboard


#GUI should show a leaderboard of the songs being upvoted by the user that is continously updated. 
# For now every time a song is rated, it updates leaderboard and recommendations board (So just a POST request basically)