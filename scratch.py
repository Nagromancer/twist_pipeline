from path import Path
import numpy as np
import matplotlib.pyplot as plt

bjed = 2461068.321666922

lc_path = Path("/Users/nagro/PycharmProjects/twist_pipeline/ztf_j0328-1219_combined.lc")
lc = np.loadtxt(lc_path, skiprows=13)

time = lc[:, 0] / 86400 + bjed
flux = lc[:, 1] + 1
flux_err = lc[:, 2]

plt.rcParams['figure.figsize'] = [14, 9]
plt.rcParams["font.family"] = "Times"
plt.rcParams["font.size"] = 32
plt.rcParams['legend.fontsize'] = 25
plt.rcParams['text.usetex'] = True
plt.rcParams['axes.titlesize'] = 32

period = 

flux_mod_offset = (time - bjed).astype(int)
plt.errorbar(time % 1, flux + flux_mod_offset, yerr=flux_err, fmt='o', color='blue', ecolor='lightgray', elinewidth=3, capsize=0)
plt.xlabel("Time (BJD)")
plt.ylabel("Relative Flux")
plt.title("Light Curve")
plt.grid()
plt.show()