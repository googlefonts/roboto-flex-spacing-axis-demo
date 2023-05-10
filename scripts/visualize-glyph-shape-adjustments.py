from importlib import reload
import progvis.modules.pens
reload(progvis.modules.pens)

from fontParts.world import OpenFont, RGlyph
from progvis.modules.DB.tools import drawGlyph
from progvis.modules.pens import DecomposePointPen

# --------
# settings
# --------

ufoPath = '/Users/sergiogonzalez/Desktop/hipertipo/fonts/roboto-flex/sources/1A-drawings/Mains/RobotoFlex_wght400.ufo'

glyphNames = 'quotedbl quotedblleft quotedblright quotedblbase percent perthousand onequarter onehalf threequarters ij fi fl f_f f_f_i f_f_l f_f_ij f_ij IJacute ijacute DZcaron Dzcaron dzcaron LJ Lj lj NJ Nj nj Lcaron lcaron Ldot ldot napostrophe Alphatonos Epsilontonos Etatonos Iotatonos Omicrontonos Upsilontonos Omegatonos doubleprimemod second numero'.split()

tightLayer = 'SPAC_tight'

mx, my = 20, 10
s = 0.036

lh = 1.1

ctx1 = 'n'
ctx2 = 'n'

c1 = 1, 0, 0
c2 = 0, 0, 0

# -----
# draw!
# -----

f = OpenFont(ufoPath)

# TO-DO: load tight spacing state

g1 = f[ctx1]
g2 = f[ctx2]

for i in range(2):

    tightShow = bool(i)

    newPage('A4Landscape')
    fill(1)
    rect(0, 0, width(), height())

    x = mx
    y = height() - f.info.unitsPerEm*s - my

    _x, _y = x, y

    for gName in glyphNames:

        if not tightShow:
            srcGlyph = f[gName]
        else:
            srcGlyph = f[gName].getLayer(tightLayer)

        g = RGlyph()
        pointPen = g.getPointPen()
        if not tightShow:
            decomposePen = DecomposePointPen(f, pointPen)
        else:
            decomposePen = DecomposePointPen(f.getLayer(tightLayer), pointPen)
        srcGlyph.drawPoints(decomposePen)
        g.name    = srcGlyph.name
        g.unicode = srcGlyph.unicode
        g.width   = srcGlyph.width

        with savedState():
            if _x > width() - mx - (g.width+g1.width+g2.width)*s:
                _x = x
                _y -= f.info.unitsPerEm * s * lh

            translate(_x, _y)
            scale(s)
            fill(*c1)
            with savedState():
                fill(*c2)
                drawGlyph(g2)
            translate(g1.width, 0)
            drawGlyph(g)
            translate(g.width, 0)
            with savedState():
                fill(*c2)
                drawGlyph(g2)

        _x += (g.width+g1.width+g2.width) * s

# ------
# saving
# ------

saveImage('glyph-adjustments-SPAC.png', multipage=True)
