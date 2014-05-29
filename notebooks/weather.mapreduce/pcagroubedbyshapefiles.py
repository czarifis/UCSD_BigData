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

class pcagroubedby(MRJob):
    
    def __init__(self, *args, **kwargs):
        super(pcagroubedby, self).__init__(*args, **kwargs)
        self.data = {}
        
    

    def configure_options(self):
        super(pcagroubedby, self).configure_options()
        self.add_file_option('--hashmap')
        self.add_file_option('--usemeasurement')

    def mapper_init(self):
        json_data=open(self.options.hashmap)
        self.meas = self.options.usemeasurement
        self.data = json.load(json_data)
        #sys.stderr.write('loaded: '+str(self.meas))
        #sys.stderr.write(str(data))
        json_data.close()
        # make dictionary available to mapper
        #sys.stderr.write('MAPPER_INIT!!')
        #sys.stderr.write(str(self.options.hashmap))
        
        #self.sqlite_conn = sqlite3.connect(self.options.database)
    def mapper(self, _, line):
#         for key in self.data:
#             sys.stderr.write( key + ' corresponds to'+ str(self.data[key])+'\n')

        try:
            self.increment_counter('MrJob Counters','mapper-all',1)
            elements=line.split(',')
            if elements[0]=='station':
                
                # if the header is spotted add it, it's not going to matter
                # since no base-station with name: 'header' exists, so when we do the
                # inner join this will be pruned
                
                out=('header','0~0')
                #yield out
            else:
                if elements[1]==self.meas:
                    #sys.stderr.write('YOLO')
                    
                    # Uncomment that to get measurements from a specific year.
                    #if elements[2]=='1973':
                        
                        # Use the following instead if you want to avoid null values
                        #out=(str(self.data[elements[0]]),str(filter(None,elements[3:])))#+'~'+str(0))
                        
                        out=(str(self.data[elements[0]]),(elements[3:]))#+'~'+str(0))
                        #sys.stderr.write(str(out))
                        yield out
#                 elif elements[1]=='TMAX':
                    
#                     # Uncomment that to get measurements from a specific year.
#                     #if elements[2]=='1973':
                        
                        
#                         out=(str(self.data[elements[0]]),'TMAX'+(elements[3:]))#+'~'+str(0))
#                         sys.stderr.write(str(out))
#                         yield out
        except Exception, e:

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
        
    def reducer(self, group, vals):

        self.increment_counter('MrJob Counters','reducer',1)
        #sys.stderr.write('group range is: '+str(group)+'\n')
        valArr = []
        
        for val in vals:
            #sys.stderr.write(str(val)+'\n')
            valArr.append(val)



        # Awesome! Let's use a Dataframe!
        ddtf = pd.DataFrame(valArr,columns = range(1,366))
        
        # Since we have a lot of empty values replace them with np.nan 
        # this is gonna make the processing easier
        
        ddtf = ddtf.replace('', np.nan)
        
        # Let's check out the measurements
        #sys.stderr.write(str(ddtf.head()))  # Checked!
        

        
        # switch the type of every element in the dataframe from an object to a float
        for listElem in list(ddtf.columns.values):
            #sys.stderr.write(str(listElem))
            ddtf[listElem] = ddtf[listElem].astype(float)#.fillna(0.0)
        
        
        # It should be float now
        # sys.stderr.write('\nddtf types: '+str(ddtf.dtypes))   # Yes it is!

        
        M=ddtf.loc[:,:].transpose()
        
        # check the shape of M
        #sys.stderr.write('\nM shape is: '+str(M.shape))
        
        M=M.dropna(axis=1)
        
        # check again after dropping the nan values
        #sys.stderr.write('\n M shape after droping NaNs is: '+str(np.shape(M)))
        
        (columns,rows)=np.shape(M)
        
        
        # Let's compute the covariance, (We could use np.cov instead...)
        if rows !=0:
            Mean=np.mean(M, axis=1).values


            C=np.zeros([columns,columns])   # Sum
            N=np.zeros([columns,columns])   # Counter of non-nan entries

            for i in range(rows):
                row=M.iloc[:,i]-Mean;
                outer=np.outer(row,row)
                valid=np.isnan(outer)==False
                C[valid]=C[valid]+outer[valid]  # update C with the valid location in outer
                N[valid]=N[valid]+1
            valid_outer=np.multiply(1-np.isnan(N),N>0)
            cov=np.divide(C,N)
#             cov2 = np.cov(M)
#             sys.stderr.write('\ncov is: \n'+str(cov)+'\ncov2 is: \n'+str(cov2))
#             for elem in cov:
#                 sys.stderr.write('\ncov is: \n'+str(elem))
#            sys.stderr.write('\nnp.sum(cov) : '+str(np.sum(cov)))
            summation = np.sum(cov)
            if summation!=0:
                U,D,V=np.linalg.svd(cov)
                #sys.stderr.write('\nyielding D')
                yield (group+str(rows),str(D))

                
        #else:
        #    sys.stderr.write('nothing to do here')

if __name__ == '__main__':
    pcagroubedby.run()