import os, sys
import numpy as np
import glob

# import local
sys.path.insert(0,'/share/apps/orbit_utils/')
import comet_orbits
import mpc_new_processing_sub_directory as newsub

# Directories, etc
comet_dir = "/sa/incoming/cmt/"
cmt_dir = os.path.join(comet_dir, "cmt")


# Functions
def process_single_cmt(cmt_desig , tmp_obs_file, directory):
    ''' Process a single (temp) file from /sa/incoming/cmt/cmt that will contain only obs of a single comet'''
    print(cmt_desig , tmp_obs_file , directory)
    
    # Run a fit on the temp file
    # python3 /sa/orbit_utils/comet_orbits.py CK21A040 --add_obsfile /sa/incoming/cmt/cmt/2021-03-14T00:41:31.001_0000E5vL.obs --orbit N
    """
    arg_parser.add_argument('cmt_desig', help="Provide comet MPC packed designation")
    arg_parser.add_argument('--trksub', dest='trksub', help='Is it a trksub? Y=Yes, N=No', default='N')
    arg_parser.add_argument('--obsfile', dest='obsfile', help="Observations file to use (file name, DB for database, ades for ADES format)",default='DB')
    arg_parser.add_argument('--orbit', dest='orbit', help="Preliminary orbit to be used (Y=Yes, N=No or file name)",default='Y')
    arg_parser.add_argument('--frag', dest='frag', help="Fragment (Y=yes,N=No)", default='N')
    arg_parser.add_argument('--t_std', dest='t_std', help="Current epoch", default=59200.)
    arg_parser.add_argument('--nongravs', dest='nongrav', help="Non-gravitational perturbations",choices=['Y','N'],default='N')
    arg_parser.add_argument('--model', dest='model', help="Non-gravs model: 1=Marsden1973, 2=Yeomans&Chodas, 3=Yabushita", default='1')
    arg_parser.add_argument('--params', dest='params', help="Non-gravs parameters, 1=A1,A2; 2=A1,A2,A3; 3=A1,A2,A3,DT",default='1')
    arg_parser.add_argument('--firstobs', dest='firstobs', help="First observation to be used (YYYY/MM/DD)",default='0000/00/00')
    arg_parser.add_argument('--lastobs', dest='lastobs', help="Last observation to be used (YYYY/MM/DD)",default='0000/00/00')
    arg_parser.add_argument('--a1ng', dest='a1ng', help='A1 non-gravs if you want to detect DT', default='0.')
    arg_parser.add_argument('--a2ng', dest='a2ng', help='A2 non-gravs if you want to detect DT', default='0.')
    arg_parser.add_argument('--a3ng', dest='a3ng', help='A3 non-gravs if you want to detect DT', default='0.')
    arg_parser.add_argument('--add_obsfile', dest='addobs', help='Add observation file to the obs in the DB', default='N')
    arg_parser.add_argument('--directory', dest='directory', help="Directory to be used", default='N')
    """
    comet_orbits.main(cmt_desig,'N','DB','N','N',59200.,'N','N','1','0000/00/00','0000/00/00','0.','0.','0.',tmp_obs_file,directory)
    sys.exit()
    return {}

def process_submission(obs_file):
    ''' Process a single submission file from /sa/incoming/cmt/cmt '''
    submission_fit_dict = {}
    
    # Read the contents of the file
    with open(obs_file, 'r') as fh:
        data = fh.readlines()
    
    # Extract the desig(s) of the comets in the file
    desigs = [ _[:13].strip() for _ in data]
    
    
    # There may be multiple objects in a file ...
    # ... so just process object-by-object
    for n, desig in enumerate(list(set(desigs))):
    
        # Do we want to do any kind of check on the desigs?
        
        # Set up the tmp-proc-dir
        proc_dir = newsub.generate_subdirectory( 'comets' )

        # Set up a temp file name
        tmp_obs_file = os.path.join(sub_dir , obs_file.split("/")[0] , str(n) )
        print("tmp_obs_file", tmp_obs_file)
        sys.exit()
        # Open temp file to allow us to write to it
        with open(tmp_obs_file, 'w') as fh:
        
            # Print matching lines to the file
            for n,d in enumerate(desigs):
                if d == desig:
                    fh.write(data[n])
                    
        # Run fit
        submission_fit_dict[desig] = process_single_cmt(tmp_obs_file)
            
        # Tidy-up
        if os.path.isfile(tmp_obs_file):
            os.remove(tmp_obs_file)
        

    return submission_fit_dict
  
def summarize_processing( fit_dict) :
    ''' Provides a summary of the processing done on submissions in /sa/incoming/cmt/cmt '''
    routine         = list(fit_dict.keys())[0]
    fit_dict        = fit_dict[routine]
    n_submissions   = len(fit_dict)
    # *** ADD IN MORE TO DESCRIBE SUCCESS/FAILURE ONCE I KNOW WHAT THE OUTPUT LOOKS LIKE ***
    
    for _ in [  f"Routine: {routine}",
                f"Number of submissions: {n_submissions}",
                ]:
        print(_)
  
def process_cmt():
    ''' Process all submissions in /sa/incoming/cmt/cmt '''
    cmt_fit_dict = {}
    
    # Get all obs files
    obs_file_list = glob.glob(cmt_dir + "/*.obs")
    
    # Process each obs file
    for obs_file in obs_file_list:
        cmt_fit_dict[obs_file] = process_submission(obs_file)
        sys.exit()
        
    # Summarize the result
    summarize_processing( {"process_cmt" : cmt_fit_dict} )

    return True
    
    
if __name__ == '__main__':
    # If called from the command-line, do /cmt/cmt directory
    # In the future could allow for options to call other routines, e.g. pct ...
    process_cmt()
