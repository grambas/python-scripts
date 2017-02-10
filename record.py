#! python
import time
import subprocess as sp, sys
import urllib


def record():
    sourcePath ='https://tv3sportozona.data.lt/2barai1/smil:2barai.smil/chunklist_w26425534_b1572864.m3u8'
    name = '_video.ts'

    destPath = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + name

    command = [ 'ffmpeg',
    '-y',  # (optional) overwrite output file if it exists
    '-hide_banner',
    '-loglevel', 'panic',
    '-i',
    sourcePath,
    '-vcodec', 'copy',
    '-acodec', 'copy',
    '-ss', '00:00:00.0',
    '-t', '01:00:00.0',
   # '-profile:v','high',
   # '-preset','slow',
   # '-threads', '2',
    destPath]

    returnExitCode = sp.call(command)

    if returnExitCode != 0:
        url_status = urllib.urlopen(sourcePath).getcode()
        if url_status != 200:
            print "Bad url response = " + str(url_status) + " Check source url"
        else:
            print  "Error in ffmpeg"
            print(returnExitCode)
        print "Waiting 10 seconds"
        time.sleep(10)
    else:
        print "ALL OK"
        # print(returnExitCode)

       # print(destPath)

 
def main(argv):
    print "Program started..."
    while True:
        record()

if __name__ == "__main__":
    main(sys.argv)
