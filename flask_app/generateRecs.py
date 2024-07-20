import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import requests
from pymongo import MongoClient
import certifi
import os
import numpy as np

from river import linear_model
from river import optim
from river import metrics



#About the incremental learning model: it uses stochastic gradient descent https://riverml.xyz/dev/examples/batch-to-online/






def generateRecs(goodIDs, sp, model, metric, learned, currSong, artist, opinion):
    

    #Connecting to MongoDB Database
    # os.environ["PYTHONWARNINGS"] = "ignore:Unverified HTTPS request"
    # mongo = MongoClient('mongodb+srv://shriyamahakala:2BjCwDdbJ4Ux1ma9@browser.04wdzqe.mongodb.net/?retryWrites=true&w=majority&appName=Browser', tlsCAFile=certifi.where())
    # db = mongo['songreqs']
    # tasks = db["songs"]

    #Once app, database are set up, song reqs will instead by the songs from the database

    #As it was, Lover, Pipe Down Drake, Stir Fry Migos
    songreqs = {"4Dvkj6JhhA12EX05fT7y2e":0.4, "1dGr1c8CrMLDpV6mPbImSI": 0.9, "11pEKMLmavDu8fxOB5QjbQ":0.75, "2UVbBKQOdFAekPTRsnkzcf":0.3} #holds the data about songs recomended from app


    #Incremental Learning Logistic Regression Function
   #This block below was just for testing purposes. Ignore it
    # recommended = [{"id":"erjk","name":"song1", "artist":"artist1"}, {"id":"erjk","name":"song1", "artist":"artist1"}]
    # s = json.dumps(recommended)
    # res = requests.post("http://127.0.0.1:5000/song", json=s).json()
    # # res = requests.get("http://127.0.0.1:5000/song", json=s).json()
    # print(res)
    # break
        
        
        #getting unique spotify id for song
    try:
        query = f"track:\"{currSong}\" artist:\"{artist}\""
        results = sp.search(q=query, limit=1, type='track')
        id = results['tracks']['items'][0]['id']
    except Exception as e:
        print(e)
        print("Song not found")
        return
        
    print(id)
        
    if id in songreqs:
        if opinion == 'y':
            y = 1
        else:
            y = 0
            
        y_pred = model.predict_one({"score":songreqs[id]})
        metric.update(y, y_pred)
        model.learn_one({"score":songreqs[id]}, y)
            
        print(f"Accuracy: {metric.get()}", f"y_pred: {y_pred}", f"y_true: {y}")
        del songreqs[id]
        learned+=1
            
        
    if opinion == 'n':
        return 
        
        
    goodIDs.append(id)
        
        
    #query user recommended songs from "songreqs". Get all the songs that the predictor classifies as 1 (for now just run it over the 
    # entire dict and later you can make it more efficient by mainting an ordered dict and running from highest score to lowest)
    query = []
        
        
    if learned>=3:
        for id in songreqs:
            if model.predict_one(songreqs[id]):
                query.append(id)
        
    query = query + goodIDs
        
    result = sp.recommendations(seed_tracks=query, limit=5)
        
    recommended = []
    for song in result['tracks']:
        recommended.append({"name":song['name'], "artist":song['artists'][0]['name']})
        
    return recommended
        

if __name__ == "__main__":
    optimizer = optim.SGD(lr=0.01)
    model = linear_model.LogisticRegression(optimizer)
    metric = metrics.Accuracy()
    
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    learned = 0
    goodIDs = [] #running list of all the ids deemed good by DJ
    #asyncio.run(main())
    while True:
        currSong = input("Enter song: ")
        artist = input("Enter artist: ")
        opinion = input("Is this song good? (y/n): ")
        generateRecs(goodIDs, sp, model, metric, learned, currSong, artist, opinion)







#convert to use apple music api instead of spotify api


#recommend songs based on all the songs in goodids plus the queried song using the spotify recommend feature
       
#update songreqs dict to see any new entries and recompute scores for all songs in the dict
        
        
        
#Plans for GUI:
#eventually make it so it detects the current song and artist. Make it a button so DJ can select whether 
#song is "good or not" easily. 
#GUI should show a leaderboard of the song from the user plus their upvotes
#GUI should also show the recommendations in order of closest BPM to the current song

#Use Pytest Unit Tests