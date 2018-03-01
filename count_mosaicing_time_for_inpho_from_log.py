# -*- coding: utf-8 -*-
"""
Script Name: Count the mosaicing time for Inpho(OrthoVista) from it's log file
Description: 
    The log file contains every process of Inpho.
    Generally, the process contains:
    a. overview generation,
    b. image region calculation,
    c. seamline selection,
    d. seam polygon generation, 
    e. and overview generation of the final mosaic.
    
    We will count the time from:
        c. seamline selection to d. seam polygon generation
                
Created on Thu Nov  2 10:20:04 2017

@author: Chaoer
"""

import sys
import re
import math
from datetime import datetime

def parse_time(time_str):
    # parse time str in format: 2017-02-13 15:23:17.417
    # print (re.split('[- :]', time_str))
    y, mon, d, h, m, s, tmp  = re.split('[- :]', time_str)
    
    se = int(math.floor(float(s)))
    milse = int(float(s) * 1000 - se * 1000)
    
    return datetime(int(y), int(mon), int(d), int(h), int(m), se, milse)
    
    
def count_time(log_file_path):
    file = open(log_file_path, "r")
    
    time_st_str = ""
    time_ed_str = ""
    
    for line in file:
		if line.find("Mosaicking: got all input data, starting processing") != -1:
			time_st_str = line.split("---")[0]
		if line.find("Mosaicking: processing done") != -1:
			time_ed_str = line.split("---")[0]
		if line.find("Finished processing") != -1:
			break
			
    file.close()
    
    time_st = parse_time(time_st_str)
    time_ed = parse_time(time_ed_str)
    
    time_lapse = time_ed - time_st
    
    return time_lapse.seconds
    
    
def main():
    if len(sys.argv) != 2:
        print("Please specify the log file path.\n")
        sys.exit(-1)
        
    log_file_path = sys.argv[1]
    time_lapse = count_time(log_file_path)
    print ("log file: " + log_file_path)
    print ("cost: %.3f sec." % time_lapse)
    
if __name__ == '__main__':
    main()
