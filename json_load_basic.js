iowadata.network.setMap(null);
$.getJSON("http://localhost:8000/_smaller_exp_net_h4.geojson",function(a){
	iowadata.network = new google.maps.Data;
	iowadata.network.addGeoJson(a);
	iowadata.network.setMap(map);
	iowadata.network.setStyle(function(feature){
		color = "rgba(0,0,0,255)";
		return({
			strokeColor:color,
			strokeWeight:1,
			strokeOpacity:1,
			clickable: !1
		})
	})
	iowadata.network.idPropertyName = "true";
})