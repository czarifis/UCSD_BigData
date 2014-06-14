#!/usr/bin/python
"""
count the number of measurements for each base-station
"""
import sys
import pandas as pd
import numpy as np
import sklearn as sk
sys.path.append('/usr/lib/python2.6/dist-packages')
from mrjob.job import MRJob
from mrjob.step import MRStep
import re
from sys import stderr
import json

class maxminprcp(MRJob):
    
    def __init__(self, *args, **kwargs):
        super(maxminprcp, self).__init__(*args, **kwargs)
        self.data = {}
        
    

    def configure_options(self):
        super(maxminprcp, self).configure_options()

        

    def mapper(self, _, line):

        self.increment_counter('MrJob Counters','mapper-all',1)
        elements=line.split(',')
        if elements[0]=='station':
            out=('header','0~0')
        else:
            
            if elements[1]=='PRCP' or elements[1]=='TMAX' or elements[1]=='TMIN':
                x = elements[3:]                
                #sys.stderr.write(str(x))
                floats = [float(strr) if strr else 0 for strr in x]

                #sys.stderr.write('mean is:\n')

            
                aa = [item for item in floats if item != 0]
                mmean = np.mean(aa)


                out=((elements[0]),(elements[1],elements[2], mmean))#+'~'+str(0))
                #sys.stderr.write('printing\n')
                #sys.stderr.write(str(out))
                
                    #sys.stderr.write(str(out))
                yield out

        self.increment_counter('MrJob Counters','mapper-error',1)
            
            # Again... This would be pruned when we would do the inner join later so let's ommit it right away...
            
            
            ################################################################################################################
            # NOTE! Since I could not run the HWPART1 step on the cluster I run it locally and used a smaller dataset      #
            # with TMAX measurements instead. So the basestations included in the ALL.head and the SAMPLE_TMAX are not     #
            # the same... Just use the same file for both Part1 and Part 2                                                 #
            ################################################################################################################
        #   out=('error','0~0')
            #yield out

        
#     def combiner(self, station, vals):
#         yield (0,0)
        
    def reducer(self, station, vals):

        self.increment_counter('MrJob Counters','reducer',1)
        #sys.stderr.write('base-station name is: '+str(station)+'\n')
        valArr = []
       
        #from collections import defaultdict
        d = {}#defaultdict(list)
        for val in vals: 

            a = val[0]
            b = val[1]
            c = val[2]

            if b in d:
                d[b][a] = c
            else:
                d[b] = {}
                d[b][a] = c
        #sys.stderr.write(str(d))

        for k,v in d.iteritems():               # will become d.items() in py3k
          
#             sys.stderr.write('\n')
#             sys.stderr.write('len: ')
#             sys.stderr.write(str(len(v)))
            if len(v)==3:
#                 sys.stderr.write('\n')
#                 sys.stderr.write((str(k)+'-'+str(v)))
#                 sys.stderr.write('\n')
                out = ((station,k,v['TMAX'],v['TMIN'],v['PRCP']), None)
                
#                 sys.stderr.write(str(out))
                yield out
                


if __name__ == '__main__':
    maxminprcp.run()