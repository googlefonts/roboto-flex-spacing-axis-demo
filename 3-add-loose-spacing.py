# make sure VariableSpacing is installed
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

# ---------------
# script settings
# ---------------

_addSpacingStates   = True
_checkSpacingStates = True

# ------------
# project data
# ------------

sourcesFolder      = '/hipertipo/fonts/Roboto-Flex/sources'
drawingsFolder     = '1A-drawings'
sourcesSubFolders  = ['Mains', 'Duovars']

# ---------
# do stuff!
# ---------

# collect sources
sources = []
for subFolder in sourcesSubFolders:
    folder = os.path.join(sourcesFolder, drawingsFolder, subFolder)
    sources += glob.glob(f'{folder}/*.ufo')
sources = [s for s in sources if 'GRAD' not in s]

if _addSpacingStates:
    # add spacing states to fonts
    for ufoPath in sources:
        f = OpenFont(ufoPath, showInterface=False)
        print(f"creating 'loose' spacing state in {ufoPath}...")

        # save default spacing state
        # vs.saveComponentsToLib(f)
        # vs.saveSpacingToLib(f, 'default')
        # vs.saveKerningToLib(f, 'default')

        # expand glyph margins
        vs.smartSetMargins(f, f.glyphOrder, leftMargin=100, leftMode=1, rightMargin=100, rightMode=1, verbose=False, setUndo=False)
        # modify space glyph
        f['space'].width *= 1.5

        # save loose spacing state
        vs.saveSpacingToLib(f, 'loose')
        vs.saveKerningToLib(f, 'loose')

        # load default spacing state
        vs.loadSpacingFromLib(f, 'default')
        vs.loadKerningFromLib(f, 'default')

        # f.openInterface()
        f.save()
        f.close()

# check for spacing states in fonts
if _checkSpacingStates:
    for ufoPath in sources:
        if '_SPAC' in ufoPath:
            continue
        f = OpenFont(ufoPath, showInterface=False)
        spacingStates = vs.getSpacingStates(f)
        print(f"{ufoPath} : {' '.join(spacingStates)}")
        f.close()
