from io import BytesIO
figfile = BytesIO()
plt.savefig(figfile, format='svg')
figdata_svg = figfile.getvalue()
