import numpy as np
import matplotlib.pyplot as plt

y = np.array([range(2,8), range(3,9), range(4,10), range(5,11), range(6,12), range(7, 13)]).flatten()

plt.clf()
plt.xticks(range(2,13))
plt.hist(y, bins = 11, density = True, rwidth = 1, align='mid')
plt.savefig("../article_raw/images/die_roll_histogram.png")
