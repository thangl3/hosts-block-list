import hashlib
import errno
import glob, os, shutil

tmpDir = 'tmp'
hostFileName = 'hosts'

if not os.path.exists(tmpDir):
  try:
    os.makedirs(tmpDir)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise

# merge files to the one
fileNames = glob.glob('source/*.txt')

with open(os.path.join(tmpDir, hostFileName), 'w') as outfile:
  for fName in fileNames:
    with open(fName) as infile:
      for line in infile:
        outfile.write(line)

print 'merge done!';

# filter
outputFilePath = hostFileName
inputFilePath = os.path.join(tmpDir, hostFileName)

scanCompletedLinesHashSet = set()

outputFile = open(outputFilePath, 'w')

for line in open(inputFilePath, 'r'):
  hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()

  if hashValue not in scanCompletedLinesHashSet:
    outputFile.write(line)
    scanCompletedLinesHashSet.add(hashValue)

outputFile.close()

print 'filter done!';

try:
  shutil.rmtree(tmpDir)
except OSError as e:
  print ("Error: %s - %s." % (e.filename, e.strerror))

print 'done!'
