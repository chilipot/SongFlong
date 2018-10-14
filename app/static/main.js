function updateSize() {
	var y = document.getElementsByTagName("video");
	var z = document.getElementsByClassName("title");
	//console.log(z);
	
	for (var i = 0; i < y.length; i++) {
		//console.log(y[i].offsetHeight);
		z[i].style.height = y[i].offsetHeight; 
	}
}

var elems = document.getElementsByClassName("video two-thirds column");

for (var i = 0; i < elems.length; i++) {
	new ResizeSensor(elems[i], updateSize);
}

updateSize();