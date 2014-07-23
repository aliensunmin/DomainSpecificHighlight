# these functions are used to download all video in a list of vlist.json with in one folder
import sys, os, subprocess, json, time, warnings, shutil

# requirement
# need to install youtube-dl (http://rg3.github.io/youtube-dl/)

# default settings:
YOUTUBEPREFIX = 'http://www.youtube.com/watch?v='
MISSINGVIDS = 'missingVideos'

# starting poit
def getAllVlist(baseDir,Filename='vlist.json'):
    # find all vlist.json files within baseDir
    # then, download all videos in all vlist.json files
    flist = getFileList(baseDir,Filename)
    N = len(flist)
    missVids = []
    for n in range(N):
        vlist = loadJson(flist[n])
        subBaseDir = os.path.dirname(flist[n])
        print "proc %s folder" % subBaseDir
        missVids.extend(getVideosGivenVlist(vlist,subBaseDir))
    # print our for record
    M = len(missVids)
    for m in range(M):
        if m == 0:
            print >> sys.stderr, "missing_vid"
        vid = os.path.basename(missVids[m])
        cacheF = baseDir + os.sep + MISSINGVIDS + os.sep + vid
        if not os.path.exists(cacheF):
            print >> sys.stderr, missVids[m]
            continue
        f = open(cacheF, 'r')
        cacheVid = f.readline().strip('\n')
        print cacheVid
        out = getTargetVideo(missVids[m],cacheVid)
        if out is None:
            print "fail to recover  %s from %s" %(vid,cacheVid)
            print >> sys.stderr, missVids[m]
        else:
            print "recover %s from %s" %(vid,cacheVid)
            souF = missVids[m] + os.sep + cacheVid + '.mp4'
            tarF = missVids[m] + os.sep + vid + '.mp4'
            shutil.move(souF,tarF)        
    return missVids

def getVideosGivenVlist(vlist,baseDir):
    N = len(vlist)
    missVids = []
    for n in range(N):
        M = len(vlist[n][0])
        for m in range(M):
            vid = vlist[n][0][m]
            vpath = baseDir+os.sep+vid
            out = getTargetVideo(vpath,vid)
            if out is None:
                missVids.append(vpath)
    return missVids

# utilities
def getFileList(folder,searchkey):
    cmd = "find %s -maxdepth 2 -mindepth 2 -name '%s'" % (folder, searchkey)
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    FileList = [] 
    for line in out.stdout:
        FileList.append(line.strip())
    return FileList

def loadJson(File):
    fp = open(File,"r");
    data = json.load(fp)
    fp.close()
    return data

def getTargetVideo(vpath,videoid,format=""):
    # vpath: the relative path to save downloaded video
    # videoid: youtube videoid for indexing the video
    # format: specify the format, if empty string, use format with highest quality 
    videoF = "%s" % vpath + os.sep+ "%s.mp4"% videoid
    if not os.path.exists(videoF):
        cmd = "youtube-dl -o %s " % videoF + YOUTUBEPREFIX+ "%s" % videoid
        print cmd
        if format != "":
            cmd = cmd + " --format %s" % format
        for i in range(5):
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if len(err) == 0:
                    break
            elif err.find('private') != -1:
                    break
            time.sleep(2)
        if len(err) != 0:
            #print "%s" %videoid
            #print err
            return None
    return videoF

if __name__ == "__main__":
    getAllVlist(sys.argv[1])
