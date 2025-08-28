#!/bin/bash

for f in `find runkeeper_gpx -name \*.gpx `
do
    echo "Importing gpx file $f to gpsrun.rk_track_points PostGIS table..." #, ${f%.*}"
    ogr2ogr -append -update  -f PostgreSQL PG:"dbname='geodb' user='postgres' password='123456'" $f -nln gpsrun.rk_track_points -sql "SELECT ele, time FROM track_points"
done


