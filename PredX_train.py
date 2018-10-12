from __future__ import print_function

import pickle as pkl
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
import sys, gc
import PredX_MPNN as MPNN
import sparse

# hyper-parameters
data = 'QM9' #'COD' or 'QM9'

import argparse
parser = argparse.ArgumentParser(description='Train student network')

parser.add_argument('--dec', type=str, default='mpnn', choices=['mpnn','npe','none'])
parser.add_argument('--save_dir', type=str, default='./checkpoints/')
parser.add_argument('--alignment-type', type=str, default='kabsch', choices=['default','linear','kabsch'])

args = parser.parse_args()

if data == 'COD':

    n_max = 50
    dim_node = 33
    dim_edge = 15
    ntrn = 60000
    nval = 3000
    ntst = 3000

elif data == 'QM9':

    n_max = 9
    dim_node = 20
    dim_edge = 15
    ntrn = 100000
    nval = 5000
    ntst = 5000

dim_h = 50
dim_f = 100
batch_size = 20

load_path = None
save_path = args.save_dir+data+'_'+str(n_max)+'_'+str(args.dec)+'_model.ckpt'

print('::: load data')
[D1, D2, D3, D4, D5] = pkl.load(open('./'+data+'_molvec_'+str(n_max)+'.p','rb'))
D1 = D1.todense()
D2 = D2.todense()
D3 = D3.todense()

[molsup, molsmi] = pkl.load(open('./'+data+'_molset_'+str(n_max)+'.p','rb'))

D1_trn = D1[:ntrn]
D2_trn = D2[:ntrn]
D3_trn = D3[:ntrn]
D4_trn = D4[:ntrn]
D5_trn = D5[:ntrn]
molsup_trn =molsup[:ntrn]
D1_val = D1[ntrn:ntrn+nval]
D2_val = D2[ntrn:ntrn+nval]
D3_val = D3[ntrn:ntrn+nval]
D4_val = D4[ntrn:ntrn+nval]
D5_val = D5[ntrn:ntrn+nval]
molsup_val =molsup[ntrn:ntrn+nval]
D1_tst = D1[ntrn+nval:ntrn+nval+ntst]
D2_tst = D2[ntrn+nval:ntrn+nval+ntst]
D3_tst = D3[ntrn+nval:ntrn+nval+ntst]
D4_tst = D4[ntrn+nval:ntrn+nval+ntst]
D5_tst = D5[ntrn+nval:ntrn+nval+ntst]
molsup_tst =molsup[ntrn+nval:ntrn+nval+ntst]

del D1, D2, D3, D4, D5, molsup

model = MPNN.Model(data, n_max, dim_node, dim_edge, dim_h, dim_f, batch_size, args.dec, args.alignment_type)
with model.sess:
    model.train(D1_trn, D2_trn, D3_trn, D4_trn, D5_trn, molsup_trn, D1_val, D2_val, D3_val, D4_val, D5_val, molsup_val, load_path, save_path)
    #model.saver.restore( model.sess, save_path )
