from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
import os
import requests
from textblob import TextBlob
from googleapiclient.discovery import build
from pytube import extract
from deep_translator import GoogleTranslator
from pytube import extract


def video_comments(data,size,lan):
    api_key='AIzaSyBvaQJX-uvbKcMZNWTysv9HsHK5EtBLNm8'
    S=[]
    t=False
    for i in data:
        if i ==" ":
            t=True
            a=data.split()
            data=a[0]
            a=a[1]
            break
    url=data
    data=extract.video_id(url)
    youtube = build('youtube', 'v3',
                    developerKey=api_key)
  
    video_response=youtube.commentThreads().list(
    part='snippet',maxResults=10000,videoId=data).execute()
    counter=[0,0,0]
    cnt=0
    lpositive=[]
    lnegative=[]
    lneutre=[]
    sentencesComments = []
    for item in video_response['items'] :
        texttt = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comment = texttt
        names=item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        images=item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']
        chaine=item['snippet']['topLevelComment']['snippet']['authorChannelUrl']
        time=item['snippet']['topLevelComment']['snippet']['updatedAt']
        time=time[0:4]
        ok=False
        if (t and time==a):
            ok=True
        if ((ok and t) or t==False):
            sentencesComments.append((names,images,chaine,comment))
            if lan==1:
                texttt = GoogleTranslator(target='en').translate(comment)
                texttt = str(texttt)
            analysis=TextBlob(texttt)
            cnt=cnt+1
            if cnt > size and size != 1 :
                break            
            if analysis.sentiment.polarity > 0:
                res='positive'
                counter[0]+=1
                lpositive.append(comment)
            elif analysis.sentiment.polarity == 0:
                res='neutral'
                counter[2]+=1
                lneutre.append(comment)
            else:
                res='negative'
                counter[1]+=1
                lnegative.append(comment)
    positivePer=(counter[0]/cnt)*100
    negativePer=(counter[1]/cnt)*100
    neutralPer=(counter[2]/cnt)*100
    S.append((positivePer,negativePer,neutralPer))
    return sentencesComments,S,lpositive,lneutre,lnegative

data = "q"

def index(request):
    return render(request,'ytb/home.html',{})

def form_data(request):
    try:
        condition=0
        data=request.POST['q']
        size=int(request.POST['size'])
        lan=int(request.POST['lan'])           
        sentencesComments,S,lpositive,lneutre,lnegative=video_comments(data,size,lan)
    except Exception as e:
        data= "https://www.youtube.com/watch?v=odDwnnH8Cr4"
        size=3
        lan=0
        condition=1
        sentencesComments,S,lpositive,lneutre,lnegative=video_comments(data,size,lan)
    posPer,negPer,ntrPer=S[-1][0],S[-1][1],S[-1][2]
    del S[-1]
    return render(request,'ytb/index.html',{'data':S,'search':data,'positive':lpositive,"negative":lnegative,"neutre":lneutre,'posPer':posPer,'negPer':negPer,'ntrPer':ntrPer,"sentencesComments":sentencesComments,"condition":condition})
