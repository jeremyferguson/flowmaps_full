import json,urllib2,polyline
import time #temporary

start = int(round(time.time() * 1000))
url = "http://localhost:8000/iowanetwork.json"
out_fname = "iowanetwork_anim.json"

data = json.load(urllib2.urlopen(url))
new_json = {'type':'FeatureCollection','features':[],'properties':data['properties']}
coords_arr = []
maxSize = 20
def isParent(a,b):
    #a is a parent of b if a's head touches b's tail( or anywhere along b except the head)
    #first compare head to head to make sure they are in the same area
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

c = 1
for geo in data['geometry']['geometries']:
    coords_temp = polyline.decode(geo['coordinates'])
    if len(coords_temp) < maxSize:
        addFeat(new_json,coords_arr,coords_temp,c)
        c+=1
    else:
        for i in range(0,len(coords_temp),maxSize):
            addFeat(new_json,coords_arr,coords_temp[i:i+maxSize+1],c)
            c+=1
    
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
j = 0
k = 0
print(len(coords_arr))
starts = []
#quick fixes
'''coords_arr[30]['parents'] = [31]
coords_arr[76]['children'] = []
coords_arr[32]['parents'] = [33]
coords_arr[32]['children'] = [861]
coords_arr[55]['parents'] = [56]
coords_arr[55]['children'] = [861]
coords_arr[861]['parents'] = [55,32]
print(coords_arr[161])
print(coords_arr[175])
print(coords_arr[176])'''

for c in coords_arr:
    if not c['parents']:
        starts.append(c)
        
def traceAnimPath(curr,frame):
    #print(curr['id'])
    if not frame in curr['animFrames']:
        curr['animFrames'].append(frame)
    if(curr['children']):
        for i in curr['children']:
            traceAnimPath(coords_arr[i-1],frame+1)
            
def shiftChildren(curr,shift):
    curr['startFrame'] += shift
    curr['endFrame'] += shift
    if curr['children']:
        for i in curr['children']:
            shiftChildren(coords_arr[i-1],shift)
            
def shiftAnimFrames(curr):
    if curr['endFrame'] - curr['startFrame'] > 0:
        print('New shift')
        print(curr['id'])
        print(curr['endFrame'] - curr['startFrame'])
        if curr['children']:
            for i in curr['children']:
                shiftChildren(coords_arr[i-1],curr['endFrame']-curr['startFrame'])
    if curr['children']:
        for i in curr['children']:
            shiftAnimFrames(coords_arr[i-1])
for head in starts:
    traceAnimPath(head,0)
for coords in coords_arr:
    #print(coords['id'])
    #print(coords['parents'])
    #print(coords['children'])
 #   print(coords['animFrames'])
    coords['startFrame'] = min(coords['animFrames'])
    coords['endFrame'] = max(coords['animFrames'])
#for head in starts:
 #   shiftAnimFrames(head)
#print(len(coords_arr))
for i in range(len(coords_arr)):
    if len(coords_arr[i]["parents"]) > 0:
        j += 1
    else:
        new_json['features'][i]['properties']['active'] = 'true'
    if len(coords_arr[i]['children']) > 0:
        k += 1
    new_json['features'][i]['properties']['parents'] = coords_arr[i]["parents"]
    new_json['features'][i]['properties']['children'] = coords_arr[i]['children']
    new_json['features'][i]['properties']['startFrame'] = coords_arr[i]['startFrame']
    new_json['features'][i]['properties']['endFrame'] = coords_arr[i]['endFrame']
    new_json['features'][i]['properties']['animFrames'] = coords_arr[i]['animFrames']
    
print(coords_arr[0])
print(k)
for c in coords_arr:
    if len(c['children']) > 1:
        print(c)
with open(out_fname,"w") as myfile:
    myfile.write(json.dumps(new_json))
end = int(round(time.time() * 1000))    
print(end-start)
