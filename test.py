from colour.plotting import CIE_1931_chromaticity_diagram_plot, display
from colour import CMFS, ILLUMINANTS_RELATIVE_SPDS, SpectralPowerDistribution, spectral_to_XYZ, XYZ_to_xy
import pandas as pd
import pylab
from io import BytesIO


cmfs = CMFS['CIE 1931 2 Degree Standard Observer']
with open('test.txt') as f:
    data = pd.read_csv(f, sep="\t" or ' ' or ',', header=None)
    f.close()
w = [i[0] for i in data.values]
s = [i[1] for i in data.values]
data_formated = dict(zip(w, s))
print(data)
print(data.values)
print(data_formated)
spd = SpectralPowerDistribution('Sample', data_formated)
illuminant = ILLUMINANTS_RELATIVE_SPDS['D50']
XYZ = spectral_to_XYZ(spd, cmfs, illuminant)
print(XYZ)
xy = XYZ_to_xy(XYZ)
print(xy)

CIE_1931_chromaticity_diagram_plot(standalone=False)
x, y = xy
pylab.plot(x, y, 'o-', color='white')
pylab.annotate('test',
               xy=xy,
               xytext=(-50, 30),
               textcoords='offset points',
               arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=-0.2'))

a = display(standalone=False)
print(type(a))
figfile = BytesIO()
a.savefig(figfile, format='svg')
figfile.seek(0)
figdata_svg = '<svg' + str(figfile.getvalue()).split('<svg')[1]
#figdata_svg = figdata_svg.encode('utf-8')
print(figdata_svg)
