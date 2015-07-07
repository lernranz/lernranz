#!/usr/bin/python3

import datetime
import gzip
import io
import json
from pathlib import Path
import re
import sys

def parse_aps(json_data):
    for building in json_data:
        for ap in building['aps']:
            ap['building'] = building['building']
            yield ap

def utc_mstimestamp(dt):
    return int((dt - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds() * 1000)


aps = {}
roomsSpec = json.load(open('rooms.json'))
roomFiles= {}
for room in roomsSpec:
    for ap in room['aps']:
        aps[ap] = room['name']
    parsedFilePath = 'parsed/' + room['id'] + '.json'
    if Path(parsedFilePath).is_file():
        pass
    parsedData = [{'label': 'Nutzer', 'values': []}]
    roomFiles[room['name']] = {'filename': parsedFilePath, 'file': parsedData}


p = Path('.')
files = list(p.glob('raw/*.json.gz'))
files.sort()
threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7) # ideally 7 days

for f in files:
    date_str = re.sub(
            r"^raw/(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)([+-]\d+):(\d+).json.gz$",
            r"\1-\2-\3T\4:\5:\6\7\8",
            str(f))
    date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    if (date < threshold):
        continue

    roomCounts = {}
    for room in roomsSpec:
        roomCounts[room['name']] = 0

    decompressed = gzip.open(str(f), mode='r')
    parsed = json.load(io.TextIOWrapper(decompressed))
    for ap in parse_aps(parsed['data']):
        if ap['name'] in aps:
            roomCounts[aps[ap['name']]] += int(ap['user'])

    for room in roomsSpec:
        roomFiles[room['name']]['file'][0]['values'].append({
            'x': utc_mstimestamp(date),
            'y': roomCounts[room['name']]})

    print(str(date) + ' ' + str(roomCounts))

    #sys.exit()

parsedDir = Path('parsed')
if not parsedDir.is_dir():
    parsedDir.mkdir()
for room in roomsSpec:
    import pprint
    #pprint.pprint(roomFiles[room['name']]['file'])
    json.dump(roomFiles[room['name']]['file'], open(roomFiles[room['name']]['filename'], mode='w'))


