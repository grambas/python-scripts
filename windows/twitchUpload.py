# ! python
import os, sys, urllib, time, signal, multiprocessing
from time import gmtime, strftime
from subprocess import Popen, PIPE
import httplib2
import json
import requests

TWITCH_VERSION_HEADER = "application/vnd.twitchtv.v5+json"
CHUNKSIZE = 10 * 1024 * 1024 # 10MB chunk size for video parts

#TO FILL
TOKEN = "XXXXXXX"
TWITCH_CLIENT_ID = "XXXXXXX"
USER_ID = "XXXXXX"

def get_channel_name(twitch_auth_token):
    url = 'https://api.twitch.tv/kraken/user'
    headers = {'Authorization': 'OAuth ' + twitch_auth_token,
             'Accept': TWITCH_VERSION_HEADER,
             'Client-ID': TWITCH_CLIENT_ID }  
    r = requests.get(url, headers=headers)
    user = r.json()
    #print user
    return user['name']

def create_twitch_video(title, description, tags, twitch_auth_token):

    print ('Creating video on Twitch... with title' + str(title))
    url = 'https://api.twitch.tv/kraken/videos'
    payload = {'channel_name': get_channel_name(twitch_auth_token),
               'channel_id': USER_ID,
               'title': title,
               'description': description,
               'tags': tags }   
    headers = {'Authorization': 'OAuth ' + twitch_auth_token,
               'Accept': TWITCH_VERSION_HEADER,
               'Client-ID': TWITCH_CLIENT_ID,
               'channel_id': USER_ID,
               'Content-Type': 'application/json' }
    r = requests.post(url, json=payload, headers=headers)
    video = r.json()
    print (video)
    return video["upload"]["url"], video["upload"]["token"]

def upload_to_twitch(filename, upload_url, upload_token):
    print(filename)
    print(upload_url)
    print(upload_token)
    print ("Uploading " + filename + " to Twitch via " + upload_url + ", " + str(CHUNKSIZE) + " bytes at a time..." )

    file = open(filename, 'rb')
    index = 0
    while 1:
      chunk = file.read(CHUNKSIZE)
      if not chunk: break
      index += 1
      headers = {'Accept': TWITCH_VERSION_HEADER,
                 'Client-ID': TWITCH_CLIENT_ID,
                 'Content-Length': str(len(chunk)) }
      params = {'part': index,
                 'upload_token': upload_token }
      r = requests.put(upload_url, params=params, data=chunk, headers=headers)
      print ('Completed uploading part ' + str(index))
    file.close()

    headers = {'Accept': TWITCH_VERSION_HEADER,
               'Client-ID': TWITCH_CLIENT_ID }
    params = {'upload_token': upload_token }
    r = requests.post(upload_url + '/complete', params=params, headers=headers)
    print ("DONE!!!!!!!!!")
    return


def main(argv):
    print 
    upload_url, upload_token = create_twitch_video(sys.argv[1], "VIDEO_DESCRIPTION", "VIDEO_TAGS", TOKEN)
    upload_to_twitch(sys.argv[2], upload_url, upload_token)
    #os.remove(sys.argv[2])

if __name__ == "__main__":
    main(sys.argv)

