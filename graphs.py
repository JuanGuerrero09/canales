import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

G = 9.81
Q = 3.5
b = 2
z = 1.5



def energy_trapezoidal(y):
    return y + (Q**2 / (2 * G * (b*y + z*y**2)**2))

print(energy_trapezoidal(0.001))

y1 = np.arange(0.2, 4.5, 0.1)

ax1 = plt.subplot(212)
ax1.margins(0.05)           # Default margin is 0.05, value 0 means fit
ax1.plot( energy_trapezoidal(y1), y1)

ax2 = plt.subplot(221)
ax2.margins(2, 2)           # Values >0.0 zoom out
ax2.plot( energy_trapezoidal(y1), y1)
ax2.set_title('Zoomed out')

ax3 = plt.subplot(222)
ax3.margins(x=0, y=-0.25)   # Values in (-0.5, 0.0) zooms in to center
ax3.plot( energy_trapezoidal(y1), y1)
ax3.set_title('Zoomed in')

plt.show()