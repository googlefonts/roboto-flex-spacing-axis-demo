# clean-up spacing states files from bad values

import sys
modulePath = '/hipertipo/tools/VariableSpacing/code/Lib'
if modulePath not in sys.path:
    sys.path.append(modulePath)
from importlib import reload
import variableSpacing
reload(variableSpacing)

import os, glob, json
from variableSpacing import *

jsonFolder = '/hipertipo/fonts/Roboto-Flex_SPAC/spacing states/'
jsonPaths = glob.glob(f'{jsonFolder}/*.json')

for jsonPath in jsonPaths:

    # load json data into dict
    with open(jsonPath, 'r', encoding='utf-8') as f:
        spacingStates = json.load(f)

    # manipulate spacing states data
    spacingLib = spacingStates[KEY_SPACING]

    print(jsonPath)

    # clear negative widths in 'loose' spacing state    
    deleteGlyphs = []
    for glyphName in spacingLib['loose']:
        if spacingLib['loose'][glyphName]['width'] < 0:
            deleteGlyphs.append(glyphName)
    for glyphName in deleteGlyphs:
        print(f"removing {glyphName} (loose): width {spacingLib['loose'][glyphName]['width']}")
        del spacingLib['loose'][glyphName]

    # remove any width changes to space
    for spacingState in spacingLib:
        if 'space' in spacingLib[spacingState]:
            print(f'removing space from {spacingState}')
            del spacingLib[spacingState]['space']

    # save spacing states data back into dict
    spacingStates[KEY_SPACING] = spacingLib
    print(f'saving corrected data back into json file')
    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(spacingStates, f, indent=2)

    print()
