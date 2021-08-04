import re

with open('result_text.txt') as ocr:
    Text = ocr.readlines()

CleanText = []

ne_pattern = re.compile(
    r'''
    (               
        \,*?        
        \ N\.?      
        \ ?E       
        .           
    )               
    $               
''', re.VERBOSE)

nw_pattern = re.compile(
    r'''
    (                   
        \,*?            
        \ N\.?          
        \ ?W            
        [\.\,]*?        
        _?              
    )                   
    $                   
    ''', re.VERBOSE)

for line in Text:
    dashes = re.search('(--+)', line)

    if dashes:
        nodash = re.sub('.(-+)', ',', line)
        nodots = re.sub('.(\.\.+)', '', nodash)
        nospaces = re.sub('(  +)', ',', nodots)
        nostar = re.sub('.[*]', '', nospaces)
        flushleft = re.sub('^\W', '', nostar)
        comma = re.sub(',{2,3}', ',', flushleft)
        caps = re.sub('[A-N|P-Z]{2,}', ',', comma)
        ne = re.sub(ne_pattern, ' NE', caps)
        nw = re.sub(nw_pattern, ' NW', ne)
        match = re.search('^([A-Z][a-z]+\.)', nw)
        if match:
            names = re.sub('\.', ',', nw)
        else:
            names = nw
        CleanText.append(names)

with open('rs1.csv', 'w') as fcsv:
    for line in CleanText:
        fcsv.write(line)
