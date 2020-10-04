import mysql.connector
import json
from twython import Twython
from datetime import datetime

#####################################

# this is the code that runs every hour
# and uploads from database according to
# current time and date

#####################################


# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# database'e bağlanır
mydb = mysql.connector.connect(
    host="YOUR HOST",
    user="YOUR USER",
    password="YOUR PASS",
    database="YOURDATABASE"
)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'], creds['ACCESS_TOKEN'],creds['ACCESS_SECRET'])

#time control
cdate = str(datetime.today().date())
chour = str(datetime.today().hour)
print("Current Date: " + str(cdate))
mycursor = mydb.cursor()

tweet = ""

mycursor.execute("SELECT tweet FROM tweets WHERE tarih = '%s' AND saat = '%s'" % (cdate,chour))
for x in mycursor:
    tweet = x

tweet_str = str(tweet[0])
print(tweet_str)
if len(tweet) > 0 :
    print("Bugüne ait veri var.")
    #python_tweets.update_status(status=tweet_str)
    print("Tweet paylasildi. Basarili.")
else:
    print("Bugüne ait veri bulunamadı. ")




