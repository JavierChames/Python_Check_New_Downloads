import os.path
import time
print(os.getcwd())
locations={}
with open("paths.txt") as f:
    for line in f:
        (key, val) = line.split()
        locations[key] = val 

for value in locations.values():
    print("Created: %s" % time.ctime(os.path.getctime(value)))
