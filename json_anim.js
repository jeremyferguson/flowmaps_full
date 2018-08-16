var start = new Date().getTime()
var AnimId;

function animationCycle(data,animFrames,currFrame,size){
	var prevFrame;
	var frame = currFrame;
	var length = animFrames.length;
	if(frame == 0){prevFrame = [];}
	else{prevFrame = animFrames[frame-1];}
	if(frame == length -1){frame=0;}
	var currFrame = animFrames[frame];
	for(var i = 0;i<prevFrame.length;i++){
		if(currFrame.indexOf(prevFrame[i]) == -1 ){
			if(data.getFeatureById(prevFrame[i]).getProperty("children").length >0){
				data.getFeatureById(prevFrame[i]).setProperty("active","false");
			}
		}
	}
	for(var i = 0;i<currFrame.length;i++){
		//console.log(currFrame[i]);
		if(prevFrame.indexOf(currFrame[i]) == -1){data.getFeatureById(currFrame[i]).setProperty("active","true");}	
	}
	return(frame+1);
}
function load_json(_callback){
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
	});
	//console.log('tast');
	waitTime = 500;
	if(false || !!document.documentMode){waitTime = 3000;}
	google.maps.event.trigger(map,'resize');
	setTimeout(_callback,waitTime);
}
function run_animation(){
	//console.log('test');	
	animArr = [[]];
	google.maps.event.trigger(map,'resize');
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
	AnimId = setInterval(function(){frame = animationCycle(iowadata.network,animArr,frame,size);},150);
	google.maps.event.addListener(map, "zoom_changed", function() {
	clearInterval(AnimId);
	setTimeout(function(){
		AnimId = (setInterval(function(){
			frame = animationCycle(iowadata.network,animArr,frame,size);
		},150));
	},500);
	});
}
function main_screen(){
	iowadata.network.setMap(null);
	load_json(run_animation);

	//waitTime = 5000;
	//if(false || !!document.documentMode){waitTime = 20000;}
	/**setTimeout(function(){
		
	},waitTime);*/
	
}
main_screen();