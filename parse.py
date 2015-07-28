#!/usr/bin/python3

from datetime import datetime,timedelta,timezone
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
    return int((dt - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1000)


date_now = datetime.now(timezone.utc)
threshold = date_now - timedelta(days=7) # ideally 7 days

aps = {}
roomsSpec = json.load(open('rooms.json'))
roomFiles= {}
last_parsed_date = threshold
for room in roomsSpec:
    for ap in room['aps']:
        aps[ap] = room['name']
    parsedFilePath = 'parsed/' + room['id'] + '.json'
    if Path(parsedFilePath).is_file():
        parsedData = json.load(open(parsedFilePath))
        parsedData[0]['values'] = [i for i in parsedData[0]['values']
                if threshold < datetime.fromtimestamp(i['x']/1000, tz=timezone.utc)]
        if len(parsedData[0]['values']) > 0:
            last_parsed_date = datetime.fromtimestamp(
                    parsedData[0]['values'][-1]['x']/1000,
                    tz=timezone.utc)
    else:
        parsedData = [{'label': 'Nutzer', 'values': []}]
    roomFiles[room['name']] = {'filename': parsedFilePath, 'file': parsedData}

print('last_parsed_date=' + str(last_parsed_date))

p = Path('.')
files = list(p.glob('raw/*.json.gz'))
files.sort()

lastDate = last_parsed_date
for f in files:
    date_str = re.sub(
            r"^raw/(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)([+-]\d+):(\d+).json.gz$",
            r"\1-\2-\3T\4:\5:\6\7\8",
            str(f))
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    if (date <= last_parsed_date):
        continue

    roomCounts = {}
    for room in roomsSpec:
        roomCounts[room['name']] = 0

    decompressed = gzip.open(str(f), mode='r')
    try:
        parsed = json.load(io.TextIOWrapper(decompressed))
    except ValueError:
        print('{0} is malformed json, renaming to {0}.broken'.format(str(f)))
        f.rename(str(f) + '.broken')
    for ap in parse_aps(parsed['data']):
        if ap['name'] in aps:
            roomCounts[aps[ap['name']]] += int(ap['user'])

    for room in roomsSpec:
        dead=False
        if (date-lastDate) > timedelta(hours=2):
            dead=True
        roomFiles[room['name']]['file'][0]['values'].append({
            'x': utc_mstimestamp(date),
            'y': roomCounts[room['name']],
            'dead': dead })

    print(str(date) + ' ' + str(roomCounts) + ' ' + str(dead))
    lastDate=date


    #sys.exit()

parsedDir = Path('parsed')
if not parsedDir.is_dir():
    parsedDir.mkdir()
for room in roomsSpec:
    import pprint
    #pprint.pprint(roomFiles[room['name']]['file'])
    json.dump(roomFiles[room['name']]['file'], open(roomFiles[room['name']]['filename'], mode='w'))


