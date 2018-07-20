# !/usr/bin/env python3
#
# Frederic Dreyer, BOOST 2018 tutorial
#
# Load two files of signal and background images, and plot them
#
# Usage:
#   python3 plot_lund.py [--sig file_sig] [--bkg file_bkg]
#                        [--nev nevents]  [--npxl npixels]
#

from create_image import LundImage
from matplotlib.colors import LogNorm
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Plot lund images')
parser.add_argument('--sig',action='store',
                    default='W-lund-pt2000-parton.json.gz',
                    dest='file_sig')
parser.add_argument('--bkg',action='store',
                    default='dijet-lund-pt2000-parton.json.gz',
                    dest='file_bkg')
parser.add_argument('--nev',  type=int, default=50000, dest='nev')
parser.add_argument('--npxl', type=int, default=25,    dest='npxl')

args = parser.parse_args()

# set up the readers
sig_reader = LundImage(args.file_sig, args.nev, args.npxl)
bkg_reader = LundImage(args.file_bkg, args.nev, args.npxl)

# get array from file
sig_images = np.array(sig_reader.values())[:,0]
bkg_images = np.array(bkg_reader.values())[:,0]

# plot average images
sig_avg_img = np.transpose(np.average(sig_images,axis=0))
bkg_avg_img = np.transpose(np.average(bkg_images,axis=0))
fig=plt.figure(figsize=(18, 4.5))

# signal
fig.add_subplot(1,3,1)
plt.title('Lund image (W)')
plt.xlabel('$\ln(R / \Delta)$')
plt.ylabel('$\ln(k_t / \mathrm{GeV})$')
plt.imshow(sig_avg_img, origin='lower',
           aspect='auto', extent=[0,7,-3,7], cmap=plt.get_cmap('BuPu'),
           vmax=0.01,vmin=0.0)
plt.colorbar()

# background
fig.add_subplot(1,3,2)
plt.title('Lund image (QCD)')
plt.xlabel('$\ln(R / \Delta)$')
plt.ylabel('$\ln(k_t / \mathrm{GeV})$')
plt.imshow(bkg_avg_img, origin='lower',
           aspect='auto', extent=[0,7,-3,7], cmap=plt.get_cmap('BuPu'),
           vmax=0.01,vmin=0.0)
plt.colorbar()

# ratio
fig.add_subplot(1,3,3)
plt.title('Lund image (W/QCD)')
plt.xlabel('$\ln(R / \Delta)$')
plt.ylabel('$\ln(k_t / \mathrm{GeV})$')
plt.imshow(sig_avg_img/bkg_avg_img, norm=LogNorm(), origin='lower', aspect='auto',
           extent=[0,7,-3,7], cmap=plt.get_cmap('seismic'), vmin=0.01,vmax=100)
plt.colorbar()
plt.show()
