'''
delete spacing state from sources

'''
# local variables
modulePath    = '/Users/sergiogonzalez/Desktop/hipertipo/tools/VariableSpacing/code/Lib' # '/hipertipo/tools/VariableSpacing/code/Lib'
sourcesFolder = '/Users/sergiogonzalez/Desktop/hipertipo/fonts/roboto-flex/sources'      # '/hipertipo/fonts/Roboto-Flex/sources'

# make sure that the VariableSpacing module is installed
import sys
if modulePath not in sys.path:
    sys.path.append(modulePath)
from importlib import reload
import variableSpacing
reload(variableSpacing)

import os, glob
from fontParts.world import OpenFont
import variableSpacing as vs

drawingsFolder     = '1A-drawings'
sourcesSubFolders  = ['Mains', 'Duovars']

# ---------------
# script settings
# ---------------

_spacingStateName   = 'loose'
_deleteSpacingState = True
_checkSpacingStates = True

# ---------
# do stuff!
# ---------

# collect sources
sources = []
for subFolder in sourcesSubFolders:
    folder = os.path.join(sourcesFolder, drawingsFolder, subFolder)
    sources += glob.glob(f'{folder}/*.ufo')
sources = [s for s in sources if 'GRAD' not in s]

if _deleteSpacingState:
    # add spacing states to fonts
    for ufoPath in sources:
        f = OpenFont(ufoPath, showInterface=False)
        print(f"deleting '{_spacingStateName}' spacing state from {ufoPath}...")
        vs.deleteSpacingState(f, _spacingStateName)
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
