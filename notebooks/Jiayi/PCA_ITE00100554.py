#!/usr/bin/python
"""
count the number of measurements of each type
"""
import sys
sys.path.append('/usr/lib/python2.6/dist-packages')
from mrjob.job import MRJob
import re
import numpy as np
from sys import stderr

class PCA_ITE00100554(MRJob):

    def mapper(self, _, line):
        try:
            self.increment_counter('MrJob Counters','mapper',1)
            # Parse the line
            elements=line.split(',')
            station = elements[0]
            measure_type = elements[1]
            year = int(elements[2])
            measurements = elements[2:]
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
            if (measure_type == 'TMAX')\
                and "ITE00100" in station and len(measurements)==366 and nomeas>=366 and AllNum: 
                self.increment_counter('MrJob Counters','usefull lines',1)
                yield (station, measurements)
                
        except Exception, e:
            stderr.write('Error in line:\n'+line)
            stderr.write(e.message)
            self.increment_counter('MrJob Counters','mapper-error',1)
            yield (('error','mapper', str(e)), 1)
            
    def reducer(self, station, measurements):
        try:
            if station[0] == 'error':
                yield(station,sum(data))
                return
            self.increment_counter('MrJob Counters','reducer',1)
            
            sumvec=np.zeros(365)
            matr=np.zeros((365,365))
            
            number_Year=0
            data={}
            year={}

            for vector in measurements:
                strvec=vector[1:]
                numvec=[int(ss) for ss in strvec]
                data[number_Year]=numvec
                year[number_Year]=int(vector[0])
                number_Year = number_Year + 1
            
            for t in range(0,number_Year):
                sumvec=sumvec+np.array(data[t])
                
            sumlis=sumvec.tolist()
            meanlis=[float(n)/number_Year for n in sumlis]
            
            for t in range(0,number_Year):
                subtarr=np.array(data[t])-np.array(meanlis)
                matr+=np.outer(subtarr,subtarr)
                
            matr=np.divide(matr,number_Year)
            U,D,V=np.linalg.svd(matr)
            varexp=[]
            ptvar=0
            ttvar=sum(D)
            for n in range(0,365):
                ptvar+=D[n]
                if ptvar/ttvar>0.90:
                    break
                    
            k=20
#Eigenvalues:    
            Eig=np.matrix(U[:,:k])
            for t in range(0,number_Year):
                if 1890 <= year[t] and year[t] <= 1900:                    
                    subtarr=np.array(data[t])-np.array(meanlis)  
                    nbs = np.inner(subtarr,subtarr)
                    for i in range(0,k):
                        eigvec =np.array(Eig)[:,i]
                        subtarr = subtarr - np.inner(eigvec,subtarr)*eigvec
                        if i % 5 ==0:
                            yield(i, np.inner(subtarr,subtarr)/nbs)
           # matr+=np.outer(subtarr,subtarr)
           # matrix=np.matrix(measurements.ix[:,1:365])#-Mean
           # Prod=matrix*Eig;
                        
            yield(station,n)
        except Exception, e:
            #yield (('error','reducer', str(e)), 1)
            stderr.write('Error in reducer')
        
if __name__ == '__main__':
    PCA_ITE00100554.run()