import json,urllib2,polyline,math
import time
start = int(round(time.time() * 1000))
def isParent(a,b):
    if(abs(a['coords'][0][0]-b['coords'][0][0])<1.0 and abs(a['coords'][0][1]-b['coords'][0][1])<1.0):
        for i in range(1,len(b['coords'])):
            if(abs(a['coords'][0][0] - b['coords'][i][0])< 0.001 and abs(a['coords'][0][1] - b['coords'][i][1])<0.001):
                return(True)
        return(False)
    else:
        return(False)

def addFeat(full_json,coords_array,coords,c):
    full_json['features'].append({
            "type":"Feature",
            "id":c,
            "properties":{"active":"false","weight":1},
            "geometry":{
                "type":"LineString",
                "coordinates":polyline.encode(coords)
    }})
    coords_array.append({"branches":1,"parents":[],"children":[],"animFrames":[],"coords":coords,"id":c})

def traceAnimPath(coords_arr,curr,frame):
    #print(curr['id'])
    if len(curr['parents']) > 1:
        curr['branches'] += len(curr['parents']) - 1
    if not frame in curr['animFrames']:
        curr['animFrames'].append(frame)
    active = curr
    for a in range(1):
        if len(active['children']) > 0:
            active = coords_arr[active['children'][0]-1]
            if not frame in active['animFrames']:
                active['animFrames'].append(frame)
    if(curr['children']):
        for i in curr['children']:
            currChild = coords_arr[i-1]
            currChild['branches'] = max([coords_arr[i-1]['branches'] for i in currChild['parents']])
            traceAnimPath(coords_arr,currChild,frame+1)
            
def findSegs(north,east,south,west,coords_arr):
    results = []
    for c in coords_arr:
        for point in c['coords']:
            if point[0] < east and point[0] > west and point[1] < north and point[1] > south:
                results.append(c)
                break
    return(results)

def makeDicts(data):
    new_json = {'type':'FeatureCollection','features':[],'properties':data['properties']}
    coords_arr = []
    c = 1
    maxSize = 10
    for geo in data['geometry']['geometries']:
        coords_temp = polyline.decode(geo['coordinates'])
        #Fixes for a few problem segments
        prob_segs = [(-96.0926,41.7128),(-96.35266,42.22678),(-90.14678,41.88502),(-90.77557, 42.6672)]
        for pr in prob_segs:
            if pr in coords_temp:
                coords_temp = list(reversed(coords_temp))
        #Removes super weird segment that is tiny and in the middle of the mississippi river
        if not (-90.67616, 42.59908) in coords_temp :
            if len(coords_temp) < maxSize:
                addFeat(new_json,coords_arr,coords_temp,c)
                c+=1
            else:
                for i in range(0,len(coords_temp),maxSize):
                    addFeat(new_json,coords_arr,coords_temp[i:i+maxSize+1],c)
                    c+=1
    return((new_json,coords_arr))

def makeRels(coords_arr):
    for i in range(len(coords_arr)):
        j = 0
        foundChild = False
        while j < len(coords_arr) and not foundChild:
            if(i!=j) and isParent(coords_arr[i],coords_arr[j]):
                if not j+1 in coords_arr[i]["parents"] and not i+1 in coords_arr[j]["children"]:
                    foundChild = True
                    coords_arr[i]["children"].append(j+1)
                    coords_arr[j]["parents"].append(i+1)
            j+=1
        
def getStarts(coords_arr):
    starts = []
    for c in coords_arr:
        if not c['parents']:
            starts.append(c)
    return(starts)

def makeFrames(starts,coords_arr):
    for head in starts:
        traceAnimPath(coords_arr,head,0)
    for coords in coords_arr:
        coords['startFrame'] = min(coords['animFrames'])
        coords['endFrame'] = max(coords['animFrames'])

def addProps(coords_arr,new_json):
    for i in range(len(coords_arr)):
        #if not len(coords_arr[i]["parents"]) > 0:
         #   new_json['features'][i]['properties']['active'] = 'true'
        new_json['features'][i]['properties']['parents'] = coords_arr[i]["parents"]
        new_json['features'][i]['properties']['children'] = coords_arr[i]['children']
        new_json['features'][i]['properties']['startFrame'] = coords_arr[i]['startFrame']
        new_json['features'][i]['properties']['endFrame'] = coords_arr[i]['endFrame']
        new_json['features'][i]['properties']['animFrames'] = coords_arr[i]['animFrames']
        new_json['features'][i]['properties']['weight'] = math.ceil(coords_arr[i]['branches']/7.0)

def write_json(new_json,fname):
    with open(fname,"w") as myfile:
        myfile.write(json.dumps(new_json))

def makeAnimArray(coords_arr):
    animArr = [[]]
    for seg in coords_arr:
        eFrame = max(seg['animFrames'])
        for i in range(len(animArr)-1,eFrame):
            animArr.append([])
        for i in seg['animFrames']:
            animArr[i].append(seg['id'])
    return(animArr)

def writeAnimArr(animArr,fname):
    with open(fname,"w") as myfile:
        for i in animArr:
            myfile.write(" ".join([str(a) for a in i])+"\n")
def main():
    url = "http://localhost:8000/iowanetwork.json"
    out_fname = "iowanetwork_anim.json"
    animArr_fname = "iowanetwork_animarr.txt"
    data = json.load(urllib2.urlopen(url))
    new_json,coords_arr = makeDicts(data)
    makeRels(coords_arr)
    starts = getStarts(coords_arr)
    makeFrames(starts,coords_arr)
    addProps(coords_arr,new_json)
    write_json(new_json,out_fname)
    animArr = makeAnimArray(coords_arr)
    writeAnimArr(animArr,animArr_fname)
main()
end = int(round(time.time() * 1000))
print(end-start)

