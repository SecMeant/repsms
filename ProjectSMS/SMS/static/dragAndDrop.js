function allowDrop(ev) {
    ev.preventDefault();
}
function CpySUB() {
	alert(staffTaken.join());
	document.getElementById("AllSubjects").value = staffTaken.join();
	return true;
}
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
    tmp = "#" + ev.target.id;
    $(tmp).css("opacity", 0.4)
}
//ev is object that i try to put element
function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    if (ev.target.id == "Subjects")
   		ev.target.appendChild(document.getElementById(data));
   	else{
   		
   		SwapSubjects(data,ev.target.id);
   		SWAPArrayElements(document.getElementById(data).value,ev.target.value)

   	}

}
function SWAPArrayElements(v1, v2){
	idx1 = staffTaken.indexOf(v1, 0);
	idx2 = staffTaken.indexOf(v2, 0);
	staffTaken[idx1] = v2;
	staffTaken[idx2] = v1;

}
function SwapSubjects(from , to) {  //from == Data, to == ev.target
	id_from = "#" + from;
	id_to = "#" + to;
	var temp_from = $(id_from);
	var temp_to = $(id_to);

	var element_to_swap1 = document.createElement("INPUT");
	element_to_swap1.setAttribute("id","temp1");
	var element_to_swap2 = document.createElement("INPUT");
	element_to_swap2.setAttribute("id","temp2");

	document.getElementById(from).parentNode.insertBefore(element_to_swap1, document.getElementById(from));
	document.getElementById(to).parentNode.insertBefore(element_to_swap2, document.getElementById(to));
	$( "#temp1" ).replaceWith( temp_to );
	$( "#temp2" ).replaceWith( temp_from );
	$(id_from).css("opacity", 1);
}

	
	function not_In(v, tabV){
		check =true;
		for(var i = 0 in tabV){
			if(tabV[i] == v){
				return false;
			}
			
		}
		return true;
	}