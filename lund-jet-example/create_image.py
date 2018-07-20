# Frederic Dreyer, BOOST 2018 tutorial

from abc import ABC, abstractmethod
import numpy as np
from math import log, ceil, floor, cos, sin, pi
import json, gzip, sys

#----------------------------------------------------------------------
class Reader(object):
    """
    Reader for files consisting of a sequence of json objects.
    Any pure string object is considered to be part of a header (even if it appears at the end!)
    """
    def __init__(self, infile, nmax = -1):
        self.infile = infile
        self.nmax = nmax
        self.reset()
        
    def reset(self):
        """
        Reset the reader to the start of the file, clear the header and event count.
        """
        self.stream = gzip.open(self.infile,'r')
        self.n = 0
        self.header = []
        
        
    #----------------------------------------------------------------------
    def __iter__(self):
        # needed for iteration to work 
        return self
        
    def __next__(self):
        ev = self.next_event()
        if (ev is None): raise StopIteration
        else           : return ev

    def next(self): return self.__next__()
        
    def next_event(self):

        # we have hit the maximum number of events
        if (self.n == self.nmax):
            print ("# Exiting after having read nmax jet declusterings")
            return None
        
        try:
            line = self.stream.readline()
            j = json.loads(line.decode('utf-8'))
        except IOError:
            print("# got to end with IOError (maybe gzip structure broken?) around event", self.n, file=sys.stderr)
            return None
        except EOFError:
            print("# got to end with EOFError (maybe gzip structure broken?) around event", self.n, file=sys.stderr)
            return None
        except ValueError:
            print("# got to end with ValueError (empty json entry) around event", self.n, file=sys.stderr)
            return None

        # skip this
        if (type(j) is str):
            self.header.append(j)
            return self.next_event()
        self.n += 1
        return j

    
class Image(ABC):
    """Image which transforms point-like information into pixelated 2D
    images which can be processed by convolutional neural networks."""
    def __init__(self, infile, nmax):
        self.reader = Reader(infile, nmax)

    @abstractmethod
    def process(self, event):
        pass
    
    def values(self):
        res = []
        while True:
            event = self.reader.next_event()
            if event!=None:
                res.append(self.process(event))
            else:
                break
        self.reader.reset()
        return res

        
        
class JetImage(Image):
    """
    Take input file and transforms it into parsable jet image.
    """
    def __init__(self, infile, nmax, npxl, R=1.0):
        Image.__init__(self, infile, nmax)
        self.npxl = npxl
        self.pxl_wdth = 2.0 * R / npxl
        self.R = R

    def process(self, event):
        res = np.zeros((2,self.npxl,self.npxl))
        j = event[0]
        tot_pt = 0.0
        wgt_avg_rap = 0.0
        wgt_avg_phi = 0.0
        for p in event[1:]:
            phi = p['phi']
            if (p['phi'] - j['phi'] > 2 * self.R):
                phi -= 2.0*pi
            if (p['phi'] - j['phi'] < -2 * self.R):
                phi += 2.0*pi
            tot_pt += p['pt']
            wgt_avg_rap += p['rap']*p['pt']
            wgt_avg_phi += phi     *p['pt']
        wgt_avg_rap = wgt_avg_rap / tot_pt
        wgt_avg_phi = wgt_avg_phi / tot_pt

        rap_pt_cent_indx = int(ceil(wgt_avg_rap/self.pxl_wdth - 0.5) - floor(self.npxl/2.0))
        phi_pt_cent_indx = int(ceil(wgt_avg_phi/self.pxl_wdth - 0.5) - floor(self.npxl/2.0))

        L1norm = 0.0
        for p in event[1:]:
            phi = p['phi']
            if (p['phi'] - j['phi'] > 2 * self.R):
                phi -= 2.0*pi
            if (p['phi'] - j['phi'] < -2 * self.R):
                phi += 2.0*pi
            rap_indx = int(ceil(p['rap']/self.pxl_wdth - 0.5) - rap_pt_cent_indx)
            phi_indx = int(ceil(phi     /self.pxl_wdth - 0.5) - phi_pt_cent_indx)
            # print(rap_pt_cent_indx,rap_indx,phi_pt_cent_indx,phi_indx,
            #       ':',p['pt'])
            if (rap_indx < 0 or rap_indx >= self.npxl or
                phi_indx < 0 or phi_indx >= self.npxl):
                continue
            res[0,phi_indx,rap_indx] += p['pt']
            res[1,phi_indx,rap_indx] += 1
            L1norm += p['pt']

        if L1norm > 0.0:
            res[0] = res[0]/L1norm

        return res
        
class LundImageAbs(Image):
    """
    Take input file and transforms it into parsable lund image.
    """
    def __init__(self, infile, nmax, npxl, xval, yval):
        Image.__init__(self, infile, nmax)
        self.npxl = npxl
        self.xmin = xval[0]
        self.ymin = yval[0]
        self.x_pxl_wdth = (xval[1] - xval[0])/npxl
        self.y_pxl_wdth = (yval[1] - yval[0])/npxl

    def process(self, event):
        res = np.zeros((4,self.npxl,self.npxl))
        L1norm = 0.0

        for declust in event:
            x = log(1.0/declust['delta_R'])
            y = self.ptcoord(declust)
            varphi = declust['varphi']
            xind = ceil((x - self.xmin)/self.x_pxl_wdth - 1.0)
            yind = ceil((y - self.ymin)/self.y_pxl_wdth - 1.0)
            # print((x - self.xmin)/self.x_pxl_wdth,xind,
            #       (y - self.ymin)/self.y_pxl_wdth,yind,':',
            #       declust['delta_R'],declust['pt2'])
            if (max(xind,yind) < self.npxl and min(xind, yind) >= 0):
                res[0,xind,yind] += 1
                if not (abs(res[1,xind,yind]) > 0):
                    res[1,xind,yind] = 0.5 * (1.0 + cos(varphi))
                if not (abs(res[2,xind,yind]) > 0):
                    res[2,xind,yind] = 0.5 * (1.0 + sin(varphi))
                L1norm += 1.0
        if L1norm > 0.0:
            res[0] = res[0]/L1norm
        return res

    @abstractmethod
    def ptcoord(self, declust):
        pass

class LundImageLnpt(LundImageAbs):
    def __init__(self, infile, nmax, npxl, xval = [0.0, 7.0], yval = [-3.0, 7.0]):
        LundImageAbs.__init__(self, infile, nmax, npxl, xval, yval)
    
    def ptcoord(self, declust):
        val = declust['pt2'] * declust['delta_R']
        return log(val)
    
class LundImageZrel(LundImageAbs):
    def __init__(self, infile, nmax, npxl, xval = [0.0, 7.0], yval = [-12.0, 0.0]):
        LundImageAbs.__init__(self, infile, nmax, npxl, xval, yval)
    
    def ptcoord(self, declust):
        val = declust['pt2'] / (declust['pt1']+declust['pt2'])
        return log(val * declust['delta_R'])
    
class LundImageZabs(LundImageAbs):
    def __init__(self, infile, nmax, npxl, xval = [0.0, 7.0], yval = [-12.0, 0.0]):
        LundImageAbs.__init__(self, infile, nmax, npxl, xval, yval)
    
    def ptcoord(self, declust):
        val = declust['z'] * declust['delta_R']
        return log(val)

class LundImage(object):
    def __init__(self, infile, nmax, npxl, metric='lnpt'):
        if metric=='lnpt':
            self.lund = LundImageLnpt(infile, nmax, npxl)
        elif metric=='zrel':
            self.lund = LundImageZrel(infile, nmax, npxl)
        elif metric=='zabs':
            self.lund = LundImageZabs(infile, nmax, npxl)
        else:
            raise ValueError("LundImage metric must be: lnpt, zrel or zabs")

    def values(self):
        return self.lund.values()

class LundDenseAbs(Image):
    def __init__(self,infile, nmax, nlen, secondary=False):
        Image.__init__(self, infile, nmax)
        self.nlen      = nlen
        self.secondary = secondary
        
    def process(self, event):
        res = np.zeros((self.nlen if not self.secondary else self.nlen*2, 8))

        if self.secondary:
            event_secondary = event[1]
            event = event[0]
            for i in range(self.nlen):
                if (i>= len(event_secondary)):
                    break
                dec=self.fill_declust(event_secondary[i])
                res[self.nlen+i,:] = dec
                
        for i in range(self.nlen):
            if (i >= len(event)):
                break
            res[i,:] = self.fill_declust(event[i])
            
        return res

    def fill_declust(self,declust):
        res = np.zeros(8)
        x = log(1.0/declust['delta_R'])
        y = self.ptcoord(declust)
        varphi = declust['varphi']
        pt1 = declust['pt1']
        pt2 = declust['pt2']
        kt  = declust['kt']
        z   = declust['z']
        m   = declust['m']
        res[0] = x
        res[1] = y
        res[2] = varphi
        res[3] = m
        res[4] = pt1
        res[5] = pt2
        res[6] = kt
        res[7] = z
        return res
        
    @abstractmethod
    def ptcoord(self, declust):
        pass

class LundDenseLnpt(LundDenseAbs):
    def __init__(self, infile, nmax, nlen, secondary=False):
        LundDenseAbs.__init__(self, infile, nmax, nlen, secondary)
    
    def ptcoord(self, declust):
        val = declust['pt2'] * declust['delta_R']
        return log(val)
    
class LundDenseZrel(LundDenseAbs):
    def __init__(self, infile, nmax, nlen, secondary=False):
        LundDenseAbs.__init__(self, infile, nmax, nlen, secondary)
    
    def ptcoord(self, declust):
        val = declust['pt2'] / (declust['pt1']+declust['pt2'])
        return log(val * declust['delta_R'])
    
class LundDenseZabs(LundDenseAbs):
    def __init__(self, infile, nmax, nlen, secondary=False):
        LundDenseAbs.__init__(self, infile, nmax, nlen, secondary)
    
    def ptcoord(self, declust):
        val = declust['z'] * declust['delta_R']
        return log(val)

class LundDense(object):
    def __init__(self, infile, nmax, nlen, metric='lnpt', secondary=False):
        if metric=='lnpt':
            self.lund = LundDenseLnpt(infile, nmax, nlen, secondary)
        elif metric=='zrel':
            self.lund = LundDenseZrel(infile, nmax, nlen, secondary)
        elif metric=='zabs':
            self.lund = LundDenseZabs(infile, nmax, nlen, secondary)
        else:
            raise ValueError("LundDense metric must be: lnpt, zrel or zabs")

    def values(self):
        return self.lund.values()
