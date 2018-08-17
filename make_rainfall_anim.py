import h5py,json,polyline,requests
import numpy as np
import os,time
import pandas as pd

start = int(round(time.time() * 1000))
dir_path = os.getcwd()
json_in = "/exp_net_h4_condensed.geojson"
h5_in = "/hydrograph_mrms_et_hrrr_1520514000.h5"
out_fname = "/rainfall_network_anim.geojson"

def normalize(arr):
    _min = min(arr)
    _max = max(arr)
    _range = _max - _min
    return((arr-_min)/(_range))

f = h5py.File(dir_path+h5_in,'r')
for key in f.keys():
    dataset = f[key]
#print(f.get('outputs'))
issue_time = f.attrs['issue_time'][0]
linkids = pd.unique(dataset['LinkID'])
linkids = np.reshape(linkids,(-1,1))
times = pd.unique(dataset['TimeI'])
states = np.reshape(dataset['State0'],(-1,times.size))
#normalized = np.apply_along_axis(normalize,1,states)
#states = normalized
f.close()
#print(states.shape)
#print(linkids.shape)
flow_ix_class_normalize = [i/7.0 for i in range(8)]
flow_ix_class = [0.0, 0.2, 0.5, 1, 2, 3, 4, 8, 10000000000]
def getClassified (_data, _classes = flow_ix_class):
    _return = np.zeros( _data.shape, np.uint8)
    for color_ix in range(len(_classes)-1):
        mask = np.logical_and(_data >= _classes[color_ix], _data < _classes[color_ix+1])
        _return[mask] = color_ix
    return _return

def compressRow(row):
    out_str = "0"+str(row[0])
    for i in range(1,len(row)):
        if(row[i] != row[i-1]):
            out_str+=("|"+str(i)+str(row[i]))
    return(out_str)

def write_json(new_json,fname):
    with open(fname,"w") as myfile:
        myfile.write(json.dumps(new_json,separators=(',',':')))
        
classified = getClassified(states,flow_ix_class)
inst = np.unique(classified[:,0],return_counts = True)[1]
print(inst)
#print(np.amin(classified))
#print(classified.shape)
#full_arr = np.concatenate((linkids,classified),axis = 1)
#print(full_arr)
with open(dir_path+json_in,"r") as myfile:
    jsondoc = json.load(myfile)

new_json = {'type':'FeatureCollection','features':[],'name':'rainfall_network_anim',"crs":jsondoc['crs']}
i = 1
for feat in jsondoc['features']:
    lid = feat['properties']['link_id']
    pos = np.where(linkids == lid)[0][0]
    #print(i)
    currRow = classified[pos]
    output = compressRow(currRow)
    if i%5000 == 0:
        print(output)
    new_json['features'].append({
        "type":"Feature",
        "id":i,
        "properties":{"frames":output},
        "geometry":{
            "type":"LineString",
            "coordinates":polyline.encode(feat['geometry']['coordinates'])
        }
    })
    i+= 1
print(i)
write_json(new_json,dir_path+out_fname)
end = int(round(time.time() * 1000))
print(end-start)
