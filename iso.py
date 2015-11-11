from PIL import Image
import omg, math, time, sys
from omg import MapEditor

def test(map):
    print(len(map.linedefs))

class progress:
    def __init__(self,max):
        self.start(max)
        
    def start(self,max):
        self.prg = 0
        self.max = max
        self.starttime = time.time()
        
    def update(self):
        self.prg += 1
        update_progress(self.prg/self.max)
        
    def end(self):
        print "time elapsed: {}".format(time.time()-self.starttime)
    
def st_p(max):
    prg = 0
    prgmax = max
    
def up_p():
    prg += 1
    update_progress(prg/prgmax)
    
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
    
def draw_base_lines(map):

    # calculate bounds
    print("calculate bounds")
    prog = progress(len(map.vertexes))
    
    v1 = map.vertexes[0]
    bounds = [v1.x,v1.y,v1.x,v1.y]
    s1 = map.sectors[0]
    bound_height = [s1.z_floor,s1.z_ceil,0]
    
    for v in map.vertexes:
        
        if v.x < bounds[0]: bounds[0] = v.x
        if v.y < bounds[1]: bounds[1] = v.y
        if v.x > bounds[2]: bounds[2] = v.x
        if v.y > bounds[3]: bounds[3] = v.y
        
        prog.update()
    prog.end()
    
    
    # calculate height bounds
    print("calculate height bounds")
    prog.start(len(map.linedefs))
    for l in map.linedefs:
        va = gv(map,l.vx_a)
        vb = gv(map,l.vx_b)
        zs = get_zs(map,l)
        z1 = zs[0]
        z2 = zs[1]
        if z1 < bound_height[0]: bound_height[0] = z1
        if z2 > bound_height[1]: bound_height[1] = z2
        if (va.y - z2 < bounds[1]): bounds[1] = va.y - z2
        if (vb.y - z2 < bounds[1]): bounds[1] = va.y - z2
        if (va.y - z1 > bounds[3]): bounds[3] = va.y - z1
        if (vb.y - z1 > bounds[3]): bounds[3] = va.y - z1
        prog.update()
    mewb = ( bounds[2] - bounds[0], bounds[3] - bounds[1] )
    bound_height[2] = bound_height[1]-bound_height[0]
    prog.end()
        
    # draw map
    #bound_height *= -1
    print("bound height "+str(bound_height))
    
    print("draw map")
    prog.start(len(map.linedefs))
        
    img = Image.new("RGB",(bounds[2]-bounds[0]+1,bounds[3]-bounds[1]+1),0)
    print("image: {} {}".format(img.width,img.height))
    
    for l in map.linedefs:
        va = gv(map,l.vx_a)
        vb = gv(map,l.vx_b)
        ln = [va.x,va.y,vb.x,vb.y]
        zs = get_zs(map,l)
        xp = line_to_xpoints(ln,zs, bound_height)
        for p in xp:
            q = offset(bounds,p)
            print(q)
            img.putpixel(q,(255,0,0))
        prog.update()
    prog.end()
        
        
    img.show()
        
    
def gv(map,i):
    return map.vertexes[i]
    
def get_zs(map,line):
    s = map.sidedefs[line.front]
    sc = map.sectors[s.sector]
    z1 = sc.z_floor
    z2 = sc.z_ceil
    return (z1,z2)
    
def line_to_xpoints(line,zs,h):
    zs = (h[2]-zs[0],h[2]-zs[1])
    output = []
    if line[0] == line[2]: 
        for i in range(min(line[1],line[3]),max(line[1],line[3])):
            output.append( (line[0],i - zs[0]) )
            output.append( (line[0],i - zs[1]) )
        return output
    
    xa = line[0]
    xb = line[2]
    x1 = min(xa,xb)
    x2 = max(xa,xb)
    if xb > xa:
        y1 = line[1]
        y2 = line[3]
    else:
        y1 = line[3]
        y2 = line[1]
    w = x2-x1
    h = y2-y1
    for i in range(x1,x2 + 1):
        prc = 1.0
        prc *= (i - x1) / float(w)
        j = y1 + (h * prc)
        output.append( (int(i), int(j) - zs[0] ) )
        output.append( (int(i), int(j) - zs[1] ) )
    return output
    
def offset(b,p):
    return ( p[0] - b[0], (b[3] - p[1]))
        
    
if __name__ == "__main__":
    testwad = "test.wad"
    draw_base_lines(MapEditor(omg.WAD(testwad).maps["MAP01"]))