'''
build Roboto Flex SPAC variable font

- take RobotoFlex sources with spacing state libs
- build spacing states as separate UFO sources
- change the designspace to include a SPAC axis and the new sources
- build Roboto Flex SPAC variable font with fontmake
- optionally generate a WOFF2 file for testing

WARNING: this script takes a very long time to run!

the current performance bottleneck is the function `loadSpacingFromLib`
TL:DR; when the left margin of a glyph is changed,
we need to make sure that all its components stay in place

'''

# local variables
modulePath    = '/Users/sergiogonzalez/Desktop/hipertipo/tools/VariableSpacing/code/Lib' # '/hipertipo/tools/VariableSpacing/code/Lib'
sourcesFolder = '/Users/sergiogonzalez/Desktop/hipertipo/fonts/roboto-flex/sources/'     # '/hipertipo/fonts/Roboto-Flex/sources'
outputFolder  = '/Users/sergiogonzalez/Desktop/hipertipo/fonts/roboto-flex-spac/'        # '/hipertipo/fonts/Roboto-Flex_SPAC'

# make sure that the VariableSpacing module is installed
import sys
if modulePath not in sys.path:
    sys.path.append(modulePath)
from importlib import reload
import variableSpacing
reload(variableSpacing)

import os, shutil, glob
from operator import attrgetter
from defcon import Font
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor
from fontmake.font_project import FontProject
from variableSpacing import buildSpacingSources
from hTools3.modules.webfonts import sfnt2woff2

# --------
# settings
# --------

_clearOldFiles        = False
_buildSpacingSources  = False
_ammendDesignspace    = False
_generateVariableFont = False
_generateWOFF2        = True
_clearFiles           = False

# input
drawingsFolder        = '1A-drawings'
sourcesSubFolders     = ['Mains', 'Duovars']
designspacePath       = os.path.join(sourcesFolder, 'RobotoFlex.designspace')
designspacePathNew    = designspacePath.replace('.designspace', '_spacing-axis.designspace') # '_SPAC.designspace'

# output
varFontPath           = os.path.join(outputFolder, 'Roboto-Flex_SPAC.ttf')
prefix                = '_SPAC-'

# ------
# build!
# ------

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

    # delete all spacing sources
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
    spacingAxis.maximum = 100
    spacingAxis.minimum = -100
    spacingAxis.default = 0
    D.addAxis(spacingAxis)

    # add spacing sources / add spacing location to existing sources
    print('\tadding spacing sources to designspace:')
    sources = []
    for source in D.sources:
        print(f'\t\tadding default SPAC location to {source.filename}...')

        # update existing sources with neutral spacing location
        source.location['SPAC'] = 0
        sources.append(source)
 
        # add new sources with tight spacing (-100)
        spacingSourcePath = source.filename.replace('.ufo', f'{prefix}tight.ufo')
        if os.path.join(sourcesFolder, spacingSourcePath) not in spacingSources:
            continue
        print(f'\t\tadding new source for {spacingSourcePath}...')
        newLocation = source.location.copy()
        newLocation['SPAC'] = -100
        srcSpacing = SourceDescriptor()
        srcSpacing.familyName = source.familyName
        srcSpacing.filename   = spacingSourcePath
        srcSpacing.location   = newLocation
        sources.append(srcSpacing)

        # add new sources with loose spacing (+100)
        spacingSourcePath = source.filename.replace('.ufo', f'{prefix}loose.ufo')
        if os.path.join(sourcesFolder, spacingSourcePath) not in spacingSources:
            continue
        print(f'\t\tadding new source for {spacingSourcePath}...')
        newLocation = source.location.copy()
        newLocation['SPAC'] = 100
        srcSpacing = SourceDescriptor()
        srcSpacing.familyName = source.familyName
        srcSpacing.filename   = spacingSourcePath
        srcSpacing.location   = newLocation
        sources.append(srcSpacing)

    D.sources = sorted(sources, key=attrgetter('filename'))
    D.write(designspacePathNew)
    print('...done.\n')

if _generateVariableFont:
    # pre-load fonts as defcon objects
    print('pre-loading sources as Defcon objects...')
    D = DesignSpaceDocument()
    D.read(designspacePathNew)
    for src in D.sources:
        print(f'\tloading {src.path}...\n')
        src.font = Font(src.path)
    print('...done.\n')

    # generate variable font
    print('generating variable font... ', end='')
    P = FontProject()
    P.build_variable_fonts(D, output_path=varFontPath, verbose=False)
    print('done!\n')
    print(varFontPath, os.path.exists(varFontPath))

if _generateWOFF2:
    # generate webfont
    sfnt2woff2(varFontPath, varFontPath.replace('.ttf', '.woff2'))

if _clearFiles:
    # clear temporary files
    os.remove(designspacePathNew)
    for ufoPath in newSources:
        shutil.rmtree(ufoPath)
