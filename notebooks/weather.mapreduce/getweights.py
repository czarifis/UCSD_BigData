#!/usr/bin/python
"""
count the number of measurements of each type. 
"""
import sys
sys.path.append('/usr/lib/python2.6/dist-packages')
from mrjob.job import MRJob
import re
from sys import stderr

class MRWeather(MRJob):

    def mapper(self, _, line):
        #try:
            self.increment_counter('MrJob Counters','mapper-all',1)
            elements=line.split(',')
            if elements[0]=='station':
                out=('header',1)
                yield out
            else:
                if elements[1]=='TMAX':
                    #if elements[2]=='1973':
                        #stderr.write(len(filter("", elements[3:])))
                        
                        #sys.stderr.write(', '.join(len(filter(None, elements))))
                        #sys.stderr.write(str(len(filter(None, elements[3:]))))
                        #sys.stderr.write(' measurements out of '+str(len(elements[3:]))+' on basestation: '+elements[0]+'\n')
                        out=(elements[0],(str(len(filter(None, elements[3:]))),0))
                        yield out
                elif elements[1]=='TMIN':
                        out=(elements[0],(0,str(len(filter(None, elements[3:])))))
                        yield out
                
                
                #out=(elements[1],1)
                
        #except Exception, e:
        #    stderr.write('Error in line:\n'+line)
        #    stderr.write(e)
        #    self.increment_counter('MrJob Counters','mapper-error',1)
        #    out=('error',1)
        #    yield out

        #finally:
        #    yield out
        
        
    def combiner(self, station, maxmin):
        self.increment_counter('MrJob Counters','reducer',1)
        #sys.stderr.write('basestation: '+station+'\n')
        maxs=[]
        mins=[]
        for x,y in maxmin:
            #sys.stderr.write('tuple of max min for basestation: '+station+': '+str(x)+','+str(y)+'\n')
            maxs.append(int(x))
            mins.append(int(y))
            #sys.stderr.write(str(x))
            #yield (station, 1)
        summax = sum(maxs)
        summin = sum(mins)
        #sys.stderr.write('number of max measurements: '+str(summax)+' number of min measurements: '+str(summin)+'\n')
        yield (station,(summax,summin))
        
        

    def reducer(self, station, maxmin):
        self.increment_counter('MrJob Counters','reducer',1)
        #sys.stderr.write('basestation: '+station+'\n')
        maxs=[]
        mins=[]
        for x,y in maxmin:
            #sys.stderr.write('tuple of max min for basestation: '+station+': '+str(x)+','+str(y)+'\n')
            maxs.append(int(x))
            mins.append(int(y))
            #sys.stderr.write(str(x))
            #yield (station, 1)
        summax = sum(maxs)
        summin = sum(mins)
        #sys.stderr.write('number of max measurements: '+str(summax)+' number of min measurements: '+str(summin)+'\n')
        yield (station,(summax,summin))
        

if __name__ == '__main__':
    MRWeather.run()