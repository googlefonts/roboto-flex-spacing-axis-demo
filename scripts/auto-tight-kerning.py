from importlib import reload
import variableSpacing
reload(variableSpacing)
import variableSpacing.extras.touche
reload(variableSpacing.extras.touche)

from variableSpacing.extras.touche import Touche
from mojo.UI import CurrentSpaceCenter

f = CurrentFont()
T = Touche(f)
S = CurrentSpaceCenter()

steps = 100  # maximum attempts for pair
step = 5     # try with increment of 5 units

for g1, g2 in f.kerning.keys():
    # get key glyphs for kerning groups
    if 'public.kern' in g1:
        if g1 in f.groups and len(f.groups[g1]):
            glyph1 = f.groups[g1][0]
        else:
            print('\tempty group, skipping...')
            continue
    else:
        glyph1 = g1
    if 'public.kern' in g2:
        if g2 in f.groups and len(f.groups[g2]):
            glyph2 = f.groups[g2][0]
        else:
            print('\tempty group, skipping...')
            continue
    else:
        glyph2 = g2    

    # show pair in Space Center
    if S:
        txt = f'/H/H/{glyph1}/{glyph2}/H/O/H'
        S.setRaw(txt)

    # adjust pair until it (almost) touches
    print(f'adjusting pair ({g1}, {g2})...')
    oldValue = T.getKerning(f[glyph1], f[glyph2])
    foundValue = False
    for i in range(steps):
        T.lookupSidebearings([f[glyph1], f[glyph2]])
        if T.checkPair(f[glyph1], f[glyph2]):
            # pair overlaps, take previous value
            value = T.getKerning(f[glyph1], f[glyph2])
            value += step
            print(f'\tfound value: {value}')
            f.kerning[(g1, g2)] = value
            f.kerning.changed()
            foundValue = True
            break
        else:
            value = T.getKerning(f[glyph1], f[glyph2])
            value -= step
            # update font
            f.kerning[(g1, g2)] = value
            f.kerning.changed()
            # update touché
            T.flatKerning = f.naked().flatKerning
    if not foundValue:
        f.kerning[(g1, g2)] = oldValue
    print()
