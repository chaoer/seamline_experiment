# -*- coding: utf-8 -*-
"""
Script Name: Count the mosaicing time for OrthoMaker from it's log file
Description: 
    The log file contains every process of OrthoMaker. (our approache)
    Generally, the process contains:
    a. color balancing, 
    b. dense image matching,
    c. dem generation,
    d. ortho rectification,
    e. image dodging,
    f. and image mosaicing.
    
    We will count the time of: 
        f. image mosaicing
                
Created on Mar. 28 18:56:29 2018

@author: Chaoer
"""

import sys
import re
import math
from datetime import datetime

def parse_time(time_str):
    # parse time str in format: 2017-02-13 15:23:17
    # print (re.split('[- :]', time_str))
    y, mon, d, h, m, s  = re.split('[- :]', time_str)
    
    se = int(math.floor(float(s)))
    milse = int(float(s) * 1000 - se * 1000)
    
    return datetime(int(y), int(mon), int(d), int(h), int(m), se, milse)
    
    
def count_time(log_file_path):
    file = open(log_file_path, "r")
    
    time_st_str = ""
    time_ed_str = ""
    
    for line in file:
        if line.find("Smart Mosaic Begin") != -1:
            time_st_str = line.split(":", 1)[1].strip()
        if line.find("Smart Mosaic End") != -1:
            time_ed_str = line.split(":", 1)[1].strip()
        if line.find("End Time") != -1:
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
