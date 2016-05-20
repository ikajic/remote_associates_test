"""
Read the spreadsheets in ./data/ and return the following
information:
    a) the number of normed words (counting yes)
    b) a pickled file named: free_association_vocabulary

The pickled file contains (in the order):
    1. idtow dictionary: mapping between word ids and words
    2. wtoid dictionary: mapping between words and word ids
    3. numpy array (csr_matrix): cue x responses association strength matrix
"""
from __future__ import division
from scipy.sparse import csr_matrix

import numpy as np
import matplotlib.pyplot as pl
import pandas as pd
import cPickle as pickle
import os

# directory with the spreadsheets
datapath = os.path.join(os.path.dirname(__file__), 'data')

wtoid = dict()      # word to index dictionary
idtow = dict()      # index to word dictionary
normed = 0          # count the number of normed words (should be 5018)

database = ()
cues = set()
words = set()

dir_files = os.listdir(datapath)

# there should be 8 sheets of data
sheet_name_pref = 'Cue_Target_'
nr_sheets = np.array([sheet_name_pref in name for name in dir_files])
assert nr_sheets.sum() == 8,\
    'Found %d sheets: download them!' % nr_sheets.sum()

# first get all the data from the sheets and store it in a 'database'
for filename in dir_files:
    # read in the sheet
    datafile = os.path.join(datapath, filename)

    # skip everything that is not a spreadsheet
    if 'Cue_Target_' not in filename:
        continue

    # read the contents of the spreadsheet
    print 'Processing: ', filename
    df = pd.read_csv(datafile, skipinitialspace=True, skiprows=3, skipfooter=3)
    normed += df['NORMED?'].value_counts()['YES']

    # extract norms
    for i in range(len(df)):
        row = df.irow(i)

        # skip unnormed data
        if row['NORMED?'] == 'NO':
            continue

        cue, target = row['CUE'].lower(), row['TARGET'].lower()
        cues.add(cue)

        words.add(cue)
        words.add(target)

        # extract forward-strength
        try:
            fsg = np.float(row['FSG'])
        except ValueError:
            fsg = .0

        try:
            bsg = np.float(row['BSG'])
        except ValueError:
            bsg = .0

        database += ((cue, target, fsg, bsg), )

ids = np.arange(len(words))     # create a unique id for every word

# fill the dictionaries with eiter words or ids as keys
wtoid.update(zip(words, ids))
idtow.update(zip(ids, words))
nr_words = len(wtoid)

# make sure all ids are unique
assert len(np.unique(idtow.values())) == len(wtoid)

print 'Number of normed words (should be 5019):', len(wtoid)
print 'Number of normed responses (should be 63619):', normed

# then create a connection matrix based on the entries in the database
conn_mat = np.zeros((nr_words, nr_words))

for cue, target, fsg, bsg in database:
    cue_id, target_id = wtoid[cue], wtoid[target]
    conn_mat[cue_id, target_id] += fsg
    # conn_mat[target_id, cue_id] += bsg

# count the deviation for the avg nr of associates
nr_assoc_row = np.zeros(nr_words)

for i, row in enumerate(conn_mat):
    nr_assoc_row[i] = len(np.nonzero(row)[0])

print 'Average number of associates per word:',\
    normed/nr_words, nr_assoc_row.std()

# save the connection matrix and the vocabularies
# path = '../../processed/'
path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,
        'processed', 'free_associations_vocabulary')
resp = raw_input('Save the data to ' + path + '? [y/n] ')

if resp in 'yY':
    print 'Saving the vocabularies and the connection matrix...'
    f = open(path, 'wb')
    pickle.dump(idtow, f, protocol=2)
    pickle.dump(wtoid, f, protocol=2)

    sparse_mat = csr_matrix(conn_mat)

    pickle.dump(sparse_mat, f)
    f.close()
    print 'Done.'

# if desired, plot the data
if 0:
    pl.figure()
    pl.hist(nr_assoc_row, bins=int(nr_assoc_row.max()))
    pl.xlabel('Number of associates')
    pl.ylabel('Number of words in the database')
    pl.savefig('fa_word_distr.pdf', bbox_inches='tight')

    pl.show()
