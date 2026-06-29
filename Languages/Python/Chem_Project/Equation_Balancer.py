import numpy as np
x = np.array([-1, 3])
dx = np.ones_like(x)
dx[x < 0] = 0
print(dx)
