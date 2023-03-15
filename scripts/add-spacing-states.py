'''
automatically adds 'tight' and 'loose' spacing state to UFO sources

'''

# make sure that the VariableSpacing module is installed
import sys
modulePath = '/hipertipo/tools/VariableSpacing/code/Lib'
if modulePath not in sys.path:
    sys.path.append(modulePath)
from importlib import reload
import variableSpacing
reload(variableSpacing)

import os, glob
from fontParts.world import OpenFont
import variableSpacing as vs

# local variables
sourcesFolder = '/Users/sergiogonzalez/Desktop/hipertipo/fonts/roboto-flex/sources' # '/hipertipo/fonts/Roboto-Flex/sources'

# --------
# settings
# --------

_addLooseSpacingState = True
_scaleLooseState      = 200
_addTightSpacingState = True
_marginTightState     = 10
_checkSpacingStates   = True
_findNegativeWidths   = False

drawingsFolder        = '1A-drawings'
sourcesSubFolders     = ['Trivars'] # ['Mains', 'Duovars']

# ---------
# do stuff!
# ---------

# collect UFO sources
sources = []
for subFolder in sourcesSubFolders:
    folder   = os.path.join(sourcesFolder, drawingsFolder, subFolder)
    sources += glob.glob(f'{folder}/*.ufo')
# do not include GRAD sources
sources = [s for s in sources if 'GRAD' not in s]

if _addLooseSpacingState or _addTightSpacingState:
    # add spacing states to sources
    for ufoPath in sources:
        f = OpenFont(ufoPath, showInterface=False)

        # save the current spacing state as 'default'
        vs.saveSpacingToLib(f, 'default')
        vs.saveKerningToLib(f, 'default')

        # -------------------
        # add 'loose' spacing
        # -------------------

        if _addLooseSpacingState:
            print(f"creating 'loose' spacing state in {ufoPath}...")

            # increase all glyph margins by % -- DO NOT modify space glyph
            vs.smartSetMargins(f, f.glyphOrder, leftMargin=_scaleLooseState, leftMode=2, rightMargin=_scaleLooseState, rightMode=2, setUndo=False)

            # set all kerning to zero
            kerning = {}
            for pair, value in f.kerning.items():
                kerning[pair] = 1 if value > 0 else -1
            f.kerning.update(kerning)

            # save the new 'loose' spacing state
            vs.saveSpacingToLib(f, 'loose')
            vs.saveKerningToLib(f, 'loose')

            # load back the 'default' spacing state
            vs.loadSpacingFromLib(f, 'default')
            vs.loadKerningFromLib(f, 'default')

        # -------------------
        # add 'tight' spacing
        # -------------------

        if _addTightSpacingState:
            print(f"creating 'tight' spacing state in {ufoPath}...")

            # reduce all glyph margins to minimum -- DO NOT modify space glyph
            vs.smartSetMargins(f, f.glyphOrder, leftMargin=_marginTightState, leftMode=0, rightMargin=_marginTightState, rightMode=0, setUndo=False)

            # set kerning to almost touching ## too slow, skipping for now
            # vs.autoSetTightKerning(f)

            # save the new 'loose' spacing state
            vs.saveSpacingToLib(f, 'tight')
            vs.saveKerningToLib(f, 'tight')

            # load back the 'default' spacing state
            vs.loadSpacingFromLib(f, 'default')
            vs.loadKerningFromLib(f, 'default')

        # -----
        # done!
        # -----

        f.save()
        f.close()

if _checkSpacingStates:
    # double-check all spacing states in UFO sources
    for ufoPath in sources:
        if '_SPAC' in ufoPath:
            continue
        f = OpenFont(ufoPath, showInterface=False)
        spacingStates = vs.getSpacingStates(f)
        print(f"{ufoPath} : {' '.join(spacingStates)}")
        f.close()

if _findNegativeWidths:
    # find glyphs with negative widths
    for ufoPath in sources:
        f = OpenFont(ufoPath, showInterface=False)
        print(ufoPath)
        for g in f:
            if g.width < 0:
                print(g.name, g.width)
                # QUICK FIX
                g.width = 0
        print()
        f.save()
        f.close()
