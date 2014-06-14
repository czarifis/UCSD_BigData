#!/usr/bin/python
"""
count the number of measurements of each type
"""
import sys
import numpy as np
sys.path.append('/usr/lib/python2.6/dist-packages')
from mrjob.job import MRJob
import re
from sys import stderr

class get_mean_diff_std_year(MRJob):

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
            usefulmeas=[]
            for ss in measurements:
                if ss!="":
                    try:
                        ii=float(ss)
                        usefulmeas.append(ii)
                        nomeas+=1
                    except:
                        AllNum=False
            #filter out the unwanted measurements and the header line
            if (measure_type == 'TMIN' or measure_type == 'TMAX' or measure_type=='PRCP') \
                and station != 'station' and len(measurements)==365 and nomeas>=300 and AllNum: 
                self.increment_counter('MrJob Counters','usefull lines',1)
                yield (station, [year,measure_type,usefulmeas])
                
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
            mean_TMIN=[]
            mean_TMAX=[]
            mean_PRCP=[]
            std_TMIN=[]
            std_TMAX=[]
            std_PRCP=[]
            for key in dic_TMIN:
                if dic_TMAX.has_key(key) and dic_PRCP.has_key(key):
                    validyear.append(key)
                    mean_TMIN.append(np.mean(np.array(dic_TMIN[key])))
                    mean_TMAX.append(np.mean(np.array(dic_TMAX[key])))
                    mean_PRCP.append(np.mean(np.array(dic_PRCP[key])))
                    std_TMIN.append(np.std(np.array(dic_TMIN[key])))
                    std_TMAX.append(np.std(np.array(dic_TMAX[key])))
                    std_PRCP.append(np.std(np.array(dic_PRCP[key])))
            if len(validyear)>100:
                yield (station, [validyear,mean_TMIN,mean_TMAX])
            #else:
            #    yield (station, _)
        except Exception, e:
            #yield (('error','reducer', str(e)), 1)
            stderr.write('Error in reducer')
        
if __name__ == '__main__':
    get_mean_diff_std_year.run()