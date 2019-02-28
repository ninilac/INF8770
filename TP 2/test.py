import numpy as np
import zigzag

x = np.arange(49)
y = zigzag.square(x)
print y
print zigzag.diagonal(y)