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

class get_mean_diff_prcp(MRJob):

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
                yield (station, [year,measure_type,np.mean(np.array(usefulmeas))])
                
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
            mean_temp=[]
            diff_temp=[]
            mean_PRCP=[]
            for key in dic_TMIN:
                if dic_TMAX.has_key(key) and dic_PRCP.has_key(key):
                    ma=dic_TMAX[key]
                    mi=dic_TMIN[key]
                    pr=dic_PRCP[key]
                    validyear.append(key)
                    mean_temp.append(round((ma+mi)/2.0,3))
                    diff_temp.append(round(ma-mi,3))
                    mean_PRCP.append(round(pr,3))
            if len(validyear)>=100 and max(validyear)>2006:
                yield(station, [validyear, mean_temp, diff_temp, mean_PRCP])
#                 out=[np.mean(np.array(mean_TMIN)), np.mean(np.array(mean_TMAX)), \
#                      np.mean(np.array(mean_TMAX))-np.mean(np.array(mean_TMIN)), np.mean(np.array(mean_PRCP)),\
#                      np.mean(np.array(std_TMIN)),np.mean(np.array(std_TMAX)),np.mean(np.array(std_PRCP))]
#                 yield (station, out)
#             else:
#                 yield (station, [9999,9999,9999,9999,9999,9999,9999])
        except Exception, e:
            #yield (('error','reducer', str(e)), 1)
            stderr.write('Error in reducer')
        
if __name__ == '__main__':
    get_mean_diff_prcp.run()