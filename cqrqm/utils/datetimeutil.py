#!/usr/bin/env python
import time

class Timer:
    def __init__(self):
	self.enabled=True

    def start(self):
        if self.enabled: 
		self.start_time=time.time()
    
    def end(self,msg):
        if self.enabled: 
		self.end_time=time.time()
       		elapsed_seconds= self.end_time - self.start_time
#       	elapsed_minutes= elapsed/60
        	print '[timer] it took %s seconds to %s' % (elapsed_seconds,msg)
        	elapsed_seconds=None
    
