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
        stderr.write(line+'\n')

if __name__ == '__main__':
    MRWeather.run()