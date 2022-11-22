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

_clearSpacingState  = True
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

if _clearSpacingState:
    # add spacing states to fonts
    for ufoPath in sources:
        f = OpenFont(ufoPath, showInterface=False)
        print(f"deleting 'loose' spacing from {ufoPath}...")
        vs.deleteSpacingState(f, 'loose')
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
