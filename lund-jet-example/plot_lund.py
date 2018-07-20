# !/usr/bin/env python3
#
# Frederic Dreyer, BOOST 2018 tutorial
#

from create_image import LundImage
from matplotlib.colors import LogNorm
import numpy as np
import matplotlib.pyplot as plt

# set up the readers
sig_reader = LundImage('W-lund-pt2000-parton.json.gz',50000,25)
bkg_reader = LundImage('dijet-lund-pt2000-parton.json.gz',50000,25)

# get array from file
sig_images = np.array(sig_reader.values())[:,0]
bkg_images = np.array(bkg_reader.values())[:,0]
sig_avg_img = np.transpose(np.average(sig_images,axis=0))
bkg_avg_img = np.transpose(np.average(bkg_images,axis=0))
# plot average image


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
