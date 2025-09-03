#!/bin/bash
mkdir -p rivers

for f in $(ogrinfo PG:"dbname='geodb' user='postgres' password='123456'" \
  -sql "SELECT DISTINCT iso_a2 FROM public.countries ORDER BY iso_a2" \
  | grep "iso_a2 (String)" | awk -F= '{print $2}' | tr -d ' ')
do 
    echo "Exporting river shapefile for $f country..."
    ogr2ogr rivers/rivers_$f.shp PG:"dbname='geodb' user='postgres' password='123456'" \
      -sql "SELECT * FROM public.rivers_clipped_by_country WHERE iso2 = '$f'"
done


