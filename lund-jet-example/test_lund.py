# !/usr/bin/env python3
#
# Frederic Dreyer, BOOST 2018 tutorial
#
# Load a keras model and apply it to sample a of W and dijet images,
# then plot the results.
#
# Usage:
#   python3 test_lund.py [--sig file_sig]       [--bkg file_bkg]
#                        [--threshold treshold] [--nev nevents]
#                        [--model file_model]
#

import keras
from create_image import LundImage
from matplotlib.colors import LogNorm
import numpy as np
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser(description='Plot lund images')
parser.add_argument('--sig', action='store',
                    default='W-lund-pt2000-parton.json.gz',
                    dest='file_sig')
parser.add_argument('--bkg', action='store',
                    default='dijet-lund-pt2000-parton.json.gz',
                    dest='file_bkg')
parser.add_argument('--model', action='store',
                    default='W_Conv_Net_lund_pt2000-parton.h5',
                    dest='file_model')
parser.add_argument('--nev', type=int, default=2000, dest='nev')
parser.add_argument('--treshold', type=float, default=0.5, dest='tresh')

args = parser.parse_args()

# set up the readers
sig_reader = LundImage(args.file_sig, args.nev, 50)
bkg_reader = LundImage(args.file_bkg, args.nev, 50)

# get array from file
print('# Reading images from file')
sig_images = np.array(sig_reader.values())[:,0]
bkg_images = np.array(bkg_reader.values())[:,0]
images = np.zeros((len(sig_images)+len(bkg_images),1,50,50))
images[:len(bkg_images),0,:,:] = bkg_images
images[len(bkg_images):,0,:,:] = sig_images

# create labels
labels = np.concatenate((np.zeros(len(bkg_images)),np.ones(len(sig_images))))
labels = np.asarray([[1 if x == n else 0 for n in range(2)] for x in labels])

# load the keras model and evaluate on images
print('# Loading keras model')
model = keras.models.load_model(args.file_model)
print('# Evaluating model on data sample')
sig_prob = model.predict(images, verbose=0)[:,1]


# prepare plotting of results
print('# Plotting results')
fig=plt.figure(figsize=(14, 11))

# plot the signal lund images
sig_tag     = images[sig_prob<args.tresh]
sig_avg_img = np.transpose(np.average(sig_images,axis=0))
sig_tag_avg = np.transpose(np.average(sig_tag[:,0,:,:],axis=0))
fig.add_subplot(2,2,1)
plt.title('Lund image (W) - truth')
plt.xlabel('$\ln(R / \Delta)$')
plt.ylabel('$\ln(k_t / \mathrm{GeV})$')
plt.imshow(sig_avg_img, origin='lower',
           aspect='auto', extent=[0,7,-3,7], cmap=plt.get_cmap('BuPu'),
           vmax=0.005,vmin=0.0)
plt.colorbar()

fig.add_subplot(2,2,2)
plt.title('Lund image (W) - tagged')
plt.xlabel('$\ln(R / \Delta)$')
plt.ylabel('$\ln(k_t / \mathrm{GeV})$')
plt.imshow(sig_tag_avg, origin='lower',
           aspect='auto', extent=[0,7,-3,7], cmap=plt.get_cmap('BuPu'),
           vmax=0.005,vmin=0.0)
plt.colorbar()


# plot the background lund images
bkg_tag     = images[sig_prob>args.tresh]
bkg_avg_img = np.transpose(np.average(bkg_images,axis=0))
bkg_tag_avg = np.transpose(np.average(bkg_tag[:,0,:,:],axis=0))
fig.add_subplot(2,2,3)
plt.title('Lund image (QCD) - truth')
plt.xlabel('$\ln(R / \Delta)$')
plt.ylabel('$\ln(k_t / \mathrm{GeV})$')
plt.imshow(bkg_avg_img, origin='lower',
           aspect='auto', extent=[0,7,-3,7], cmap=plt.get_cmap('BuPu'),
           vmax=0.005,vmin=0.0)
plt.colorbar()

fig.add_subplot(2,2,4)
plt.title('Lund image (QCD) - tagged')
plt.xlabel('$\ln(R / \Delta)$')
plt.ylabel('$\ln(k_t / \mathrm{GeV})$')
plt.imshow(bkg_tag_avg, origin='lower',
           aspect='auto', extent=[0,7,-3,7], cmap=plt.get_cmap('BuPu'),
           vmax=0.005,vmin=0.0)
plt.colorbar()
plt.show()
