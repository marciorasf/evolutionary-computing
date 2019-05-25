# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

# Make data.
X = np.arange(-5.12, 5.12, 0.05)
Y = np.arange(-5.12, 5.12, 0.05)
X, Y = np.meshgrid(X, Y)
Z = 20 + X**2 - 10*np.cos(np.pi*2*X) + Y**2 - 10*np.cos(np.pi*2*Y)


# fig = plt.figure()
# ax = fig.gca(projection='3d')

# # Plot the surface.
# surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,linewidth=0, antialiased=True)

# # Customize the z axis.
# ax.set_zlim(-1, 100)
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# fig.colorbar(surf, shrink=0.5, aspect=5)
# # Add a color bar which maps values to colors.

# plt.show()
plt.ion()
fig = plt.figure()
cp = plt.contourf(X, Y, Z)
plt.colorbar(cp)
plt.title('Contour')
plt.xlabel('x1')
plt.ylabel('x2')

points = fig.add_subplot()
x1 = np.arange(-2,0,0.25)
y1 = np.arange (-2,0,0.25)
linel, = points.plot(x1,y1, marker='o',color='red', linestyle='None' )
fig.canvas.draw()
input()
x1 = np.arange(0,2,0.25)
y1 = np.arange (0,2,0.25)
linel.set_data(x1, y1)
fig.canvas.draw()
input()
