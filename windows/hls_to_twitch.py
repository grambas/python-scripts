# ! python
import os, sys, urllib, traceback, time, signal, multiprocessing
from time import gmtime, strftime
from subprocess import Popen, PIPE, call
import httplib2
import json
import requests

def record():
    #interval = 43200 # 12h
    interval =3600    
    SRC = 'http://...........playlist.m3u8'

    while True:
        video_time =  time.strftime("%B%d_%H-%M", time.localtime())
        video_title = '"' + time.strftime("%B %d %H:%M", time.localtime())
        path_and_file = "videos/" + video_time + ".flv"

        cmd = ['ffmpeg',
                 '-hide_banner',
                 '-i',
                 SRC,
                 '-vcodec', 'copy',
                 '-acodec', 'aac','-strict', '-2',
                 '-crf' ,'20',
                 '-f', 'flv',
                 '-b:a', '128k',
                 path_and_file,
        ]

        cmd_str = ' '.join(cmd)

        print("Interval=  " + str(interval))
        print("Calling  " + cmd_str)
        print("Capturing stream to " + str(path_and_file))

        p = Popen(cmd_str, shell=True)
        time.sleep(interval)

        print("Sleep interval "+ str(interval)+ " is done. now killing process " + str(p.pid))

        #kill all ffmpeg processes
        pkill("ffmpeg")
        title = video_title + time.strftime(" - %H:%M", time.localtime()) + '"'

        call(["py", "twitchUpload.py", title, path_and_file])

def pkill (process_name):
    try:
        killed = os.system('tskill ' + process_name)
    except Exception:
        killed = 0
    return killed

def main(argv):
    print ("FFMPEG python script started...")
    record()
    #print "starting recording: "
    #print strftime("%Y-%m-%d %H:%M:%S", gmtime())

if __name__ == "__main__":
    main(sys.argv)
