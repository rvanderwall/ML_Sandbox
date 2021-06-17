from Generator import Generator
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

print("Mandel")

grid=(600, 600)
g = Generator(grid)
g.fill_grid()
imgplot = plt.imshow(g.grid)
plt.show()
