import json,urllib2,polyline

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
            "properties":{"active":"false"},
            "geometry":{
                "type":"LineString",
                "coordinates":polyline.encode(coords)
    }})
    coords_array.append({"parents":[],"children":[],"animFrames":[],"coords":coords,"id":c})

def traceAnimPath(coords_arr,curr,frame):
    #print(curr['id'])
    if not frame in curr['animFrames']:
        curr['animFrames'].append(frame)
    if(curr['children']):
        for i in curr['children']:
            currChild = coords_arr[i-1]
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
    maxSize = 20
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
        if not len(coords_arr[i]["parents"]) > 0:
            new_json['features'][i]['properties']['active'] = 'true'
        new_json['features'][i]['properties']['parents'] = coords_arr[i]["parents"]
        new_json['features'][i]['properties']['children'] = coords_arr[i]['children']
        new_json['features'][i]['properties']['startFrame'] = coords_arr[i]['startFrame']
        new_json['features'][i]['properties']['endFrame'] = coords_arr[i]['endFrame']
        new_json['features'][i]['properties']['animFrames'] = coords_arr[i]['animFrames']

def write_json(new_json,fname):
    with open(fname,"w") as myfile:
        myfile.write(json.dumps(new_json))

def main():
    url = "http://localhost:8000/iowanetwork.json"
    out_fname = "iowanetwork_anim.json"
    data = json.load(urllib2.urlopen(url))
    new_json,coords_arr = makeDicts(data)
    #fix for problem segment in west iowa, halfway between omaha and sioux city
    #coords_arr[1593]['coords'] = list(reversed(coords_arr[1593]['coords']))
    #fix for problem segment just south of sioux city
    #coords_arr[1592]['coords'] = list(reversed(coords_arr[1592]['coords']))
    #fix for problem segment in eastern iowa, by clinton
    #coords_arr[1598]['coords'] = list(reversed(coords_arr[1598]['coords']))
    #coords_arr[1599]['coords'] = list(reversed(coords_arr[1599]['coords']))
    #fix for problem segment just north of dubuque, tiny segment directly in
    #the middle of another segment causing problems
    #coords_arr[1600]['coords'] = list(reversed(coords_arr[1600]['coords']))
    #print(coords_arr[1593])
    makeRels(coords_arr)
    starts = getStarts(coords_arr)
    #second half of fix for problem segment north of dubuque
    #coords_arr[1334]['parents'] = [1538]
    #coords_arr[1334]['children'] = []
    #coords_arr[1537]['parents'] = [566,1601]
    #coords_arr[1334]['animFrames'] = [0]
    makeFrames(starts,coords_arr)
    addProps(coords_arr,new_json)
    write_json(new_json,out_fname)
    #r = findSegs(41.88149,-90.15267,41.88147, -90.15269,coords_arr)
    #for i in r:
     #   print(str(i)+"\n")
    #print(coords_arr[1592])
main()

