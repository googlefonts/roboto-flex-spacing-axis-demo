'''
import spacing states from JSON files
into UFO sources of the same name

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

# collect all json files with spacing states
baseFolder = os.getcwd()
spacingStatesFolder = os.path.join(baseFolder, 'spacing states')
spacingStates = {}
jsonFiles = glob.glob(f'{spacingStatesFolder}/*.json')
for jsonFile in jsonFiles:
    key = os.path.splitext(os.path.split(jsonFile)[-1])[0]
    spacingStates[key] = jsonFile

# collect related ufo sources
drawingsFolder    = '1A-drawings'
sourcesSubFolders = ['Mains', 'Duovars']
sources = {}
for subFolder in sourcesSubFolders:
    subFolderPath = os.path.join(sourcesFolder, drawingsFolder, subFolder)
    ufos = glob.glob(f'{subFolderPath}/*.ufo')
    for ufoPath in ufos:
        key = os.path.splitext(os.path.split(ufoPath)[-1])[0]
        sources[key] = ufoPath

# import spacing states into sources
for fontName in spacingStates.keys():
    jsonPath = spacingStates[fontName]
    ufoPath  = sources[fontName]
    font = OpenFont(ufoPath, showInterface=False)
    importSpacingStates(font, jsonPath)
    font.save()
    font.close()
