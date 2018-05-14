from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
import tweepy,json
import re
from textblob import TextBlob
from mtranslate import translate
from Tweets.models import Tweets
hash_list=Tweets.objects.values_list('tweet_id')
print(hash_list)
# Create your views here.

ckey = ["0HbmxMUQ5DczFuKbpUt1WFQA9",'OYmhPs9dX4HHOQWN3D4c14hgZ']
csecret = ["LjC1kTMY3LrnzBX8cMZrhTWLXXDRLBCa4ZSfXMwO42244V6O5U",'BicrMWXg9FjuQN1FkTdbYoyRViQEeW1zFNW2upSdpZdPnJWJrk']
atoken = ["2516974466-EyjU0m1wGFYJpYXoi88SGZQTtHk3PEtrkUdE4OK",'934723685415448576-xLzB7gRVWBBOiOgrbQkVooEFl9fnIkD']
asecret = ["VZGEEkH7HiytC3abwrTpTDmONsJ7SWbJkHD8XdjGSSzfF",'KBjSd3gE9vwx0JlAnR9JReOVDB68gXJzpgSWGRw1BIwxD']
auth = tweepy.OAuthHandler(ckey[0],csecret[0])
auth.set_access_token(atoken[0], asecret[0])
api = tweepy.API(auth)

'''auth1 = tweepy.OAuthHandler(ckey[1],csecret[1])
auth1.set_access_token(atoken[1], asecret[1])
api1 = tweepy.API(auth1)'''


def index(request):
    template = loader.get_template('form.html')
    return HttpResponse(template.render({},request))

def clean_tweet(tweet):return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0 : return 'positive'
    elif analysis.sentiment.polarity == 0 : return 'neutral'
    else : return 'negative'

def get_url(text):
    url=''
    text=text.split()
    for i in text:
        if 'https:' in i:
            url+=i
            url+='\n'
        else:pass
    return url

def get_replies(id,name):
    x=""
    try:replies=tweepy.Cursor(api.search, q=name ,since_id=id, tweet_mode='extended').items()
    except:print("error")
    if replies:
        for r in replies:
            if r._json["in_reply_to_status_id"] == id:
                x+=r._json['user']['screen_name']
                x+=" : "
                x+=r._json['full_text']
    else:pass
    return x



def form_result(request):
    global hash_list
    hash_list = Tweets.objects.values_list('tweet_id')
    print(hash_list)
    #print("hashlist",hash_list[0].Hashtag)
    if request.GET['hashtag']:
        message=''
        hashtag=request.GET['hashtag']
        try:all_tweets = tweepy.Cursor(api.search, q=hashtag,tweet_mode='extended').items(20)
        except:print("error")
        d={}
        cnt=0

        for t in all_tweets:
            new_d = {}
            cnt+=1
            list = t._json['created_at'].split()
            datetime = list[0] + " " + list[3] + " " + list[2] + "/" + list[1] + "/" + list[-1]
            new_d['id']=t._json['id']
            new_d['username']=t._json['user']['screen_name']
            print(type(t._json['full_text']))
            print(t._json['full_text'])
            new_d['text']=t._json['full_text'].encode().decode()
            new_d['followers_count']=t._json['user']["followers_count"]
            new_d['lang']=t._json['lang']
            new_d['created_at']=datetime
            new_d['retweet_count']=t._json['retweet_count']
            new_d['favorite_count']=t._json['favorite_count']
            #new_d['toxic']=toxic
            #new_d['url']=get_url(t._json['text'])
            #new_d['replies']=''
            d['Tweet_' + str(cnt)] = new_d
        #print(d)
        dump_d=json.dumps(d)
        dump_d1=json.dump(d,open('just.json','a'),sort_keys = True,indent = 4)
        #print(type(dump_d))
        json_d=json.loads(dump_d)

        #print(json_d)
        if json_d:
            x = "<div align=\"center\">"
            xcnt=0
            for i in json_d:
                if xcnt % 2 == 0:
                    #print('if ',xcnt%2)
                    x+="<fieldset style=\"width:900px; border-style: solid; border-width: 5; border-color:#0084b4;\"><legend style=\"margin-right:910px; color:#3A3A3A;\"><h3><b>"+str(i)+"</b></h3></legend><p align=\"left\" style=\"font-size:20px; color:#3A3A3A; float:left;\">"+json_d[i]['user']['screen_name']+" : "+ json_d[i]['full_text'] + "</p><br><br><p align=\"left\" style=\"font-size:20px; color:#3A3A3A; width:200px; margin-right:800px;\">  "+ str(json_d[i]['favorite_count']) +" Likes " + str(json_d[i]['retweet_count']) + " Retweets</p><p align=\"left\" style=\"font-size:20px; color:#3A3A3A; margin-right:840px;\">" +"<a href=\\tweets\search_res\\"+str(i)+"\\"+json_d[i]['user']['screen_name']+"\\"+json_d[i]['id_str']+">Replies</a>" +"</p></fieldset><br>"
                    list = json_d[i]['created_at'].split()
                    url = get_url(json_d[i]['full_text'])

                    if not json_d[i]['id'] in hash_list:
                        if json_d[i]['lang']=='en':
                            replies=get_replies(json_d[i]['id'],json_d[i]['user']['screen_name'])
                            toxic = get_tweet_sentiment(json_d[i]['full_text'])
                            Tweets(replies=replies,toxic=toxic,urls=url,no_followers=json_d[i]['user']["followers_count"],user_name=json_d[i]['user']['screen_name'],tweet_id=json_d[i]['id'],Lang=str(json_d[i]['lang']),Day_time_date=list[0] + " " + list[3] + " " + list[2] + "/" + list[1] + "/" + list[-1],Text=json_d[i]['full_text'],Fav_count=json_d[i]['favorite_count'],Ret_count=json_d[i]['retweet_count']).save()

                        elif json_d[i]['lang']=='hi' or 'gu':
                            replies = get_replies(json_d[i]['id'], json_d[i]['user']['screen_name'])
                            toxic=get_tweet_sentiment(translate(clean_tweet(json_d[i]['full_text']), "en", "auto"))
                            Tweets(replies=replies,toxic=toxic, urls=url, no_followers=json_d[i]['user']["followers_count"],user_name=json_d[i]['user']['screen_name'], tweet_id=json_d[i]['id'],Lang=str(json_d[i]['lang']),Day_time_date=list[0] + " " + list[3] + " " + list[2] + "/" + list[1] + "/" + list[-1], Text=json_d[i]['full_text'], Fav_count=json_d[i]['favorite_count'],Ret_count=json_d[i]['retweet_count']).save()

                else:
                    #print("else ",xcnt % 2)
                    url = ''

                    url=get_url(json_d[i]['full_text'])

                    x+="<fieldset style=\"width:900px; border-style: solid; border-width: 5; border-color:#3A3A3A;\"><legend style=\"margin-right:910px; color:#0084b4;\"><h3><b>" + str(i) + "</b></h3></legend><p align=\"left\" style=\"font-size:20px; color:#0084b4; float:left;\">" + json_d[i]['user']['screen_name'] + " : " + json_d[i]['full_text'] + "</p><br><br><p align=\"left\" style=\"font-size:20px; color:#0084b4; width:200px; margin-right:800px;\">  " + str(json_d[i]['favorite_count']) + " Likes " + str(json_d[i]['retweet_count']) + " Retweets</p><p align=\"left\" style=\"font-size:20px; color:#0084b4; margin-right:840px;\">" + "<a href=\\tweets\search_res\\" + str(i) + "\\" + json_d[i]['user']['screen_name'] + "\\" + json_d[i]['id_str'] + ">Replies</a>" + "</p></fieldset><br>"
                    list = json_d[i]['created_at'].split()
                    if not json_d[i]['id'] in hash_list:
                        if json_d[i]['lang']=='en':
                            replies = get_replies(json_d[i]['id'], json_d[i]['user']['screen_name'])
                            toxic = get_tweet_sentiment(json_d[i]['full_text'])
                            Tweets(replies=replies,toxic=toxic,urls=url,no_followers=json_d[i]['user']["followers_count"],user_name=json_d[i]['user']['screen_name'],tweet_id=json_d[i]['id'],Lang=str(json_d[i]['lang']),Day_time_date=list[0] + " " + list[3] + " " + list[2] + "/" + list[1] + "/" + list[-1],Text=json_d[i]['full_text'],Fav_count=json_d[i]['favorite_count'],Ret_count=json_d[i]['retweet_count']).save()

                        elif json_d[i]['lang']=='hi' or 'gu':
                            replies = get_replies(json_d[i]['id'], json_d[i]['user']['screen_name'])
                            toxic=get_tweet_sentiment(translate(clean_tweet(json_d[i]['full_text']), "en", "auto"))
                            Tweets(replies=replies,toxic=toxic, urls=url, no_followers=json_d[i]['user']["followers_count"],user_name=json_d[i]['user']['screen_name'], tweet_id=json_d[i]['id'],Lang=str(json_d[i]['lang']),Day_time_date=list[0] + " " + list[3] + " " + list[2] + "/" + list[1] + "/" + list[-1], Text=json_d[i]['full_text'], Fav_count=json_d[i]['favorite_count'],Ret_count=json_d[i]['retweet_count']).save()
                xcnt+=1
            message+=x
        else:message+="<h2 align=center style=color:#3A3A3A;>No tweets of a hashtag</h2>"


    else:
        message = "<script>alert('Empty');</script>"

    return HttpResponse("<br/><h1 align=center style=color:#3A3A3A;>Tweets</h1><br/><br/><br/></div>")



def reply_result(request):
    messege=""
    id=(str(request.get_full_path()).split('/'))[-1]
    name=(str(request.get_full_path()).split('/'))[-2]
    try:replies=tweepy.Cursor(api.search, q=name ,since_id=int(id), tweet_mode='extended').items()
    except:print("error")
    if replies:
        x="<fieldset style=\"width:900px; border-style: solid; border-width: 5; border-color:#0084b4;\"><legend style=\"margin-right:910px; color:#3A3A3A;\"><h3><b>Replies</b></h3></legend><p align=\"left\" style=\"font-size:20px; color:#3A3A3A; float:left;\">"
        for r in replies:
            if r._json["in_reply_to_status_id"] == int(id):
                x+=r._json['user']['screen_name']
                x+=" : "
                x+=r._json['full_text']
                x+="<br/><br/>"
                flag=1
            else:flag=0
    else:messege+="<h2 align=center style=color:#3A3A3A;>No replies of this Tweet</h2>"
    if flag : messege+=x
    else: messege+="<h2 align=center style=color:#3A3A3A;>No replies of this Tweet</h2>"

    return HttpResponse("<div align=center><h1 align=center style=color:#3A3A3A;>Replies</h1><br/><br/><br/>"+messege+"</p></fieldset></div>")




