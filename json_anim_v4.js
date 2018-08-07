var start = new Date().getTime()
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
function getAnimArr(){
	console.log("there");
	var request = new XMLHttpRequest();
	request.open('GET','http://localhost:8000/iowanetwork_animarr.txt',false);
	request.send(null);
	request.onreadystatechange = function(){
		if(request.readyState === 4 && request.status === 200){
			var type = request.getResponseHeader('Content-Type');
			if(type.indexOf("text") !== 1){
				var size = 0;
				var AnimArr = request.responseText.split("\n");
				for(var i = 0;i<AnimArr.length;i++){
					AnimArr[i] = AnimArr[i].split(" ").map(i => parseInt(i));	
					lineMax = Math.max(AnimArr[i]);
					if(lineMax > size){size = lineMax;}
				}	
				size --;
				return([AnimArr,size]);
			}
		}
	}
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
	var size = 0;
	console.log('here');
	var arr = getAnimArr();
	setTimeout(function(){
		console.log('hhhh');
		var AnimArr = arr[0];
		size = arr[1];
		console.log(size);
		var frame = 0;
		frame = animationCycle(iowadata.network,animArr,frame,size);
		console.log(setInterval(function(){frame = animationCycle(iowadata.network,animArr,frame,size);},150));
	},100000);
}
main_screen();