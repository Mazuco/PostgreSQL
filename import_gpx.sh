#!/bin/bash

# Zip path
ZIPFILE="runkeeper-gpx.zip"
WORKDIR="gpx_tmp"

# Creates temporary directory and cleans if it already exists
rm -rf "$WORKDIR"
mkdir "$WORKDIR"

# Extract all GPX from zip
unzip -j "$ZIPFILE" "*.gpx" -d "$WORKDIR"

# Loop through the extracted GPX files
for f in "$WORKDIR"/*.gpx; do
    echo "Importing $f into gpsrun.rk_track_points..."

    ogr2ogr -append -update \
        -f PostgreSQL PG:"dbname='geodb' user='postgres' password='123456'" \
        "$f" \
        -nln gpsrun.rk_track_points \
        -sql "SELECT ele, time FROM track_points"
done

# (optional) remove temporaries
rm -rf "$WORKDIR"

