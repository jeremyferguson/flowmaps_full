iowadata.network.setMap(null);
palette = ["#bfffe9","#50d2fa","#00a6d4","#0072e0","#ffdf00","#ffa000","#ff4502","#8b0000"];
function load_json(){
	$.getJSON("http://localhost:8000/rainfall_network_anim_normalized.geojson",function(a){
		a.features.forEach(function(a) {
			a.geometry.coordinates = google.maps.geometry.encoding.decodePath(a.geometry.coordinates);
			a.geometry.coordinates = a.geometry.coordinates.map(function(a) {
				return [a.lat(), a.lng()]
			});
			a['properties']['currFrame'] = 0;
			a['properties']['frames'] = a['properties']['frames'].split("|");
			size ++;
		});	
		iowadata.network = new google.maps.Data;
		iowadata.network.addGeoJson(a);
		iowadata.network.setMap(map);
		iowadata.network.setStyle(function(feature){
			colorNo = parseInt(feature.getProperty("frames")[feature.getProperty("currFrame")].slice(-1));
			color = palette[colorNo];
			return({	
				clickable: !1 ,
				strokeColor: color,    
				strokeOpacity: 1,
				strokeWeight: 2,
			});
		});
		google.maps.event.trigger(map,'resize');
		setTimeout(function(){makeAnim(size)},2000);
	})
}
var animArr =[];
var size = 0;
var frame = 0;
function makeAnim(size){
	for(var i = 0;i<241;i++){animArr.push([]);}
	for(var i = 1;i<=size;i++){
		feat = iowadata.network.getFeatureById(i);
		animArr[0].push(feat.getId());
		currFrames = feat.getProperty("frames");
		if(currFrames.length > 1){
			//console.log(currFrames);
			for(var j = 1;j<currFrames.length;j++){
				//console.log(currFrames[j]);
				cFrame = parseInt(currFrames[j].slice(0,-1));
				//console.log(cFrame);
				animArr[cFrame].push(feat.getId());
			}
		}
	}
	playAnim();
}
function playAnim(){
	frame = changeFrame(frame,1);
	setTimeout(function(){
		animId = setInterval(function(){
			frame = changeFrame(frame,1);},
		100);},
	1000);
}
function pauseAnim(){
	clearInterval(animId);
}
function nextFrame(){
	frame = changeFrame(frame,1);
}
function prevFrame(){
	frame = changeFrame(frame,-1);
}
function changeFrame(frame,direction){
	var currFrame = frame + direction;
	if(currFrame <0){currFrame = 240;}
	if(currFrame > 240){currFrame = 0;}
	for(var i = 0;i<animArr[currFrame].length;i++){
		//console.log(animArr[currFrame][i]);
		feat = iowadata.network.getFeatureById(animArr[currFrame][i]);
		if(currFrame == 0){feat.setProperty("currFrame",0);}
		else{feat.setProperty("currFrame",feat.getProperty("currFrame")+1);}
	}
	console.log(currFrame);
	return(currFrame);
}
load_json();

//console.log(size);