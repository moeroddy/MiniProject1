import tweepy
import json
import urllib.request #to extract the picture from the URL
import os 
import subprocess
import argparse
from google.cloud import videointelligence
import io
import os.path
import sys
import urllib.request
import urllib.error
import json
import subprocess
from datetime import datetime
from sys import platform
from creds import *






user_id = "CardfghgfdPicsDepot"
tweet_counts = 20

url = ''
num = 0
videoPath = os.getcwd()+"\out.mp4"
googleAuthName = ""
pathToAuthGoogle = os.getcwd()
 

def checkPlatformAndAuthGoogle():
    if platform == "linux" or platform == "linux2":
        print("platform is linux")
        os.system("export GOOGLE_APPLICATION_CREDENTIALS=" + pathToAuthGoogle )
    elif platform == "darwin":
        print("Platform is OSX")
        os.system("export GOOGLE_APPLICATION_CREDENTIALS=" + pathToAuthGoogle )
    elif platform == "win32":
        print("Platform is windows")
        os.system("set GOOGLE_APPLICATION_CREDENTIALS=" + pathToAuthGoogle )

def isInt(value):
    try:
        int(value)
        return True
    except: 
        return False


def isTweetNumBound(value):
    if int(value) > 100 and int(value) < 1:
        print("Please enter a number between 0 and 100!!")
        return False
    else:
        return True

def inputInfo():
    global user_id
    global tweet_counts
    global googleAuthName
    global pathToAuthGoogle

    user_id = input("What is the twitter screen name ? example: CarPicsDepot  => ")

    while not checkUser(user_id):
        user_id = input("What is the twitter screen name ? example: CarPicsDepot  => ")



    tweet_counts = input("How Many tweet you wanna retrieve ? max is 100 => ")

    while isInt(tweet_counts) == False:
        print("Please Enter a valid number!!")
        tweet_counts = input("How Many tweet you wanna retrieve ? max is 100 => ")

    while isTweetNumBound(tweet_counts) == False:
        print("please enter a number between 0 and 100!!")
        tweet_counts = input("How Many tweet you wanna retrieve ? max is 100 => ")

    googleAuthName = input("What is the name of the json auth file for google ? example: google.json => ")
    pathToAuthGoogle = pathToAuthGoogle + "\\" + googleAuthName






def checkUser(user_id):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        user = api.get_user(user_id)
        print("User ID number is : " + user.id_str)
        print("User screen name is : " + user.screen_name)
        return True
    except Exception:
        print("user is not found")
        pass


def tweep(consumer_key, consumer_secret, access_token, access_token_secret, url, num, user_id, tweet_counts):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    public_tweets = api.user_timeline(user_id, since_id=2, count=tweet_counts)
    print(public_tweets)    
    for tweet in public_tweets: 
        if 'media' in tweet._json['entities']:
            url = tweet._json['entities']['media'][0]["media_url"]
            print("Image" + str(num))
            print(url)
            urllib.request.urlretrieve(url, "img" + str(num) + ".jpg")
            num = num + 1

def checkFFmpeg():
    #check if FFmpeg is installed or not
    try:
        subprocess.call("ffmpeg -version")
    except OSError:
        print ("FFmpeg is either not installed or not added to the path, please install ffmpeg and rerun the program")


def makeVideo():
    os.system("ffmpeg -r 1/10 -i img%00d.jpg -c:v libx264 -pix_fmt yuv420p -vf scale=320:240 out.mp4")


def checkVid(path):
    #check if the video exists or not
    if (os.path.isfile(path)):
        print("File out.mp4 exists")
    else:
        print("File video not found")
        sys.exit()


def analyze_labels(path):
    """Detect labels given a file path."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]

    with io.open(path, 'rb') as movie:
        input_content = movie.read()

    operation = video_client.annotate_video(
        features=features, input_content=input_content)
    print('\nProcessing video for label annotations:')

    result = operation.result(timeout=300)
    print('\nFinished processing.')

    # Process video/segment level label annotations
    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print('Video label description: {}'.format(
            segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print('\tLabel category description: {}'.format(
                category_entity.description))

        for i, segment in enumerate(segment_label.segments):
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.nanos / 1e9)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            confidence = segment.confidence
            print('\tSegment {}: {}'.format(i, positions))
            print('\tConfidence: {}'.format(confidence))
        print('\n')

    # Process shot level label annotations
    shot_labels = result.annotation_results[0].shot_label_annotations
    for i, shot_label in enumerate(shot_labels):
        print('Shot label description: {}'.format(
            shot_label.entity.description))
        for category_entity in shot_label.category_entities:
            print('\tLabel category description: {}'.format(
                category_entity.description))

        for i, shot in enumerate(shot_label.segments):
            start_time = (shot.segment.start_time_offset.seconds +
                          shot.segment.start_time_offset.nanos / 1e9)
            end_time = (shot.segment.end_time_offset.seconds +
                        shot.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            confidence = shot.confidence
            print('\tSegment {}: {}'.format(i, positions))
            print('\tConfidence: {}'.format(confidence))
        print('\n')

    # Process frame level label annotations
    frame_labels = result.annotation_results[0].frame_label_annotations
    for i, frame_label in enumerate(frame_labels):
        print('Frame label description: {}'.format(
            frame_label.entity.description))
        for category_entity in frame_label.category_entities:
            print('\tLabel category description: {}'.format(
                category_entity.description))

        # Each frame_label_annotation has many frames,
        # here we print information only about the first frame.
        frame = frame_label.frames[0]
        time_offset = frame.time_offset.seconds + frame.time_offset.nanos / 1e9
        print('\tFirst frame time offset: {}s'.format(time_offset))
        print('\tFirst frame confidence: {}'.format(frame.confidence))
        print('\n')


inputInfo()
tweep(consumer_key, consumer_secret, access_token, access_token_secret, url, num, user_id, tweet_counts)
checkFFmpeg()
makeVideo()
checkVid(videoPath)
print("************************************************************")
print("************************************************************")
print("************************************************************")
print("************************************************************")
checkPlatformAndAuthGoogle()
analyze_labels(videoPath)
