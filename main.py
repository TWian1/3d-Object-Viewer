from math import floor, tan, sin, cos, sqrt
def main():
    for a in range(100):
        background = background_maker(100,60)
        tris = olddraw(openobj("teapot"), 100, 60, rotate="y", angle=(a/2),lightloc=[0, 1,-1])
        for tri in tris: filltri(background, tri, tri[3])
        for a in imgPrint(background, pre=True): print(a)
        print(f'\033[{30}A', end='\x1b[2K')
def olddraw(render_object, width, height, rotate, angle, lightloc = [0, 1, -1]):
  alldraw = []
  for tri in render_object:
    triprojected = tritranslated = newtri = [[0,0,0],[0,0,0],[0,0,0]]
    for a in range(3): td.Multiplymatrix(tri[a], newtri[a], rotations.rotate(rotate, angle))
    for a in range(3): newtri[a][1] = newtri[a][1]*-1
    for a in range(3): tritranslated[a][2] = newtri[a][2] + 2
    normal,line1,line2 = [0,0,0],td.vector_sub(tritranslated[1], tritranslated[0]),td.vector_sub(tritranslated[2], tritranslated[0])
    for a in range(3): normal[a] = line1[(a+1)%3]*line2[(a+2)%3] - line1[(a+2)%3]*line2[(a+1)%3]
    normal = td.normalize(normal)
    if normal[2] < 0:
      light_direction = td.normalize(lightloc)
      dp = max(round(td.dotprod(normal, light_direction)*230),0)+25
      for a in range(3):td.Multiplymatrix(tritranslated[a], triprojected[a], rotations.projection())
      for a in range(6):triprojected[floor(a/2)][a%2] = (triprojected[floor(a/2)][a%2]+1.0)*((width+height)/4)
      triprojected.append([dp, dp, dp, 255])
      alldraw.append(triprojected)
  alldraw.sort(key=lambda tri:(tri[0][2] + tri[1][2] + tri[2][2]))
  return alldraw
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
def background_maker(x, y='default', color=[0,0,0,0]):
  out = []
  if y == 'default': y = x
  for a in range(y*x):
    if a%x==0:out.append([])
    out[floor(a/x)].append(color)
  return out
def openobj(filename):
  file,verts,faces,out,maximum = open(filename + ".txt").readlines(),[],[],[],0
  for a in file:
    if a[0] == 'v': verts.append([float(x) for x in a[2:][:-1].split(' ')])
    elif a[0] == 'f': faces.append([int(x) for x in a[2:][:-1].split(' ')])
  for a in verts:
    if max([abs(b) for b in a]) > maximum: maximum = max([abs(b) for b in a])
  for b in faces:
    out.append([])
    for c in b: out[len(out)-1].append([q/maximum for q in verts[c-1]])
  return out
class rotations:
  def rotate(dir, angle): 
    dirs=[[1,0,0,0],[0,cos(angle*0.5),sin(angle*0.5),0],[0,-sin(angle*0.5),cos(angle*0.5),0],[0,0,0,1]],[[cos(angle),0,sin(angle),0],[0,1,0,0],[-sin(angle),0,cos(angle),0],[0,0,0,1]],[[cos(angle),sin(angle),0,0],[-sin(angle),cos(angle),0,0],[0,0,1,0],[0,0,0,1]]
    return dirs[["x", "y", "z"].index(dir)]
  def projection(height=1, width=1):
    fNear,fFar,fFov = 1.0, 1000.0, 90.0
    fFovRad,fAspectRatio = 1.0/tan(fFov*0.5),height/width
    matrix = [[fAspectRatio*fFovRad,0,0,0],[0,fFovRad,0,0],[0,0,fFar / (fFar-fNear),(-fFar*fNear)/(fFar-fNear)],[0,0,1,0]]
    return matrix
def filltri(list, coords, color, rounded = True):
  if rounded: x1,y1,x2,y2,x3,y3 =  round(coords[0][0]),round(coords[0][1]),round(coords[1][0]),round(coords[1][1]),round(coords[2][0]),round(coords[2][1])
  minx, miny, maxx, maxy, A = min(x1, x2, x3), min(y1, y2, y3), max(x1, x2, x3), max(y1, y2, y3), area(x1, y1, x2, y2, x3, y3)
  if round(maxy) == round(miny) and round(maxx) == round(minx): 
    try:list[round(maxy)][round(maxx)] = color
    except:pass
    return 0
  for y in range(len(list)):
    if y > maxy:break
    if y < miny:continue
    for x in range(len(list[0])):
      if x > maxx:break
      if x < minx:continue
      if A == area(x, y, x2, y2, x3, y3) + area(x1, y1, x, y, x3, y3) + area(x1, y1, x2, y2, x, y): list[y][x] = color
def area(x1, y1, x2, y2, x3, y3): return abs((x1*(y2-y3) + x2*(y3-y1)+ x3*(y1-y2))/2.0)
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
if __name__ == "__main__":
  main()
