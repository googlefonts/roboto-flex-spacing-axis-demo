'''
automatically adds a 'loose' spacing state to UFO sources

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
_checkSpacingStates   = False
_findNegativeWidths   = False

drawingsFolder        = '1A-drawings'
sourcesSubFolders     = ['Mains', 'Duovars']

fontNames = [
    'RobotoFlex_opsz144_wght1000.ufo',
]

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

if _addLooseSpacingState:
    # add spacing states to sources
    for ufoPath in sources:
        f = OpenFont(ufoPath, showInterface=False)

        if os.path.split(ufoPath)[-1] not in fontNames:
            continue

        # add 'loose' only to fonts which already have 'tight' and 'default'
        existingStates = vs.getSpacingStates(f)
        if 'tight' not in existingStates:
            print(f"skipping {ufoPath}...")
            continue

        print(f"creating 'loose' spacing state in {ufoPath}...")

        # we assume that the default spacing state is already saved
        # vs.saveSpacingToLib(f, 'default')
        # vs.saveKerningToLib(f, 'default')

        # increase all glyph margins by % -- DO NOT modify the space glyph!
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

        # f.openInterface()
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
