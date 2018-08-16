import json,urllib2,polyline,h5py

def write_json(new_json,fname):
    with open(fname,"w") as myfile:
        myfile.write(json.dumps(new_json))

jsonurl = "http://localhost:8000/_exp_net_h4.geojson"
h5url = "http://localhost:8000/hydrograph_mrms_et_hrrr_1520514000.h5"
out_fname = "rainfall_network_anim.geojson"
jsondoc = json.load(urllib2.urlopen(jsonurl))
new_json = {'type':'FeatureCollection','name':'_exp_rainfall_anim','features':[],'crs':jsondoc['crs']}
print(len(jsondoc['features']))
for feat in jsondoc['features']:
    new_json['features'].append({
        "type":"Feature",
        "id":feat['properties']['link_id'],
        "geometry":{"type": "LineString","coordinates":polyline.encode(feat['geometry']['coordinates'])}
    })
write_json(new_json,out_fname)
    

