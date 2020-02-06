import csv
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import pandas as pd

# First create some toy data:
x = np.linspace(0, 2*np.pi, 400)
y = np.sin(x**2)

# Creates just a figure and only one subplot
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Simple plot')
# plt.show()

# Creates two subplots and unpacks the output array immediately
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.plot(x, y)
ax1.set_title('Sharing Y axis')
ax2.scatter(x, y)
# plt.show()


# Share a Y axis with each row of subplots
plt.subplots(2, 2, sharey='row')
# plt.show()


# Show inset charts
fig, ax1 = plt.subplots()

# These are in unitless percentages of the figure size. (0,0 is bottom left)
left, bottom, width, height = [0.25, 0.6, 0.2, 0.2]
ax2 = fig.add_axes([left, bottom, width, height])

ax1.plot(range(10), color='red')
ax2.plot(range(6)[::-1], color='green')

plt.show()
