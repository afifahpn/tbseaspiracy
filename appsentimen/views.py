from django.shortcuts import render
# Create your views here.
import tweepy
import re
from textblob import TextBlob
import nltk
import io
import base64
import urllib.parse
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

from wordcloud import WordCloud

# Create your views here.
#nltk.download("stopwords")
def index(request):
    return render(request, 'index.html')

def result(request):
    if request.method == 'POST' :
        api_key = "CtenrKYqJVYs5IBJE2oDzJlGb"
        api_secret_key = "7xHJQcUbg7yIF4MVeWN4j1fH5lhKxvUbRxDrXEP6sS6vfqJCqr"
        access_token = "191385549-6IyBW85c8ZFXnYNez2iYuxxqzTUEBChdrnYvVwg5"
        access_token_secret = "LtQhH6zeCGBWcXpis6cD6r8DaxOydHcX2ChQ55BWkIjxl"

        #load api
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        tweetsSeaspiracy = api.search(q="Seaspiracy"+ "-filter:retweets "+" -filter:replies", lang="id")
        show = list()
        word = []
        #percent = list()
        for tweets in tweetsSeaspiracy:
            tweet_properties = {}
            tweet_pro = {}
            #persen = {}
            tweetext = tweets.text
            #tweet_pro["tweet kotor"] = tweetext
            #remove punctuation
            tweet_bersih = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweetext).split())
            #tweet_pro["tweet_bersih"] = tweet_bersih
            #case folding
            t = tweet_bersih.lower()
            tweet_pro["lower"] = t
            word.append(t)
            tweet_properties["isi_tweet"] = tweetext
            #tokenization
            analysis = TextBlob(t)
            tokenize = analysis.words
            #tweet_pro["tokenize"] = tokenize
            #stop words removal
            stop_words = [word for word in tokenize if word not in stopwords.words('indonesian')]
            #tweet_pro["stop_words"] = stop_words
            #print(stop_words)

            #detokenize
            detokenize = TreebankWordDetokenizer().detokenize(stop_words)
            tweet_pro["detokenize"] = detokenize
            #eng
            eng = TextBlob(detokenize)

            try:
                eng = eng.translate(to='en')
            except Exception as e:
                pass
            #tweet_pro["eng"] = eng
           #print(tweet_pro)
            tweet_properties["polarity"] = eng.sentiment.polarity
            tweet_properties["subjectivity"] = eng.sentiment.subjectivity
            if eng.sentiment.polarity > 0.0:
                tweet_properties["sentimen"] = "positif"
            elif eng.sentiment.polarity == 0.0:
                tweet_properties["sentimen"] = "netral"
            else :
                tweet_properties["sentimen"] = "negatif"
            show.append(tweet_properties)
        #wordcloud
        allWords = ' '.join([twts for twts in word])
        wordCloud = WordCloud(colormap="gray", width=1600, height=800, random_state=30, max_font_size=200, min_font_size=20).generate(allWords)
        plt.figure(figsize=(20,10), facecolor='k')
        plt.imshow(wordCloud, interpolation="bilinear")
        plt.axis('off')
        image = io.BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)
        string = base64.b64encode(image.read())
        image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)

        tweet_positif = [t for t in show if t["sentimen"] == "positif"]
        tweet_netral = [t for t in show if t["sentimen"] == "netral"]
        tweet_negatif = [t for t in show if t["sentimen"] == "negatif"]
        positif = len(tweet_positif)
        netral = len(tweet_netral)
        negatif = len(tweet_negatif)
            #percent.append(persen)
        #pie chart
        s = len(show)
        ppositif = 100*len(tweet_positif)/s
        pnetral = 100*len(tweet_netral)/s
        pnegatif = 100*len(tweet_negatif)/s

        labels = ['Positif', 'Negatif', 'Netral']
        sizes=[ppositif, pnegatif, pnetral]
        #explode = (0.1, 0)
        fig1, ax1 = plt.subplots()
        colors=['yellowgreen','red','silver']
        ax1.pie(sizes, labels=labels,  colors=colors, startangle=90, autopct='%1.2f%%')
        ax1.axis("equal")
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        strng = base64.b64encode(img.read())
        img_64 = 'data:image/png;base64,' + urllib.parse.quote(strng)

        context = {
            'hasil' : show,
            'positif' : positif,
            'netral' : netral,
            'negatif' : negatif,
            'jumlah' : s,
            'image' : image_64,
            'pie' : img_64
        }
        return render(request, 'result.html', context=context)

def about(request):
    return render(request, 'about.html')