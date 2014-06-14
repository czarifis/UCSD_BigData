#!/usr/bin/python
"""
count the number of measurements of each type
"""
import sys
sys.path.append('/usr/lib/python2.6/dist-packages')
from mrjob.job import MRJob
import re
from sys import stderr

class count_validyear(MRJob):

    def mapper(self, _, line):
        try:
            self.increment_counter('MrJob Counters','mapper',1)
            # Parse the line
            elements=line.split(',')
            station = elements[0]
            measure_type = elements[1]
            year = int(elements[2])
            measurements = elements[3:]
            nomeas = 0
            #
            AllNum=True
            for ss in measurements:
                if ss!="":
                    try:
                        ii=float(ss)
                        nomeas+=1
                    except:
                        AllNum=False
            #filter out the unwanted measurements and the header line
            if (measure_type == 'TMIN' or measure_type == 'TMAX' or measure_type=='PRCP') \
                and station != 'station' and len(measurements)==365 and nomeas>=200 and AllNum: 
                self.increment_counter('MrJob Counters','usefull lines',1)
                yield (station, [year,measure_type,nomeas])
                
        except Exception, e:
            stderr.write('Error in line:\n'+line)
            stderr.write(e.message)
            self.increment_counter('MrJob Counters','mapper-error',1)
            yield (('error','mapper', str(e)), 1)
            
    def reducer(self, station, counts):
        try:
            if station[0] == 'error':
                yield(station,sum(data))
                return
            self.increment_counter('MrJob Counters','reducer',1)
            dic_TMIN={}
            dic_TMAX={}
            dic_PRCP={}
            for vec in counts:
                if vec[1]=='TMIN':
                    dic_TMIN[vec[0]]=vec[2]
                elif vec[1]=='TMAX':
                    dic_TMAX[vec[0]]=vec[2]
                else:
                    dic_PRCP[vec[0]]=vec[2]
            validyear=[]
            for key in dic_TMIN:
                if dic_TMAX.has_key(key) and dic_PRCP.has_key(key):
                    validyear.append(key)
            yield (station, len(validyear))
        except Exception, e:
            #yield (('error','reducer', str(e)), 1)
            stderr.write('Error in reducer')
        
if __name__ == '__main__':
    count_validyear.run()