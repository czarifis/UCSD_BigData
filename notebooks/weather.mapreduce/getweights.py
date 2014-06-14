#!/usr/bin/python
"""
count the number of measurements for each base-station
"""
import sys
sys.path.append('/usr/lib/python2.6/dist-packages')
from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol
from mrjob.step import MRStep
import re
from sys import stderr

class MRWeather(MRJob):
    '''
        The mapper outputs tuples of the form (station_name, "number_of_TMAX_measurements~number_of_TMIN_measurements")
    '''
    def mapper(self, _, line):
        try:
            self.increment_counter('MrJob Counters','mapper-all',1)
            elements=line.split(',')
            if elements[0]=='station':
                
                # if the header is spotted add it, it's not going to matter
                # since no base-station with name: 'header' exists, so when we do the
                # inner join this will be pruned
                
                out=('header','0~0')
                yield out
            else:
                if elements[1]=='TMAX':
                    
                    # Uncomment that to get measurements from a specific year.
                    #if elements[2]=='1973':
                        
                        out=(elements[0],str(len(filter(None, elements[3:])))+'~'+str(0))
                        yield out
                elif elements[1]=='TMIN':
                    
                    # Uncomment that to get measurements from a specific year.
                    #if elements[2]=='1973':
                        
                        out=(elements[0],str(0)+'~'+str(len(filter(None, elements[3:]))))
                        yield out
                
        except Exception, e:
            #stderr.write('Error in line:\n'+line)
            #stderr.write(e)
            self.increment_counter('MrJob Counters','mapper-error',1)
            
            # Again... This will be pruned when we do the inner join later...
            
            out=('error','0~0')
            yield out

        
    '''
        The combiner outputs tuples of the form (station_name, "number_of_TMAX_measurements~number_of_TMIN_measurements")
    '''  
    def combiner(self, station, vals):
        try:
            self.increment_counter('MrJob Counters','combiner',1)
            maxs=[]
            mins=[]
            for val in vals:
                #sys.stderr.write('tuple of max min for basestation: '+station+': '+str(x)+','+str(y)+'\n')
                elements=val.split('~')
                x = elements[0]
                y = elements[1]
                #sys.stderr.write('tuple of max min for basestation: '+station+': '+str(x)+','+str(y)+'\n')
                maxs.append(int(x))
                mins.append(int(y))
                #sys.stderr.write(str(x))
                #yield (station, 1)
            summax = sum(maxs)
            summin = sum(mins)
            #sys.stderr.write('number of max measurements: '+str(summax)+' number of min measurements: '+str(summin)+'\n')
            out = (station,(str(summax)+'~'+str(summin)))
            #sys.stderr.write(str(out)+'\n')
            yield out
        except Exception, e:
            # It never gets here, but better be safe than sorry
            #stderr.write('Error in line:\n'+station+", "+maxmin)
            #stderr.write(e)
            out=('error2','0~0')
            yield out
           
        
    '''
        The reducer outputs tuples of the form (station_name, "number_of_TMAX_measurements~number_of_TMIN_measurements")
    ''' 
    def reducer(self, station, vals):
        #try:
            self.increment_counter('MrJob Counters','reducer',1)
            maxs=[]
            mins=[]
            for val in vals:
                elements=val.split('~')
                x = elements[0]
                y = elements[1]
                maxs.append(int(x))
                mins.append(int(y))
            summax = sum(maxs)
            summin = sum(mins)
            #sys.stderr.write('number of max measurements: '+str(summax)+' number of min measurements: '+str(summin)+'\n')
            out = (station,(str(summax)+'~'+str(summin)))
            #sys.stderr.write(str(out)+'\n')
            yield out
        #except Exception, e:
            #stderr.write('Error in line:\n'+str(station)+', '+str(maxmin))
            #stderr.write(e)
            


if __name__ == '__main__':
    MRWeather.run()