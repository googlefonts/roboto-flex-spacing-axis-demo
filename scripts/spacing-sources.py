import os, glob
from fontParts.world import OpenFont
from progvis.objects.ufotext import UFOSetter

baseFolder = '/Users/sergiogonzalez/Desktop/hipertipo/fonts/roboto-flex/sources/1A-drawings'
subFolders = ['Mains', 'Duovars']

c0 = 0,
c1 = 1,0,0
c2 = 0,0,1

for folder in subFolders:

    ufos = glob.glob(f'{baseFolder}/{folder}/*.ufo')

    statesTrue  = []
    statesFalse = []
    for ufo in ufos:
        if 'SPAC' in ufo:
            continue
        ufoTight = ufo.replace('.ufo', '_SPAC-tight.ufo')
        ufoLoose = ufo.replace('.ufo', '_SPAC-loose.ufo')
        if os.path.exists(ufoTight) and os.path.exists(ufoLoose):
            statesTrue.append(ufo)
        else:
            statesFalse.append(ufo)

    ufos = sorted(statesFalse)
    for ufo in sorted(statesTrue):
        ufos += [
            ufo.replace('.ufo', '_SPAC-tight.ufo'),     
            ufo, 
            ufo.replace('.ufo', '_SPAC-loose.ufo')
        ]

    txt = 'abcdegno'

    newPage('A4')
    save()
    translate(width()/2, height()-70)
    fontSize(13)
    text(folder, (0, 40), align='center')
    fontSize(7)

    for ufo in ufos:
        f = OpenFont(ufo)
        T = UFOSetter(f)
        T.scale = 0.0125
        T.text = txt
        if ufo in statesFalse:
            c = c1
        elif '_SPAC' in ufo:
            c = c2
        else:
            c = c0
        fill(*c)
        T.fillColor = 0, # c
        T.draw((0, 0))
        text(os.path.split(ufo)[-1], (-5, 0), align='right')
        translate(0, -f.info.unitsPerEm * T.scale)
    
    restore()    

    s = 16

    translate(120, 30)
    for i in range(3):
        if i == 0:
            c = c0
            caption = 'default'
        elif i == 1: 
            c = c2
            caption = 'added'
        else:
            c = c1
            caption = 'plain'
        fill(*c)
        rect(0, 0, s, s)
        text(caption, (s*1.5, s*0.3))
        translate(width()*0.2, 0)
    
saveImage('spacing-sources.pdf')
