from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from colour.plotting import CIE_1931_chromaticity_diagram_plot, single_spd_plot
from colour import CMFS, ILLUMINANTS_RELATIVE_SPDS, SpectralPowerDistribution, spectral_to_XYZ, XYZ_to_xy
import pandas as pd
import pylab
from io import StringIO
#import pprint
import matplotlib.pyplot as plot


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    cmfs = CMFS['CIE 1931 2 Degree Standard Observer']
    with open('test.txt') as f:
        data = pd.read_csv(f, sep="\t" or ' ' or ',', header=None)
        f.close()
    w = [i[0] for i in data.values]
    s = [i[1] for i in data.values]
    data_formated = dict(zip(w, s))
    spd = SpectralPowerDistribution('Sample', data_formated)
    b = single_spd_plot(spd, standalone=False, figure_size=(5, 5), title='Spectrum')
    figfile_b = StringIO()
    b.savefig(figfile_b, format='svg')
    figfile_b.seek(0)
    figdata_svg_b = '<svg' + figfile_b.getvalue().split('<svg')[1]
    illuminant = ILLUMINANTS_RELATIVE_SPDS['D50']
    XYZ = spectral_to_XYZ(spd, cmfs, illuminant)
    xy = XYZ_to_xy(XYZ)
    print(xy)

    CIE_1931_chromaticity_diagram_plot(standalone=False, figure_size=(5, 5), grid=False,
                                       title='CIE 1931 Chromaticity Diagram', bounding_box=(-0.1, 0.9, -0.05, 0.95))
    x, y = xy
    pylab.plot(x, y, 'o-', color='white')
    pylab.annotate((("%.4f" % x), ("%.4f" % y)),
                   xy=xy,
                   xytext=(-50, 30),
                   textcoords='offset points',
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=-0.2'))

    a = plot.gcf()
    figfile = StringIO()
    a.savefig(figfile, format='svg')
    figfile.seek(0)
    figdata_svg = '<svg' + figfile.getvalue().split('<svg')[1]
    #pprint.pprint(figdata_svg)
    return render_template('index.html', spd=figdata_svg_b, result=figdata_svg)

if __name__ == "__main__":
    app.run()
