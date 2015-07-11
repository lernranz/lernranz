#!/bin/sh

filename="/home/lernranz/raw/`date "+%FT%H:%M:%S%:z"`.json"
if curl -sS "http://netstatus.rz.rwth-aachen.de/wlan/map/getinfo.php?type=all" -o $filename
then
    gzip $filename
    cd /var/www/lernranz
    ./parse.py >/dev/null
else
    rm -f $filename
fi
