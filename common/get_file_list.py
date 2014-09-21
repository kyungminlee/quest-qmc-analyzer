from __future__ import division
import os

import parser


__author__ = 'vladimir'


def get_filelist_temp(modelName, path):
    """
    Returns list of the files with time independent measurements
    """
    # get list of the filenames that have information that we need
    potential_files = []
    for fName in os.listdir(path):
        if modelName in fName:  #filter for the proper model
            if '.out' in fName:
                if 'tdm.out' not in fName:
                    potential_files += [os.path.join(path, fName)]
    return potential_files


def helper_function(fName, **kwargs):
    dimension = kwargs['dimension']
    toOpen_indep = open(fName)
    p = parser.Parser(toOpen_indep.read(), dimension=dimension)
    try:
        p.get_rho()
    except:
        print 'bad file = ', fName
        os.remove(fName)
    toOpen_indep.close()
    return p


def get_filelist(modelName, path, **kwargs):
    dimension = kwargs['dimension']
    return (helper_function(tx, dimension=dimension) for tx in get_filelist_temp(modelName, path))

