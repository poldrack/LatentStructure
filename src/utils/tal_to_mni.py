import numpy as np
import scipy.linalg
from numpy import *

def tal_to_mni(foci):
        trans = np.array([[0.9254, 0.0024, -0.0118, -1.0207], [-0.0048, 0.9316, -0.0871, -1.7667], [0.0152, 0.0883,  0.8924, 4.0926], [0.0, 0.0, 0.0, 1.0]]).T
        trans = linalg.pinv(trans)
        foci = np.hstack((foci, ones((foci.shape[0], 1))))
        return np.dot(foci, trans)[:,0:3]


