'''
export spacing states from UFO sources
into JSON files of the same name

'''

# local variables
modulePath    = '/hipertipo/tools/VariableSpacing/code/Lib'
sourcesFolder = '/hipertipo/fonts/Roboto-Flex/sources'

# make sure that the VariableSpacing module is installed
import sys
if modulePath not in sys.path:
    sys.path.append(modulePath)
from importlib import reload
import variableSpacing
reload(variableSpacing)

import os, glob
from variableSpacing import *

drawingsFolder    = '1A-drawings'
sourcesSubFolders = ['Mains', 'Duovars']

# get output folder
baseFolder = os.getcwd()
jsonFolder = os.path.join(baseFolder, 'spacing states')

# export spacing states to JSON
for subFolder in sourcesSubFolders:
    subFolderPath = os.path.join(sourcesFolder, drawingsFolder, subFolder)
    ufos = glob.glob(f'{subFolderPath}/*.ufo')
    for ufoPath in ufos:
        f = OpenFont(ufoPath, showInterface=False)
        jsonPath = os.path.join(jsonFolder, os.path.split(ufoPath)[-1].replace('.ufo', '.json'))
        if os.path.exists(jsonPath):
            os.remove(jsonPath)
        exportSpacingStates(f, jsonPath)
        f.close()
