from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
import requests
from django.contrib import messages
from deep_translator import GoogleTranslator
import facebook
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from home.models import  AccessTokenFB
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# @login_required(login_url='/login')
# def get_token (request):
#     current_user=request.user
#     if request.method=="POST":
#         if AccessTokenFB.objects.all() is not None:
#             access= AccessTokenFB.objects.get(user_id=current_user.id)
            
#         else:
#             access= AccessTokenFB()
#             token = request.POST.get('token')
#             access.profile_id=current_user.id
#             access.save()
        
#         return HttpResponseRedirect("/facebookapp/new") 
#     else:
#         return render(request,'facebookapp/token.html',{})
@login_required(login_url='/login')
def get_token (request):
    current_user=request.user
    token=None
    if request.method=="POST" and 'analyse' in request.POST:
        try:
            access= AccessTokenFB.objects.get(user_id=current_user.id)
            token=access.token
            return HttpResponseRedirect("/facebookapp/new") 
        except ObjectDoesNotExist:
            return HttpResponseRedirect("/facebookapp/savetoken")
    
    if request.method=="POST" and 'save' in request.POST:
        return HttpResponseRedirect("/facebookapp/savetoken")
    
    if request.method=="POST" and 'update' in request.POST:
        return HttpResponseRedirect("/facebookapp/updatetoken")
    
    return render(request,'facebookapp/token.html',{"token":token})

    
def save_token (request):
    current_user=request.user
    try :
        if request.method=="POST":
            new=AccessTokenFB()
            token=request.POST.get("token")
            new.token=token
            new.user_id=request.user.id
            new.save()
            return HttpResponseRedirect("/facebookapp/new")
        else:
            return render(request,'facebookapp/savetoken.html',{})
    except Exception as e :
        messages.warning(request,"You Already Have An Access Token!  To Change It Click On 'Update Your Access Token' ")
        return HttpResponseRedirect("/facebookapp/token")



def update_token (request):
    try :
        current_user=request.user
        update=AccessTokenFB.objects.get(user_id=current_user.id)
        if request.method=="POST":
            
            token=request.POST.get("token")
            update.token=token
            update.save()
            return HttpResponseRedirect("/facebookapp/new")
        else:
            return render(request,'facebookapp/updatetoken.html',{})   
    except Exception as e :
        messages.warning(request,"You Don't Have An Access Token!  Please Click On 'Don't Have Access Token' ")
        return HttpResponseRedirect("/facebookapp/token")        


def form_data(request):
    current_user=request.user.id
    token=AccessTokenFB.objects.get(user_id=current_user)
    token=token.token
    graph = facebook.GraphAPI(token)
    def getComments(path,lan,size):
        S=[]
        numberss=[]
        counter=[0,0,0]
        sentencesComments = []
        timeComments = []
        data=[]
        s = path
        s=s[s.find('m')+2:]+"azezea"
        new=""
        for i in range(len(s)):
            if s[i] in ["0","1","2","3","4","5","6","7","8","9"] :
                new=new+s[i]
            if s[i] not in ["0","1","2","3","4","5","6","7","8","9"] :
                break
        new2= ""
        new1= ""
        for i in range(len(s)): 
            if s[i] in ["/"] and s[i+1] in ["0","1","2","3","4","5","6","7","8","9"] : 
                new2=s[i+1:]
                for j in range(len(new2)) :
                    if new2[j] in ["0","1","2","3","4","5","6","7","8","9"] :
                        new1=new1+new2[j]
        path=new + "_" + new1
        comments  = graph.get_connections(id = path, connection_name ='comments',  
                                        include_hidden = True, order ='reverse_chronological', 
                                        filter ='stream', summary ='total_count') 
        cnt = 0
        l_positive=[]
        l_negative=[]
        l_neutre=[]
        
        for comment in comments['data']:
            texttt = comment['message']
            cnt = cnt + 1
            numberss.append(cnt)
            sentencesComments.append(comment['message'])
            data.append((comment['id'],comment['message'],cnt))
            if cnt > size and size!=1 :
                break
            if lan==1:
                texttt = str(texttt)
                texttt = GoogleTranslator(target='en').translate(texttt)
                texttt = str(texttt)
            analysis=TextBlob(texttt)
            if analysis.sentiment.polarity > 0:
                res='positive'
                counter[0]+=1
                l_positive.append((comment['message']))
            elif analysis.sentiment.polarity == 0:
                res='neutral'
                counter[2]+=1
                l_neutre.append((comment['message']))
            else:
                res='negative'
                counter[1]+=1
                l_negative.append((comment['message']))
                
                
        positivePer=(counter[0]/cnt)*100
        negativePer=(counter[1]/cnt)*100
        neutralPer=(counter[2]/cnt)*100
        S.append((positivePer,negativePer,neutralPer))
        return sentencesComments,S,data,l_positive,l_neutre,l_negative

    try:
        post_id=request.POST['path']
        lan=int(request.POST['lan'])
        size=int(request.POST['size'])
        condition=0
        sentencesComments,S,data,l_positive,l_neutre,l_negative=getComments(post_id,lan,size)
    except Exception as e:
        h ="EAATf8DFXZATYBAKX6hkRHbBpWCXAdvd7wT7pE4JDHYtznzOqSH2DNEm5I5fnlydLQ8mVrEBwACzDnl7uxgZCmZCqUsg0cXdOmkGgrZBm7WBUdoEu5PZBamo4lCgy9IYXEGfHiCunUAi7WbGv3cGZAe7DsVPJsuZAEm6zTRaxWI9grNnZBbOAHdXiAFdbTqM7kbfxWBvSvBiP3QZDZD"
        graph = facebook.GraphAPI(h)
        post_id='https://www.facebook.com/102517818587306/photos/a.102517905253964/102520888586999/'
        lan = 0
        condition=1
        size = 3
        sentencesComments,S,data,l_positive,l_neutre,l_negative=getComments(post_id,lan,size)

    posPer,negPer,ntrPer=S[-1][0],S[-1][1],S[-1][2]
    del S[-1]
    return render(request,'facebookapp/index.html',{'data':data,'positive':l_positive,"negative":l_negative,"neutre":l_neutre, "l_comments":sentencesComments,'posPer':posPer,'negPer':negPer,'ntrPer':ntrPer,"condition":condition})


