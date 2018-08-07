iowadata.network.setMap(null);
function animationCycle(data,animFrames,currFrame,size){
	/**var e = 0;
	//console.log('new cycle');
	for(var i = 1;i<=c;i++){
		d = b.getFeatureById(i);
		//console.log(d);
		if(d.getProperty("active") == "true"){
			if(d.getProperty("children").length > 0){
				//console.log(d.getProperty("children"));
				b.getFeatureById(d.getProperty("children")[0]).setProperty("active","true");
				d.setProperty("active","false");
				e++;
			}
		}
	}
	//console.log(e);
	if(e < Math.floor(c*0.01) || d == 0){
	for(var i = 1;i<=c;i++){
		d = b.getFeatureById(i);
		//console.log(d.getProperty("parents").length);
		if(d.getProperty("parents").length == 0){
			d.setProperty("active","true");
		}
		else{
			d.setProperty("active","false");
		}
	}
	}*/
	//console.log(currFrame);
	var frame = currFrame;
	if(frame == animFrames.length-1){frame=0;}
	if(frame>0){
		for(var i = 0;i<animFrames[frame-1].length;i++){
			if(data.getFeatureById(animFrames[frame-1][i]).getProperty("children").length > 0){
				data.getFeatureById(animFrames[frame-1][i]).setProperty("active","false");
			}
		}
	}
	else{
		//console.log(size);
		for(var i = 1;i<=size;i++){
			data.getFeatureById(i).setProperty("active","false");	
		}
	}
	//console.log(d);
	for(var i = 0;i<animFrames[frame].length;i++){
		data.getFeatureById(animFrames[frame][i]).setProperty("active","true");
	}
	return(frame+1);
}
animArr = [[]];
var size = 0;
$.getJSON("http://localhost:8000/iowanetwork_anim.json",function(a){
	iowadata.network = new google.maps.Data;
	a.features.forEach(function(a) {
			size ++;
	    //console.log(a)
            a.geometry.coordinates = google.maps.geometry.encoding.decodePath(a.geometry.coordinates);
            a.geometry.coordinates = a.geometry.coordinates.map(function(a) {
                return [a.lat(), a.lng()]});
			//console.log(a.properties);
			var animFrames = a.properties.animFrames;
			var s = a.properties.startFrame;
			var e = a.properties.endFrame;
			//console.log(s);
			//console.log(e);
			for(var i = animArr.length-1;i<e;i++){
				animArr.push([]);
			}
			for(var i = 0;i<animFrames.length;i++){
				animArr[animFrames[i]].push(a.id);
			}
    })
    
	iowadata.network.addGeoJson(a);
	iowadata.network.setMap(map);
	//console.log(animArr);
	iowadata.network.setStyle(function(feature){
	if(feature.getProperty("active") == "true"){color = "#02fffa";}
	else{
	color = "#00F";
	}
	//console.log("id: "+feature.getId());
        return({
		strokeColor: color,    
		strokeOpacity: 1,
        	strokeWeight: 1,
        	clickable: !1
        });});
	iowadata.network.setMap(map);
	iowadata.network.idPropertyName =
            "true";
	//console.log(a.features.length);
	var frame = 0;
	frame = animationCycle(iowadata.network,animArr,frame,size);
	console.log(setInterval(function(){frame = animationCycle(iowadata.network,animArr,frame,size);},1000));
})