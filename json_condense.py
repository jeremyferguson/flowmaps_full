import json,time,os

dir_path = os.getcwd()
json_in = "/_exp_net_h4.geojson"
out_fname = "/exp_net_h4_condensed.geojson"
start = int(round(time.time() * 1000))
with open(dir_path+json_in,"r") as myfile:
    jsondoc = json.load(myfile)

#new_json = {"type": jsondoc["type"],"name":jsondoc['name'],'crs':jsondoc['crs'],'features':[]}
i = 0
for a in range(len(jsondoc['features'])):
    feat = jsondoc['features'][a-i]
    coords = feat['geometry']['coordinates']
    for coord in coords:
        if coord[1] > 43.5 or coord[0] < -96.64:
            del jsondoc['features'][a-i]
            i+= 1
            break
print(i)
for a0 in range(1):
    i = 0       
    while i <len(jsondoc['features']):
        j = 0
        feat1 = jsondoc['features'][i]
        coords1 = feat1['geometry']['coordinates']
        while j <len(jsondoc['features']):
            feat2 = jsondoc['features'][j]
            coords2 = feat2['geometry']['coordinates']
            if i != j:
                if len(coords1) < 15 and len(coords2) < 15:
                    if abs(coords1[0][0] - coords2[0][0]) < 0.02 and abs(coords1[0][1] - coords2[0][1]) < 0.02:
                        if (coords1[0][0] == coords2[-1][0] and coords1[0][1] == coords2[-1][1]) :
                            coords1 = coords2 + coords1[1:]
                            del jsondoc['features'][j]
                            j -= 1
                            if i % 100 == 0:
                                print('match at '+str(i))
                        elif (coords1[-1][0] == coords2[0][0] and coords1[-1][1] == coords2[0][1]):
                            coords1 += coords2[1:]
                            del jsondoc['features'][j]
                            j -= 1
                            if i% 100 == 0:
                                print('match at '+str(i))
            j+= 1
        i += 1
i = 0
for feat in jsondoc['features']:
    coords = feat['geometry']['coordinates']
    if len(coords)>7:
        coords = [coords[0]] + [coords[i] for i in range(1,len(coords)-1) if i%2 == 0] + [coords[-1]]
    i+=1
    
print(i)
with open(dir_path+out_fname,"w") as myfile:
    myfile.write(json.dumps(jsondoc,separators=(',',':')))
end = int(round(time.time() * 1000))
print(end-start)
