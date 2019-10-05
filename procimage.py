from PIL import Image
import io
import os
import zipfile
import time

def transimg(path, filename, key, xsize, ysize, pixsize, grid, maxxy):
    try:
        maxxy = int(maxxy)
        xsize = int(xsize)
        ysize = int(ysize)
        if xsize <= 0:
            xsize = 1
        elif xsize > maxxy:
            xsize = maxxy
        if ysize <= 0:
            ysize = 1
        elif ysize > maxxy:
            ysize = maxxy
    except:
        xsize = 100
        ysize = 100

    filelocal = os.path.join(path + "/uploads/" + filename)
    im = Image.open(filelocal)
    im = im.resize((xsize, ysize), Image.NEAREST)
    pp = list(im.getdata())
    nb = ""
    for x in range(0, xsize):
        nb += "auto "
    nb = nb + ";"

    css1 = """.grid-item {"""
    css2 = ""
    if grid == "yes":
        css2 = """border: 1px solid rgba(0, 0, 0, 0.1);"""
    css3 = """
      padding: """
    padding = pixsize
    css4 = """px;
      font-size: 1px;
      text-align: center;
    }
.grid-container {
      width:100%
      margin: 0 auto;
      display: inline-grid;
      grid-template-columns:"""
    css = css1 + css2 + css3 + padding + css4 + nb + "}"
    pixel = []
    for x in range(0,(xsize*ysize)):
        R = pp[x][0]
        G = pp[x][1]
        B = pp[x][2]
        pixelValue = (R, G, B, 0.8)
        pixel.append(pixelValue)
    generatestaticpage(css, pixel, key, path)

    return (css, pixel)

def generatestaticpage(css, pixel, key, path):
    tempfile = str(key)
    f = open(path + '/output/' + tempfile + '.html', 'w+')
    e1 = """<!DOCTYPE html>
    <html>
    <style>
"""
    e2 = """    
    </style>
        <body>
            <div class="grid-container">    
    """
    f.write(e1)
    f.write(css)
    f.write(e2)
    for pixelv in pixel:
        el = '             <div class="grid-item" style="background-color: rgba' + str(pixelv) + '"></div>' + "\r\n"
        f.write(el)
    f.write('</div></body></html>')
    f.close()
    zipfile.ZipFile(path + '/output/' + tempfile + ".zip", mode='w').write\
        (path + '/output/' + tempfile + '.html', 'static_page.html',
         compress_type=zipfile.ZIP_DEFLATED)
    os.remove(path + '/output/' + tempfile + '.html')