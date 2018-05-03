#!/usr/bin/env python

#=============================================================================
# Created by Kirstie Whitaker
# at Hot Numbers coffee shop on Trumpington Road in Cambridge, September 2016
# Contact: kw401@cam.ac.uk
#=============================================================================

#=============================================================================
# IMPORTS
#=============================================================================
from __future__ import print_function # Making code python 2 and 3 compatible

import os
import sys
import argparse
import textwrap

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts/'))
import make_corr_matrices as mcm
from useful_functions import read_in_data

#=============================================================================
# FUNCTIONS
#=============================================================================
def setup_argparser():
    '''
    Code to read in arguments from the command line
    Also allows you to change some settings
    '''
    # Build a basic parser.
    help_text = (('Generate a structural correlation matrix from an input csv file,\n')+
                 ('a list of region names and (optional) covariates.'))

    sign_off = 'Author: Kirstie Whitaker <kw401@cam.ac.uk>'

    parser = argparse.ArgumentParser(description=help_text,
                                     epilog=sign_off,
                                     formatter_class=argparse.RawTextHelpFormatter)

    # Now add the arguments
    parser.add_argument(dest='regional_measures_file',
                            type=str,
                            metavar='regional_measures_file',
                            help=textwrap.dedent(('CSV file that contains regional values for each participant.\n')+
                                                 ('Column labels should be the region names or covariate variable\n')+
                                                 ('names. All participants in the file will be included in the\n')+
                                                 ('correlation matrix.')))

    parser.add_argument(dest='names_file',
                            type=str,
                            metavar='names_file',
                            help=textwrap.dedent(('Text file that contains the names of each region to be included\n')+
                                                 ('in the correlation matrix. One region name on each line.')))

    parser.add_argument(dest='output_name',
                            type=str,
                            metavar='output_name',
                            help=textwrap.dedent(('File name of the output correlation matrix.\n')+
                                                 ('If the output directory does not yet exist it will be created.')))

    parser.add_argument('--covars_file',
                            type=str,
                            metavar='covars_file',
                            help=textwrap.dedent(('Text file that contains the names of variables that should be\n')+
                                                 ('covaried for each regional measure before the creation of the\n')+
                                                 ('correlation matrix. One variable name on each line.\n')+
                                                 ('  Default: None')),
                            default=None)

    parser.add_argument('--names_308_style',
                            action='store_true',
                            help=textwrap.dedent(('Include this flag if your names are in the NSPN 308\n')+
                                                 ('parcellation style (which means you have 41 subcortical regions)\n')+
                                                 ('that are still in the names files and that\n')+
                                                 ('the names are in <hemi>_<DK-region>_<part> format.\n')+
                                                 ('  Default: False')),
                            default=False)

    arguments = parser.parse_args()

    return arguments, parser


def corrmat_from_regionalmeasures(regional_measures_file,
                                  names_file,
                                  output_name,
                                  covars_file=None,
                                  names_308_style=False,
                                  method='pearson'):
    '''
    This is the big function!
    It reads in the CSV file that contains the regional measures for each
    participant, the names file and the list of covariates.
    Then it creates the correlation matrix and writes it out to the output_dir
    as a txt file.
    '''
    # Read in the data
    df, names, covars_list = read_in_data(regional_measures_file,
                                                names_file,
                                                covars_file=covars_file,
                                                names_308_style=names_308_style)
    
    # Correct for your covariates
    df_res = mcm.create_residuals_df(df, names, covars_list)

    # Make your correlation matrix
    M = mcm.create_corrmat(df_res, names, method=method).values

    # Save the matrix
    mcm.save_mat(M, output_name)



if __name__ == "__main__":

    # Read in the command line arguments
    arg, parser = setup_argparser()

    # Now run the main function :)
    corrmat_from_regionalmeasures(arg.regional_measures_file,
                                      arg.names_file,
                                      arg.output_name,
                                      covars_file=arg.covars_file,
                                      names_308_style=arg.names_308_style)

#=============================================================================
# Wooo! All done :)
#=============================================================================
