import numpy as np
import matplotlib.pyplot as plt

alpha = 1
A = np.array([[1, 1], [1, 1]])
tau = 1


# pure strategies look like 1) (1, 0) and (1, 0) or 2) (1, 0) and (0, 1) or 3) (0, 1) and (1, 0) or 4) (0, 1) and (0, 1)

# Then, the population will look like a mixture of all of these pure strategies. If we take the expectation on each of these