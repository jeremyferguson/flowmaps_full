var start = new Date().getTime()
var AnimId;
function animationCycle(data,animFrames,currFrame,size){
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
		for(var i = 1;i<=size;i++){
			data.getFeatureById(i).setProperty("active","false");	
		}
	}
	for(var i = 0;i<animFrames[frame].length;i++){
		data.getFeatureById(animFrames[frame][i]).setProperty("active","true");
	}
	return(frame+1);
}
function main_screen(){
	iowadata.network.setMap(null);
	animArr = [[]];
	$.getJSON("http://localhost:8000/iowanetwork_anim.json",function(a){
		iowadata.network = new google.maps.Data;
		a.features.forEach(function(a) {
            a.geometry.coordinates = google.maps.geometry.encoding.decodePath(a.geometry.coordinates);
            a.geometry.coordinates = a.geometry.coordinates.map(function(a) {
                return [a.lat(), a.lng()]
			});
    	})
		iowadata.network.addGeoJson(a);
		iowadata.network.setMap(map);
		iowadata.network.setStyle(function(feature){
			weight = feature.getProperty("weight");
			if(feature.getProperty("active") == "true"){color = "#02fffa";}
			else{color = "#00F";}
        	return({
				strokeColor: color,    
				strokeOpacity: 1,
        		strokeWeight: weight,
        		clickable: !1
        	});
		});
		iowadata.network.setMap(map);
		iowadata.network.idPropertyName = "true";
	})
	google.maps.event.trigger(map,'resize');
	setTimeout(function(){
		var size = 0;
		for(key in iowadata.network.b.b){
			size ++;
			currSeg = iowadata.network.b.b[key];
			var s = currSeg.getProperty("startFrame");
			var e = currSeg.getProperty("endFrame");
			var animFrames = currSeg.getProperty("animFrames");
			for(var j = animArr.length-1;j<e;j++){
				animArr.push([]);	
			}
			for(var j = 0;j<animFrames.length;j++){
				animArr[animFrames[j]].push(currSeg.j);	
			}
		}
		var frame = 0;
		frame = animationCycle(iowadata.network,animArr,frame,size);
		AnimId = (setInterval(function(){frame = animationCycle(iowadata.network,animArr,frame,size);},150));
		google.maps.event.addListener(map, "zoom_changed", function() {
			clearInterval(AnimId);
			setTimeout(function(){
				AnimId = (setInterval(function(){
					frame = animationCycle(iowadata.network,animArr,frame,size);
				},150));
			},500);
		});
	},5000);
		
}
main_screen();