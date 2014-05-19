import os

import sys
# This hack makes sure tha the gdal lib can get imported
sys.path.append('/usr/lib/python2.7/dist-packages/')
from osgeo import gdal
import matplotlib.pyplot as plt
# GDAL does not use python exceptions by default
gdal.UseExceptions()



import osgeo.ogr
shapefile = osgeo.ogr.Open("/home/ubuntu/worldboarders/TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)
countries = [] # List of (code,name,minLat,maxLat,
          # minLong,maxLong) tuples.
geoms=[]

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    countryCode = feature.GetField("ISO3")
    countryName = feature.GetField("NAME")
    if countryName == 'Greece':
        Greece = feature.GetGeometryRef()
    geometry = feature.GetGeometryRef()
    geoms.append(geometry)
    minLong,maxLong,minLat,maxLat = geometry.GetEnvelope()
    countries.append((countryName, countryCode,
      minLat, maxLat, minLong, maxLong, geometry))
countries.sort()
#for name,code,minLat,maxLat,minLong,maxLong, geom in countries:


point = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
point.SetPoint(0, 29841677,33069868)
print 'point created'
print "Geometry has %i points" % (geoms[0].GetPointCount())

for geom in geoms:
    #if name == 'Greece':
    #   print 'found it!'

    if point.Within(geom):
        print 'ffs'

        #print Greece
        #GetGeometryRef().Contains(point):
        #if Greece.Contains(point):
        #    print 'YOLO'
        #else:
        #    print '!YOLO'
        
    #print "%s (%s) lat=%0.4f..%0.4f, long=%0.4f..%0.4f" \
#% (name, code,minLat, maxLat,minLong, maxLong)

#print Greece



