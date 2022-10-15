from math import floor, tan, sin, cos, sqrt
def main():
  matProj = rotations.projection
  Cubetris = openobj("teapot")
  width = 64
  height = 48
  background = background_maker(width, height)
  angle = 0
  while 1:
  #for f in range(100):
    alldraw = []
    angle += 0.5
    background = background_maker(width, height)
    alldraw = displaymid([], Cubetris, angle, width, height, ["x"])
    for triproj in alldraw:
      drawtri(background, round(triproj[0][0]), round(triproj[0][1]), round(triproj[1][0]), round(triproj[1][1]), round(triproj[2][0]), round(triproj[2][1]), fill=True, fillcolor=triproj[3], color=triproj[3])
    for a in imgPrint(background, pre=True): print(a)
    print(f'\033[{24}A', end='\x1b[2K')


def zerolist(x, y=0, two = False):
  out = []
  if two:
    for a in range(x*y):
      if a%x==0:out.append([])
      out[floor(a/x)].append(0)
  else:
    for a in range(x): out.append(0)
  return out
def displaymid(list, render_object, angle, width, height, rotate, pre=True):
  alldraw = []
  for tri in render_object:
    triprojected = trirx = newtri = zerolist(3, 3, True)
    for a in rotate:
      newtri = tri
      if a == "x":
        for a in range(3): td.Multiplymatrix(newtri[a], trirx[a], rotations.x(angle))
        newtri = trirx
      if a == "z":
        for a in range(3): td.Multiplymatrix(newtri[a], trirx[a], rotations.z(angle))
        newtri = trirx
      if a == "y":
        for a in range(3): td.Multiplymatrix(newtri[a], trirx[a], rotations.y(angle))
        newtri = trirx
    for a in range(3):
      newtri[a][1] = newtri[a][1]*-1
    tritranslated = newtri
    for a in range(3): tritranslated[a][2] = trirx[a][2] + 2
    normal,line1,line2 = zerolist(3),td.vector_sub(tritranslated[1], tritranslated[0]),td.vector_sub(tritranslated[2], tritranslated[0])
    for a in range(3): normal[a] = line1[(a+1)%3]*line2[(a+2)%3] - line1[(a+2)%3]*line2[(a+1)%3]
    normal = td.normalize(normal)
    if normal[2] < 0:
      light_direction = td.normalize([0, 0, -1])
      dp = round(td.dotprod(normal, light_direction)*230)+25
      for a in range(3):td.Multiplymatrix(tritranslated[a], triprojected[a], rotations.projection(width, height))
      for a in range(6):triprojected[floor(a/2)][a%2] = (triprojected[floor(a/2)][a%2]+1.0)*((width+height)/4)
      triprojected.append([dp, dp, dp, 255])
      alldraw.append(triprojected)
  alldraw.sort(key=lambda tri:(tri[0][2] + tri[1][2] + tri[2][2]))
  return alldraw
class rotations:
  def x(angle): return [[1, 0, 0, 0],[0, cos(angle*0.5), sin(angle*0.5), 0],[0, -sin(angle*0.5), cos(angle*0.5), 0],[0,0,0,1]]
  def z(angle): return [[cos(angle), sin(angle), 0, 0],[-sin(angle), cos(angle), 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]]
  def y(angle): return [[cos(angle), 0, sin(angle), 0],[0, 1, 0, 0],[-sin(angle), 0, cos(angle), 0],[0, 0, 0, 1]]
  def projection(height, width):
    fNear = 1.0
    fFar = 1000.0
    fFov = 90.0
    fAspectRatio = height/width
    fFovRad = 1.0/tan(fFov*0.5)
    matrix = [
    [fAspectRatio*fFovRad,0, 0, 0],
    [0, fFovRad, 0, 0],
    [0, 0, fFar / (fFar-fNear), (-fFar*fNear) / (fFar-fNear)],
    [0, 0, 1, 0]]
    return matrix
class td:
  def Multiplymatrix(i, o, m):
    o[0] = i[0] * m[0][0] + i[1] * m[1][0] + i[2] * m[2][0] + m[3][0]
    o[1] = i[0] * m[0][1] + i[1] * m[1][1] + i[2] * m[2][1] + m[3][1]
    o[2] = i[0] * m[0][2] + i[1] * m[1][2] + i[2] * m[2][2] + m[3][2]
    w = i[0] * m[0][3] + i[1] * m[1][3] + i[2] * m[2][3] + m[3][3]
    if w != 0: o = td.vector_div(o, w)
  def vector_add(list1, list2): return [list1[0]+list2[0], list1[1]+list2[1], list1[2]+list2[2]]
  def vector_sub(list1, list2): return [list1[0]-list2[0], list1[1]-list2[1], list1[2]-list2[2]]
  def vector_mul(list1, a): return [list1[0]*a, list1[1]*a, list1[2]*a]
  def vector_div(list1, a): return [list1[0]/a, list1[1]/a, list1[2]/a]
  def dotprod(list1, list2): return list1[0]*list2[0] + list1[1]*list2[1] + list1[2]*list2[2]
  def length(list1): return sqrt(td.dotprod(list1, list1))
  def normalize(list1): return td.vector_div(list1, td.length(list1))
def drawtris(list, set, color=[255,255,255,255], gen=False, bgcolor=[0,0,0,0]):
  if gen:
    list = []
    maxy, maxx, miny, minx = max([max([x[1] for x in y]) for y in set]), max([max([x[0] for x in y]) for y in set]), min([min([x[1] for x in y]) for y in set]), min([min([x[0] for x in y]) for y in set])
    for a in range(maxy - miny * (maxx - minx)):
      if a % (maxx - minx) == 0: list.append([])
      list[floor(a/(maxx - minx))].append(bgcolor)
    for a in set: drawtri(list, a[0][0]-minx, a[0][1]-miny, a[1][0]-minx, a[1][1]-miny, a[2][0]-minx, a[2][1]-miny) 
    return list
  else: 
    for a in set: drawtri(list, a[0][0], a[0][1], a[1][0], a[1][1], a[2][0], a[2][1])
def background_maker(x, y='default', color=[0,0,0,0]):
  out = []
  if y == 'default': y = x
  for a in range(y*x):
    if a%x==0:out.append([])
    out[floor(a/x)].append(color)
  return out
def openobj(filename):
  file = open(filename + ".txt").readlines()
  verts = []
  faces = []
  for a in file:
    if a[0] == 'v': verts.append([float(x) for x in a[2:][:-1].split(' ')])
    if a[0] == 'f': faces.append([int(x) for x in a[2:][:-1].split(' ')])
  out = []
  maximum = 0
  for a in verts:
    if max([abs(b) for b in a]) > maximum: maximum = max([abs(b) for b in a])
  for b in faces:
    out.append([])
    for c in b:
      out[len(out)-1].append([q/maximum for q in verts[c-1]])
  return out
def setpix(list,x,y,color=[255,255,255,255]):
  try:list[y][x] = color 
  except:pass
def setline(list,x,y,x2,y2,color=[255,255,255,255],p='default',gen=False, alr = False, lim = 1000): 
  if gen: 
    if x < x2: x,x2 = 0, x2-x
    else: x2,x = 0, x-x2
    if y < y2: y,y2 = 0, y2-y
    else: y2,y = 0, y-y2
    list = []
    for a in range(round(abs(y2-y)+1)*round(abs(x2-x)+1)):
      if a%round(abs(x2-x))==0:list.append([])
      list[floor(a/round(abs(x2-x)))].append([0,0,0,0])
  if (x == x2 and y == y2) or (abs(x-x2) <= 1 and abs(y-y2) <=1 ):
    list[y][x] = color
    if gen:return list
    else: return 0
  if x2-x == 0:
    if y2 > y: vert = 1
    else: vert = -1
    yinter = y
  else:
    vert =0
    s=(y2-y)/(x2-x)
    yinter = (x*y2 - x2*y)/(x-x2)
  s2 = 1
  if x2-x < 0: s2 = -1
  xpos,ypos, = x,y
  if p == 'default': p = 70
  toprint = []
  lypos = -1
  lxpos = -1
  while(xpos < len(list[0])+lim and xpos > 0-lim and ypos < len(list)+lim and ypos > 0-lim):
    if vert == 0:
      xpos += (1/p)*s2
      ypos = (xpos*s)+yinter
      if round(xpos) == lxpos and round(ypos) == lypos: continue
      lypos,lxpos = round(ypos),round(xpos)
    else: 
      ypos += vert
      xpos += (1/len(list))*s2
    
    if (round(xpos) == x2 and round(ypos) == y2) or (abs(xpos-x2) <= 1 and abs(ypos-y2) <=1):
      toprint.append([round(xpos), round(ypos)])
      break
    toprint.append([round(xpos), round(ypos)])
  for a in toprint: setpix(list, a[0], a[1],color)
  if gen: return list

def upscale(pixelsarray, scale, limx, limy):
  out = []
  for a in range(len(pixelsarray)*scale):
    out.append([])
    for b in range(len(pixelsarray[0])*scale):out[a].append([])
  for a in range(len(pixelsarray)):
    for b in range(len(pixelsarray[0])):
      for c in range(scale):
        for d in range(scale): out[(a*scale)+c][(b*scale)+d] = pixelsarray[a][b]
  return out
def drawtri(list, x1, y1, x2, y2, x3, y3, color=[255, 255, 255, 255], gen=False, bgcolor = [0, 0, 0, 0], fill = False, fillcolor = [255, 255, 255]):
  if gen:
    list = []
    for a in range((max([y1, y2, y3]) - min([y1, y2, y3])) * (max([x1, x2, x3]) - min([x1, x2, x3]))):
      if a % (max([x1, x2, x3]) - min([x1, x2, x3])) == 0: list.append([])
      list[floor(a/(max([x1, x2, x3]) - min([x1, x2, x3])))].append(bgcolor)
  if fill:
    filltri(list, x1, y1, x2, y2, x3, y3, fillcolor)
    if color == fillcolor: return 0
  dat = [x1, y1, x2, y2, x3,y3]
  for a in range(3): setline(list, dat[a*2], dat[(a*2)+1], dat[((a*2)+2) % 6], dat[(((a*2)+2) % 6)+1], color=color)
  if gen: return list
def filltri(list, x1, y1, x2, y2, x3, y3, color):
  minx, miny, maxx, maxy, A = min(x1, x2, x3), min(y1, y2, y3), max(x1, x2, x3), max(y1, y2, y3), area(x1, y1, x2, y2, x3, y3)
  for y in range(len(list)):
    if y > maxy:break
    if y < miny:continue
    for x in range(len(list[0])):
      if x > maxx:break
      if x < minx:continue
      if A == area(x, y, x2, y2, x3, y3) + area(x1, y1, x, y, x3, y3) + area(x1, y1, x2, y2, x, y): list[y][x] = color
def area(x1, y1, x2, y2, x3, y3):
  return abs((x1*(y2-y3) + x2*(y3-y1)+ x3*(y1-y2))/2.0)
def acol(list, col=[0, 0, 0]): return combine(background_maker(len(list[0]), len(list)), list, 0, 0, 255)
def imgPrint(pixelsarray,pre=False):
  height,width,total = len(pixelsarray),len(pixelsarray[0]),[]
  for a in range(floor(height/2)):
    string_temp = ""
    for b in range(width):
      clr = [0,0,0,0,0,0]
      try:
        for c in range(3): clr[c] = pixelsarray[floor(a*2)+1][floor(b)][c]
        for c in range(3): clr[c+3] = pixelsarray[floor(a*2)][floor(b)][c]
      except Exception: pass
      string_temp += f"\033[38;2;{clr[0]};{clr[1]};{clr[2]}m\033[48;2;{clr[3]};{clr[4]};{clr[5]}m▄\033[0m"
    if pre == False: print(string_temp)
    else: total.append(string_temp)
  if pre: return total
def combine(original, image, x, y, alpha=255):
  orig = original
  for a in range(len(original)):
    for b in range(len(original[0])):
      if a >= y and b >= x and b <= x+len(image[0]) and a<=y+len(image):
        try:
          alpha2 = (image[a-y][b-x][3]/255)*(alpha/255)
          orig[a][b] = [round((orig[a][b][z]*(1-alpha2))+(image[a-y][b-x][z] * alpha2)) for z in range(3)]
        except Exception: pass
  return orig
def videoPrint(arrays, slow=1):
  for x in arrays:
    print(len(x))
    upcurs = int(len(x)+3)
    for a in range(slow):
      for b in x: print(b)
      print(f'\033[{upcurs}A', end='\x1b[2K')
def textgen(text, text_color=[255, 255, 255], text_opacity=255, background_opacity=0,  background_color=[0,0,0], return_size=False):
  valtext = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789,./\\?!()+-_:;'\""
  data = ['100000110000011000001011111001000100100010001010000101000001000', '011011001111001001111000101110', '111111010000011000001100000110000101111100100001010000101111100', '111101000110001111101000010000', '001111001000011000000100000010000001000000100000001000010011110', '011101000110000100001000101110', '111110010000101000001100000110000011000001100000110000101111100', '011111000110001011110000100001', '111111110000001000000100000011111111000000100000010000001111111', '011101000111100100101000101110', '100000010000001000000100000011111111000000100000010000001111111', '010001000100111001000011', '001110001000101000001100000110011101000000100000001000000011100', '011100000101111100011001101101', '100000110000011000001100000111111111000001100000110000011000001', '100011000111001101101000010000', '111111100010000001000000100000010000001000000100000010001111111', '111101', '011111010000010000001000000100000010000001000000100000010000001', '011101000100001000010000000001', '100000110000101000100100100011100001001000100010010000101000001', '100110101100101010011000', '111111110000001000000100000010000001000000100000010000001000000', '011010101010', '100000110010011001001101010110101011010101110001111000111000001', '1010110101101011101010000', '100000110000111000101100010110010011010001101000111000011000001', '1000110001100011100110110', '011111010000011000001100000110000011000001100000110000010111110', '0111010001100011000101110', '100000010000001000000111111010000011000001100000110000010111110', '100010001110100110010110', '001110101000101000101100000110000011000001100000101000100011100', '000110001001110100101001001100', '100001100010100100101000111110100001100001100001011110', '1000010000100001100010111', '111111000000010000001000000101111101000000100000010000000111111', '11100001011010000111', '000100000010000001000000100000010000001000000100000010001111111', '001010010010111010', '011111010000011000001100000110000011000001100000110000011000001', '0111110001100011000110001', '000100000101000010100010001001000100100010100000110000011000001', '0010001010100011000110001', '010001010101011010101101010110101011001001100000110000011000001', '0101010101101011000110001', '100000110000010100010001010000010000010100010001010000011000001', '1000101010001000101010001', '000100000010000001000001010001000100100010100000110000011000001', '011101000100001011111000110001', '111111110000000100000001000000010000000100000001000000011111111', '111111000001000001000001011111', '011111010000111000101100010110010011010001101000111000010111110', '111111100010000001000000100000010001001000010100000110000001000', '011111110000001000000100000001111100000001000000100000011111110', '111111000000010000001000000100111100000001000000100000011111110', '000010000001000000100000010001111111000100100010010001001000100', '011111010000010000001000000101111101000000100000010000001111111', '011111010000011000001100000111111101000000100000001000000011110', '100000001000000010000000100000001000000010000000100000011111111', '011111010000011000001100000101111101000001100000110000010111110', '011100000001000000010000000101111111000001100000110000010111110', '11', '1', '100001000001000010000010000010000100000100001', '000010000100010000100010001000010001000010000', '001000000000100001000001000001000010000111110', '101111111', '001010010100100100010010001', '100010010001001001010010100', '000000000000010000100111100010000100000000000', '000000000000000000000111100000000000000000000', '011111100000000000000000000000000000000000000000000000000000000', '000000000', '000100000000000000', '000000000', '000000000000000000010010000', '011111101000000100100010000001001000100010010111001000000111111']
  datas = [[7,9,0], [5,6,0], [7,9,0], [5,6,0], [7,9,0], [5,6,0], [7,9,0], [5,6,0], [7,9,0], [5,6,0], [7,9,0], [4,6,0], [7,9,0], [5,6,-1], [7,9,0], [5,6,0], [7,9,0], [1,6,0], [7,9,0], [5,6,-1], [7,9,0], [4,6,0], [7,9,0], [2,6,0], [7,9,0], [5,5,0], [7,9,0], [5,5,0], [7,9,0], [5,5,0], [7,9,0], [4,6,-1], [7,9,0], [5,6,-1], [6,9,0], [5,5,0], [7,9,0], [4,5,0], [7,9,0], [3,6,0], [7,9,0], [5,5,0], [7,9,0], [5,5,0], [7,9,0], [5,5,0], [7,9,0], [5,5,0], [7,9,0], [5,6,-1], [7,9,0], [5,6,0], [7,9,0], [7,9,0], [7,9,0], [7,9,0], [7,9,0], [7,9,0], [7,9,0], [7,9,0], [7,9,0], [7,9,0], [1,2,0], [1,1,0], [5,9,0], [5,9,0], [5,9,0], [1,9,0], [3,9,0], [3,9,0], [5,9,0], [5,9,0], [7,9,0], [1,9,0], [2,9,0], [1,9,0], [3,9,0], [7,9,0]]
  #          A         a        B        b        C        c        D        d        E        e        F        f        G         g       H         h        I        i        J        j         K        k        L        l        M        m        N        n        O        o        P         p        Q         q        R        r        S        s        T        t        U        u        V        v        W        w        X         x       Y        y         Z         z       0        1        2        3        4        5        6        7        8        9        ,         .       /        \        ?         !       (         )       +        -        _        :         ;        '        "     missing
  total_length, total_height,indexes,out,curlength = 1,0,[],[],1
  for a in text:
    if a == " ":
      indexes.append(-1)
      total_length += 4
    else:
      try: index = valtext.index(a)
      except: index = 77
      if datas[index][1] > total_height-2: total_height = datas[index][1]+2
      total_length += ((datas[index][0]) + 1)
      indexes.append(index)
  for a in range(total_height):
    out.append([])
    for b in range(total_length): out[a].append([background_color[0], background_color[1], background_color[2], background_opacity])
  for a in indexes:
    if a == -1:
      curlength += 4
      continue
    for b in range(datas[a][1]):
      for c in range(datas[a][0]):
        x = (b*datas[a][0]) + c
        if data[a][x] == "1": out[(total_height-b)-2][c+curlength] = [text_color[0], text_color[1], text_color[2], text_opacity]
    curlength += datas[a][0]+1
  if return_size: return out, total_length, total_height
  return out

if __name__ == "__main__":
  main()
