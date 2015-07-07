#!/bin/sh

filename="/home/clonejo/web/rwth-wifi/`date "+%FT%H:%M:%S%:z"`.json"
if curl -sS "http://netstatus.rz.rwth-aachen.de/wlan/map/getinfo.php?type=all" -o $filename
then
	gzip $filename
else
	rm -f $filename
fi
