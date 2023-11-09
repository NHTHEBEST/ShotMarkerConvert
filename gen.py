#!/usr/bin/python3
import tarfile, zlib, json, sys
from os import path,mkdir


file = "SM_export_Nov_05.tar"


def getsdatafromtar(filename):
    with tarfile.open(filename) as tf:
        archive = tf.getmember('archive.txt')
        archive = tf.extractfile(archive)
        archive = archive.read()
        archive = json.loads(archive)
        archive = list(archive)
        output = []
        for run in archive:
            f = "string-"+str(run)+".z"
            f = tf.getmember(f)
            f = tf.extractfile(f)
            f = f.read()
            f = zlib.decompress(f)
            f = json.loads(f)
            output.append(f)
        return output
    
def dict2csv(data):
    out = []
    for f in data:
        file = "shot_x, shot_y, shot_v, shot_temp, score, txt\r\n"
        fname = f['name'] + "_" + f['face_id'] + "_" + str(f['ts']) + ".csv"
        print(fname)
        shots = f['shots']
        for shot in shots:
            file += str(shot['x']) + ',' + str(shot['y'])+ ',' +  str(shot['v'])+ ',' +  str(shot['temp'])+ ',' +  str(shot['score'])+ ',' +  str(shot['display_text']) + '\r\n'
        out.append((fname, file))
    return out

def savefiles(data, dir = 'csv'):
    mkdir(dir)
    for file in data:
        fname = path.join(dir,file[0])
        f = open(fname,'w')
        f.write(file[1])
        f.close()

if len(sys.argv) != 1:
    file = sys.argv[1]

data = getsdatafromtar(file)

files = dict2csv(data)

savefiles(files)



