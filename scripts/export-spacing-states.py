'''
export spacing states from UFO sources
into JSON files of the same name

'''

# local variables
modulePath    = '/Users/sergiogonzalez/Desktop/hipertipo/tools/VariableSpacing/code/Lib'
sourcesFolder = '/Users/sergiogonzalez/Desktop/hipertipo/fonts/roboto-flex/sources'

# make sure that the VariableSpacing module is installed
import sys
if modulePath not in sys.path:
    sys.path.append(modulePath)
from importlib import reload
import variableSpacing
reload(variableSpacing)

import os, glob
from fontParts.world import OpenFont
from variableSpacing import *

drawingsFolder    = '1A-drawings'
sourcesSubFolders = ['Mains', 'Duovars']

# get output folder
baseFolder = os.path.dirname(os.getcwd())
jsonFolder = os.path.join(baseFolder, 'spacing states')

# export spacing states to JSON
for subFolder in sourcesSubFolders:
    subFolderPath = os.path.join(sourcesFolder, drawingsFolder, subFolder)
    ufos = glob.glob(f'{subFolderPath}/*.ufo')
    for ufoPath in ufos:
        if '_GRAD' in ufoPath:
            continue
        if '_SPAC' in ufoPath:
            continue
        f = OpenFont(ufoPath, showInterface=False)
        jsonPath = os.path.join(jsonFolder, os.path.split(ufoPath)[-1].replace('.ufo', '.json'))
        if os.path.exists(jsonPath):
            os.remove(jsonPath)
        exportSpacingStates(f, jsonPath)
        f.close()
