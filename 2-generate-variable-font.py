# make sure VariableSpacing is installed
import sys
modulePath = '/hipertipo/tools/VariableSpacing/code/Lib'
if modulePath not in sys.path:
    sys.path.append(modulePath)
from importlib import reload
import variableSpacing
reload(variableSpacing)

import os, shutil, glob
from operator import attrgetter
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor
from fontmake.font_project import FontProject
from variableSpacing import buildSpacingSources

# ---------------
# script settings
# ---------------

_clearOldFiles       = False
_buildSpacingSources = False
_ammendDesignspace   = False
_generateFont        = True
_clearFiles          = False

# ------------
# project data
# ------------

# input
sourcesFolder      = '/hipertipo/fonts/Roboto-Flex/sources'
drawingsFolder     = '1A-drawings'
sourcesSubFolders  = ['Mains', 'Duovars']
designspacePath    = '/hipertipo/fonts/Roboto-Flex/sources/RobotoFlex.designspace'
designspacePathNew = designspacePath.replace('.designspace', '_spacing-axis.designspace')

# output
outputFolder       = '/hipertipo/fonts/Roboto-Flex_SPAC'
varFontPath        = os.path.join(outputFolder, 'Roboto-Flex_SPAC.ttf')

prefix = '_SPAC-'

# ---------
# do stuff!
# ---------

if _clearOldFiles:
    # clean-up spacing axis files
    if os.path.exists(varFontPath):
        os.remove(varFontPath)
    if os.path.exists(designspacePathNew):
        os.remove(designspacePathNew)
    # collect spacing sources
    spacingSources = []
    for subFolder in sourcesSubFolders:
        folder = os.path.join(sourcesFolder, drawingsFolder, subFolder)
        spacingSources += [s for s in glob.glob(f'{folder}/*.ufo') if prefix in s]
    # delete all of them
    for ufo in spacingSources:
        shutil.rmtree(ufo)

if _buildSpacingSources:
    # build 'tight' states as separate spacing sources (temporary)
    newSources = []
    for subFolder in sourcesSubFolders:
        folder = os.path.join(sourcesFolder, drawingsFolder, subFolder)
        newSources += buildSpacingSources(folder, prefix=prefix)

if _ammendDesignspace:
    # collect all spacing sources
    spacingSources = []
    for subFolder in sourcesSubFolders:
        folder = os.path.join(sourcesFolder, drawingsFolder, subFolder)
        spacingSources += [s for s in glob.glob(f'{folder}/*.ufo') if prefix in s]
    # make a duplicate designspace
    print(f'duplicating designspace as {designspacePathNew}...')
    shutil.copyfile(designspacePath, designspacePathNew)
    # modify designspace
    D = DesignSpaceDocument()
    D.read(designspacePathNew)
    print('\tadding spacing axis to designspace...')
    # add spacing axis
    spacingAxis = AxisDescriptor()
    spacingAxis.name = spacingAxis.tag = 'SPAC'
    spacingAxis.labelNames['en'] = 'spacing'
    spacingAxis.maximum = 0
    spacingAxis.minimum = -100
    spacingAxis.default = 0
    D.addAxis(spacingAxis)
    # add spacing sources / add spacing location to existing sources
    print('\tadding spacing sources to designspace:')
    sources = []
    for source in D.sources:
        print(f'\t\tadding default location to {source.filename}...')
        # update existing sources with neutral spacing location 
        source.location['SPAC'] = 0
        sources.append(source)
        # add new sources with tight spacing (-100)
        spacingSourcePath = source.filename.replace('.ufo', f'{prefix}tight.ufo')
        if os.path.join(sourcesFolder, spacingSourcePath) not in spacingSources:
            # print(f'\t\tERROR: {spacingSourcePath} does not exist!')
            continue
        print(f'\t\tadding new source for {spacingSourcePath}...')
        newLocation = source.location.copy()
        newLocation['SPAC'] = -100
        srcSpacing = SourceDescriptor()
        srcSpacing.familyName = source.familyName
        srcSpacing.filename   = spacingSourcePath
        srcSpacing.location   = newLocation
        sources.append(srcSpacing)
    D.sources = sorted(sources, key=attrgetter('filename'))
    D.write(designspacePathNew)
    print('...done.\n')

if _generateFont:
    # generate variable font
    P = FontProject()
    P.build_variable_font(designspacePathNew, output_path=varFontPath, verbose=False)

if _clearFiles:
    # clear temporary files
    os.remove(designspacePathNew)
    for ufoPath in newSources:
        shutil.rmtree(ufoPath)
