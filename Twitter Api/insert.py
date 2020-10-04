import json
from twython import Twython
from datetime import datetime, timedelta
import mysql.connector
import csv


############################################################

# This code helps you connect to a database and add all the
# lines from the Quotes.csv according to their related time
# and date. It starts from the current date and increments
# the hour and date. The point is to create a database that
# is checkable 24/7.

############################################################



# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# Instantiate an object
# We pull the data from the json file
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'], creds['ACCESS_TOKEN'],creds['ACCESS_SECRET'])

mydb = mysql.connector.connect(
    host="YOUR HOST",
    user="YOUR USER",
    password="YOUR PASS",
    database="YOURDATABASE"
)
controller = 0
tweets = []

with open('quotes_Life.csv', newline='', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        controller += 1
        if len(row['Quote']) <= 255 :
            #print(str(controller) + ". " + row['Quote'])
            tweets.append(row['Quote'])
        else:
            next(reader)
        if controller == 53810:
            break


print(len(tweets))

#4 günlük tweet ekleme yeri
date = datetime.today().date() + timedelta(days=1)
mycursor = mydb.cursor()
hour = 0
for t in range(0,len(tweets)):
    sql = "INSERT INTO tweets (tarih , tweet , saat) VALUES (%s, %s, %s)"
    val = (date, tweets[t], hour)
    mycursor.execute(sql, val)
    mydb.commit()
    #print(str(hour)+ ".hour <<" + str(t) + ">> " +str(date) +" "+tweets[t]  )
    hour += 1
    #print("1 row inserted.")
    if hour ==24:
        hour = 0
        date += timedelta(days=1)
        print("24 records inserted. Date: " + str(date))




print(mycursor.rowcount, " TOTAL record inserted.")