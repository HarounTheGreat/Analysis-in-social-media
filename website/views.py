from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

import os
import requests
from deep_translator import GoogleTranslator

import tweepy
from textblob import TextBlob


def twitterHero(data,size,lan):

    consumer_key="dL2sSrBj479rIwhsbAlcqwrgg"

    consumer_secret="AqOkmYUCRWQmMwPgwrx6mRU7M7yc1zMavTfpxMZPkJkbyVzyv0"

    access_token="1371237496344952836-PnjDJZp5OAIyQHtRr2yBzveNRBvYg1"
    access_token_secret="EsfMUOcypP8viblJrolb6WGpECfwl8oA3x7N2GrJZ1KVx"

    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)
    P=api.user_timeline(screen_name=data,count=size,tweet_mode="extended")

    S=[]
    counter=[0,0,0] # positive, negative, neutral
    for tweet in P:
        texttt  = tweet.full_text
        if lan==1:
            texttt = GoogleTranslator(target='en').translate(texttt)
            texttt = str(texttt)
        analysis=TextBlob(texttt)
        if analysis.sentiment.polarity > 0:
            res='positive'
            counter[0]+=1
        elif analysis.sentiment.polarity == 0:
            res='neutral'
            counter[2]+=1
        else:
            res='negative'
            counter[1]+=1
        S.append((tweet.full_text,analysis.sentiment,res,tweet.user.name,tweet.user.profile_image_url_https,tweet.user.screen_name))
    positivePer=(counter[0]/size)*100
    negativePer=(counter[1]/size)*100
    neutralPer=(counter[2]/size)*100
    S.append((positivePer,negativePer,neutralPer))
    return S


def index(request):
    return render(request,'website/home.html',{})


def form_data(request):
    try:
        data=request.POST['q']
        size=int(request.POST['size'])
        lan=int(request.POST['lan'])
        condition=0
    except MultiValueDictKeyError:
        data='BillGates'
        size=50
        condition=1
        lan=0
    # if data=='':
    #     data='data science'
    #     condition=1
    S=twitterHero(data,size,lan)
    # logger.log(100,"Called function.")
    posPer,negPer,ntrPer=S[-1][0],S[-1][1],S[-1][2]
    del S[-1]
    return render(request,'website/index.html',{'data':S,'search':data,'posPer':posPer,'negPer':negPer,'ntrPer':ntrPer,"condition":condition})
