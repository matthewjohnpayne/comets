import os, sys
import numpy as np
import glob

# Directories, etc
comet_dir = "/sa/incoming/cmt/"
cmt_dir = os.path.join(comet_dir, "cmt")


# Functions
def process_single_cmt(obs_file):
    print(obs_file)
    
def process_cmt():
    ''' Process all submissions in /sa/incoming/cmt/cmt '''
    
    # Get all obs files
    obs_file_list = glob.glob(cmt_dir + "/*.obs")
    
    # Process each obs file
    for obs_file in obs_file_list:
        process_single_cmt(obs_file)
        
    # Do any tidying-up
    
    return True
    
    
if __name__ == '__main__':
    # If called from the command-line, do /cmt/cmt directory
    # In the future could allow for options to call other routines, e.g. pct ...
    process_cmt()
