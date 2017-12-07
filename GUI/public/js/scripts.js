var availableTags = [];
function getKeywords(){
	var keywordString = localStorage['objectToPass'];
	//localStorage.clear();
	var listOfKeywords = keywordString.split("; ")
	for (i=0;i<listOfKeywords.length;i++){
		availableTags.push(listOfKeywords[i]);
	}
	console.log(listOfKeywords);
}					    
// function to add new field for keyword selection	
$(function(){
	$(document).on('click', '.btn-addSelection', function(e) {		    	 
		e.preventDefault();
		var controlForm = $('.keywordGroup:first'),
		currentEntry = $(this).parents('.entry:first'),
		newEntry = $(currentEntry.clone()).appendTo(controlForm);
		//section to add autocomplete to the newly generated fields . 
		//only matches to tags with the same starting letter   

		$(".keywordGroup").find('input[type=text]:last').autocomplete({

			source: function( request, response ) {
				var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( request.term ), "i" );
				response( $.grep( availableTags, function( item ){
					return matcher.test( item );
					}) );
				}
		});

		newEntry.find('input').val('');
		controlForm.find('.entry:not(:last) .btn-addSelection')
			        .removeClass('btn-addSelection').addClass('btn-remove')
			        .removeClass('btn-success').addClass('btn-danger')
			        .html('<span class="glyphicon glyphicon-minus"></span>');
	}).on('click', '.btn-remove', function(e)
			{
				$(this).parents('.entry:first').remove();
				e.preventDefault();
				return false;
				});
});
//function to generate the keyword group div once the keywords have been submited
// only allows input that contains letters, full stops and dashes
//if no words have been added to a group and the user still tries to submit the group, an error message occurs	
function postKeywords(){
	var keyword = document.getElementsByName("kgroups")
	var div = document.createElement("div");
		div.style.width = "100%";					
		div.style.background = "white";
		div.style.color = "black";
		div.style.border = "1px solid #E6E6FA";
		div.style.borderRadius = "10px";
		div.style.padding = "1em";
		div.style.marginBottom = "1em";
	var letters = /^[A-Za-z.-\s]+$/;
	document.getElementById("check").value = "some groups";
	document.getElementById("errorArea").innerHTML = ""
	if (keyword[0].value.length>0){
		var searchString=''
		layout = '<div id="closeButton"><button type="button" class="close" aria-label="Close">\
 			<span aria-hidden="true">&times;</span></button></div><div class="btn-group" data-toggle="buttons">'
 		keywordLayout =""	
		for (let i=0; i<keyword.length; i++){
			if (keyword[i].value.length>0 ){
				if (keyword[i].value.match(letters)){
					keywordLayout+="<label class='btn btn-success active space'><input type='checkbox' \
					name='groups' checked value="+keyword[i].value+">"+ keyword[i].value+"</label>";
					if (/\s/.test(keyword[i].value)) {
						var keywordPlus = keyword[i].value.replace(/\s/g,"+");
						searchString += keywordPlus;
					}else{
						searchString +=keyword[i].value;
					}						
					if (i<keyword.length-1){
						searchString+=",";
					} 
				} else {
					keywordLayout = "<div class='alert alert-danger' role='alert'>Please, use only \
					alphabetical characters, '.' or '-'</div>";
					document.getElementById("check").value = "no groups";	
					break;
				}		
			}
		}
		console.log(searchString);
		layout = layout + keywordLayout + "<input type='hidden' name='group' value="+searchString+"></div>"
		div.innerHTML = layout;
		document.getElementById("errorMessageArea").innerHTML = "";
		document.getElementById("keywordGroupShow").appendChild(div);
	}else{
		alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Oh snap!</strong> \
		You must give at least one word.</div>"
		document.getElementById("errorMessageArea").innerHTML = alertMessageDiv;
		return false;
	}				
};
			// for the close button on each group bubble
$('#keywordGroupShow').on('click', '.close', function(events){
	$(this).parents('div').eq(1).remove();
	document.getElementById("check").value="no groups";
});
function countCheckboxes(checkboxValueList){
	var count = 0;
	var vals ="";
	for (var i=0, n=checkboxValueList.length;i<n;i++) {
		if (checkboxValueList[i].checked){ 
			count++; 	
			if (vals != ""){
				vals += ","+checkboxValueList[i].value;
			}else{
				vals += checkboxValueList[i].value;
			}		        
		}
	}
	var checkBoxstuff = [count, vals];		
	return checkBoxstuff;		 
}	
		//checks if every section of the homepage form has a value	
function validateForm()	{
	var formAction = document.getElementById('searchSpecs').action;

	var database = document.forms["searchSpecs"]["inputTypes"].value;
	if (database == "") {
		alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Oh snap!</strong> \
		You must select a search type</div>"
		document.getElementById("searchTypes").innerHTML = alertMessageDiv;
		return false;
	}else{
		if (formAction.match(/^.*connectToScript$/)){
			var discourse = document.forms["searchSpecs"]["searchnoteID"].value;
			if (discourse == ""){
				alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Oh snap!</strong> \
			    You must select a search definition.</div>"
			    document.getElementById("searchDefs").innerHTML = alertMessageDiv;
			    return false;
			}
		}else{
			console.log("test");
	console.log(formAction);
			var collections = document.getElementsByName('collectionRow');
			var checkBoxData = countCheckboxes(collections);
			var count = checkBoxData[0];
			var vals =checkBoxData[1];			
			if (count!=2){
				alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Oh snap!</strong> \
				You must select excatly two collections in order to proceed with the graph visualisation.</div>"
				document.getElementById("searchDefs").innerHTML = alertMessageDiv;
				return false;
			}else{
				document.getElementById('twoCollectionId').value = vals;
			}
		}
	}
};
//checking if there are any groups specified, if not, throw an error
function checkForGroups() {
	var groups = document.forms["keywordGroupForm"]["check"].value;
	console.log(groups);
	if (groups == "no groups"){
		alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Oh snap!</strong> \
		You forgot to actually add any keyword groups :( </div>"
		document.getElementById("errorArea").innerHTML = alertMessageDiv;
		return false;
	}else {
		document.getElementById("check").value="no groups";
		document.getElementById("errorArea").innerHTML = "";
		$(".se-pre-con").show();
        $("#mainContainer").hide(); 
	} 
};
//clear words from modal
$('#kGroupModal').on('hidden.bs.modal', function () {
	$(this)
		.find("input,textarea,select")
		.val('')
		.end()
});
$('#collectionsModal').on('hidden.bs.modal', function () {
	$(this)
		.find("input,textarea,select")
		.val('')
		.end()
	document.getElementById("collectionName").disabled = true;
	document.getElementById("collectionDescription").disabled = true;	
});
//loading gif for each page
$(window).load(function() {
	// Animate loader off screen
	$(".se-pre-con").fadeOut("slow");;
});

function setDb(dbName, notDbName){
	$(".panel-collapse").collapse("hide");
	document.getElementById("dbName").value = dbName;
	document.getElementById('notDbName').value = notDbName;
	console.log(document.getElementById("dbName").value);
	console.log(document.getElementById("notDbName").value);
	document.getElementById('searchTypes').innerHTML="";
	document.getElementById('locationSpot').innerHTML="";
	document.getElementById('map').style.visibility = 'hidden';
	document.getElementById('searchData').innerHTML="";
	localStorage.setItem( 'dbName', dbName );
};	

function changeFooter(){
	document.getElementById('footerId').style.position='relative';
};

//function to display information on click of each search button
function displaySearchData(searchName,earliest,latest,keywordString, total, coordinates, firstSearch, lastSearch, countOfSearches){
	//processing the coordinates from string python list to a json array	
	var coordinatesList = [];
	coordinateListS = coordinates.split('], [')
	for (i = 0; i<coordinateListS.length; i++){
		coorList = coordinateListS[i].split('), (');
		coordinatesList.push(coorList);
	}
	var properCoordinatersList= [];
	for (i = 0; i<coordinatesList.length; i++){	
		for (n=0; n<coordinatesList[i].length;n++){
			listOfCoorForSearch = coordinatesList[i][n].split(', ');
			var searchCoorsList = [];
			for (z=0;z<listOfCoorForSearch.length;z++){
				var coorstr = listOfCoorForSearch[z].replace(/[[\]()]/g,'');
				var coorint = parseFloat(coorstr);
				searchCoorsList.push(coorint);
			}
			properCoordinatersList.push(searchCoorsList);
		}
	}
	var pointList=[]
	for (n=0;n<properCoordinatersList.length;n++){
		var point= new Coordinates(properCoordinatersList[n]);
		pointList.push(point);
	}

	var jsonPointListStr=JSON.stringify(pointList);
	var jsonPointList = JSON.parse(jsonPointListStr);
	console.log(jsonPointListStr);
	//creating the map with the relevant coordinates
	initMap(jsonPointList);

	document.getElementById("start").value = earliest;
	document.getElementById("endof").value = latest;
	console.log(document.getElementById("endof").value);
		

	layout = "<div id='info'><h4>"+searchName+"</h4><div class='tabbable-panel'><div class='tabbable-line'>\
		<ul class='nav nav-tabs'><li class='active'><a href='#provenance' data-toggle='tab'>Provenance of the search </a></li>\
		<li><a href='#dataQualities' data-toggle='tab'>Dataset information</a></li></ul>\
		<div class='tab-content'><div class='tab-pane active' id='provenance'><strong>Start date of the search: </strong>"+firstSearch+"</br>\
		<strong>End date of the search: </strong>"+lastSearch+"</br><strong>Number of searches conducted during this period: </strong>"+countOfSearches+"</br>\
		<strong>Keywords and phrases of the search:</strong><br> "+keywordString+"\</div>\
		<div class='tab-pane' id='dataQualities'><strong>Total of tweets in this search: </strong>"+total+"</br>\
		<strong>Oldest tweet available published on:</strong> "+earliest+"</br><strong>Most recent tweet available published on:</strong> \
		"+latest+"</br></div></div></div>"

	document.getElementById("searchData").innerHTML=layout;	
};	
function setLocalStorage(keywordsList){
	var keyword = keywordsList;
    localStorage.setItem( 'objectToPass', keyword );
};
	//function to create a json array for each point
function Coordinates(coordinatesData){
	this.rad=coordinatesData[0];
	this.center={};
	this.center["lat"]=coordinatesData[1];
	this.center["lng"]=coordinatesData[2];
};

function initMap(jsonPointList) {
 	if (jsonPointList.length>0){
 		document.getElementById('map').style.visibility = 'visible';
 		document.getElementById('locationSpot').style.visibility = 'visible';	
 		console.log("map created");
 		}
 		
    // Create the map.
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: {lat: 54.695002, lng: -2.658691},
        mapTypeId: 'terrain'
    });
    // Construct the circle for each value in the point list.
    // Note: the radius is measured in meters so we need to multply it by 1000
    for (var city in jsonPointList) {
    // Add the circle for this city to the map.
         var cityCircle = new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: jsonPointList[city].center,
            radius: 1000*jsonPointList[city].rad
          });
    }
};
//function to initialize the date picker with start and end date of the selected search
$(function(){	
 	$('.input-daterange input').datetimepicker({
 		autoclose:true,
 		format:'YYYY-MM-DD HH:mm',
 		minDate: new Date(document.getElementById("fromDate").value),
	    maxDate: new Date(document.getElementById("toDate").value),
 	})

 });
$('#datetimepicker').datetimepicker({
    onSelect: function(dateText, inst) {
    	var fromDate = document.getElementById("fromDate").value; 
    	var toDate = document.getElementById("toDate").value;
    	localStorage.setItem( 'fromDate', fromDate );  
    	localStorage.setItem('toDate', toDate);

    	console.log(localStorage['fromDate']);
    	console.log(localStorage['toDate']);   
    }
});

$("input[name='kgroups']").autocomplete({
  	source: function( request, response ) {
        var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( request.term ), "i" );
        response( $.grep( availableTags, function( item ){
            return matcher.test( item );
        }) );
    }
});
function changeValues(){
	var collectionSelection = document.getElementById("listOfCollections");
	var collectionStr = collectionSelection.options[collectionSelection.selectedIndex].value;
	console.log(collectionStr);
	document.getElementById("collectionName").disabled = false;
	document.getElementById("collectionDescription").disabled = false;
	if (collectionStr != ""){
		var listOfCollections = collectionStr.split('|');
		var collectionName = listOfCollections[1];
		var collectionDescription = listOfCollections[0];
		var collectionUniqueId = listOfCollections[2];

		document.getElementById('collectionName').value = collectionName;
		document.getElementById('collectionDescription').value = collectionDescription;
		document.getElementById('collectionId').value = collectionUniqueId;
		console.log(document.getElementById('collectionId').value);
	}else{
		var uniqueIdentifier = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
		document.getElementById('collectionName').value = "";
		document.getElementById('collectionDescription').value = "";
		document.getElementById('collectionId').value = uniqueIdentifier;

		console.log(uniqueIdentifier);
	}
	var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth()+1; //January is 0!
		var yyyy = today.getFullYear();
		var hh = today.getHours();
		var ii = today.getMinutes();

		today = yyyy + '-' + mm + '-' + dd + ' ' + hh + ':' + ii;

	document.getElementById('dateOfCreation').value = today;
	console.log(document.getElementById('dateOfCreation').value);

	keywordGroup = document.getElementById('groupOriginalName').value;
	console.log(keywordGroup);
	document.getElementById('groupOfKeywords').value = keywordGroup;
	console.log(document.getElementById('groupOfKeywords').value);	
	document.getElementById('dbName').value= localStorage['dbName'];

};


$(document).ready(function(){
$("#mytable #checkall").click(function () {
        if ($("#mytable #checkall").is(':checked')) {
            $("#mytable input[type=checkbox]").each(function () {
                $(this).prop("checked", true);
            });

        } else {
            $("#mytable input[type=checkbox]").each(function () {
                $(this).prop("checked", false);
            });
        }
    });
    
    $("[data-toggle=tooltip]").tooltip();
});
//getting the database name from the local storage
function getDBName(){
	document.getElementById('dbName').value= localStorage['dbName'];
	console.log(document.getElementById('dbName').value);
};
//function to set the values for the edit modal for each collection
function setCollectionDateForEdit(name, description, collectionId, collectionDbId, keywords){
	var keywordGroups = keywords.split(";");
	var checkboxInputs = ""
	for (var i = 0; i < keywordGroups.length; i++) {
		checkboxInputs += "<div class='checkbox checkbox-success checkbox-inline'><input type='checkbox' name='keywordGroups' id='"+keywordGroups[i]+"' \
		value = '"+keywordGroups[i]+"'/><label for='"+keywordGroups[i]+"'>"+keywordGroups[i]+"</label></div>"
	}
	var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth()+1; //January is 0!
		var yyyy = today.getFullYear();
		var hh = today.getHours();
		var ii = today.getMinutes();

		today = yyyy + '-' + mm + '-' + dd + ' ' + hh + ':' + ii;
	
	document.getElementById('nameOfProject').value = name;
	document.getElementById('descriptionOfProject').value = description;
	document.getElementById('collectionId').value = collectionId;
	document.getElementById('timeStamp').value = today;
	document.getElementById('checkBoxArea').innerHTML = checkboxInputs;

	console.log(document.getElementById('nameOfProject').value);
	console.log(document.getElementById('descriptionOfProject').value);
	console.log(document.getElementById('collectionId').value);
	console.log(document.getElementById('timeStamp').value);
	
};
//function to get the unique id of the collection to be deleted
function setCollectionId(collectionId){
	document.getElementById('collectionToDeleteId').value = collectionId;
};
function setCollectionIdForTopics(){
	var collectionSelection = document.getElementById("listOfCollectionsForTopics");
	var collectionStr = collectionSelection.options[collectionSelection.selectedIndex].value;
	document.getElementById('collectionIdToShow').value = collectionStr;
};
//Function to check if two selections have been made; if so
//disable other selections and get the unique id values of
//the two selections for visualisation
$('input.checkthis').on('change', function(evt) {
   if($("input[name='collectionRow']:checked").length==2) {
	   $(':checkbox:not(:checked)').prop('disabled', true);
	   var checkboxes = document.getElementsByName('collectionRow');
	   var checkBoxData = countCheckboxes(checkboxes);
	   var count = checkBoxData[0];
	   var vals =checkBoxData[1];

		document.getElementById('twoCollectionId').value = vals;
		console.log(document.getElementById('twoCollectionId').value);
		document.getElementById('visButton').disabled=false;
	}else{
   	 	$(':checkbox:not(:checked)').prop('disabled', false);
   	 	document.getElementById('visButton').disabled=true;
   }
});

function changeKeywords(keywordGroup){
	document.getElementById('groupOriginalName').value = keywordGroup;
	console.log(document.getElementById('groupOriginalName').value);
	console.log(keywordGroup);
};
//what data to be shown based on the databse selected, needs to be refined for the case of more dbs
function selectDataToBeShown(database,notDatabase){
	var x = document.forms["searchSpecs"]["inputTypes"].value;
	var listOfNotDbs = notDatabase.split(";");
//if the database has been selected, do the following	
	if (x != ""){
		//if the database div has the relevant content, loop through the other divs
		if (document.getElementById(database)){
			for (var i = 0; i < listOfNotDbs.length; i++) {
				//if any of the not selected divs have content, hide them
				if(document.getElementById(listOfNotDbs[i])){
					document.getElementById(listOfNotDbs[i]).style.display = 'none';
					document.getElementById(database).style.display = 'block';
					document.getElementById('collectionError').innerHTML ="";
				}else if(!document.getElementById(listOfNotDbs[i])){
					document.getElementById(database).style.display = 'block';
					document.getElementById('collectionError').innerHTML = ""
				}
			}
		//if it doesn't but any of the other divs do, display error message and hide the other divs	
		}else if(!document.getElementById(database)){
			for (var i = 0; i < listOfNotDbs.length; i++) {
				if(document.getElementById(listOfNotDbs[i])){
					errorMessage = "<div class='alert alert-danger' role='alert'><strong>Whops!</strong> \
			    	There are no collections for this data source yet.</div>"
			    	console.log("triple suck");
				document.getElementById('collectionError').innerHTML = errorMessage;
				var divs = document.getElementsByClassName('setVisibility');
				for (var i = 0; i < divs.length; i++) {
				    divs[i].style.display = "none";
					} 
				}	
			}	
		}
	}else{
		alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Oh snap!</strong> \
		    	You must first select a data source</div>"
		document.getElementById("searchTypes").innerHTML = alertMessageDiv;
		return false;
	}
};
//changes the form action in the index page depending on the functionality selected
function changeFormAction(formAction){
	if (formAction == 'filterKeywords'){
		document.getElementById('searchSpecs').action="/connectToScript";
	}else{
		document.getElementById('searchSpecs').action="/visualiseCollectionsFromIndexPage";
	}
	console.log(document.getElementById('searchSpecs').action);
};
//for the filter keywords functionality
function selectFilterKeywordDataToBeShown(){
	var database = document.getElementById('dbName').value;
	var notDatabase = document.getElementById('notDbName').value;
	selectDataToBeShown(database,notDatabase);
};
//for the collection functionality
function selectCollectionDataToBeShown(){
	var database = document.getElementById('dbName').value + '_collection';
	var listNotDbs = document.getElementById('notDbName').value.split(";");
	var notDatabase = "";
	for (var i = 0; i < listNotDbs.length; i++) {
		notDbNameId = listNotDbs[i]+'_collection';
		if (notDatabase == ""){
			notDatabase=notDbNameId;
		}else{
			notDatabase+= ";"+notDbNameId;
		}
	}
		console.log(notDatabase);
		document.getElementById('locationSpot').innerHTML="";
		document.getElementById('map').style.visibility = 'hidden';
		document.getElementById('searchData').innerHTML="";

	selectDataToBeShown(database,notDatabase);
}
$('.panel-title a').collapse();

$(document).ready(function() {
    $('.dropdown-menu li a').click(function(event) {
        var option = $(event.target).text();
        $(event.target).parents('.btn-group').find('.dropdown-toggle').html(option+' <span class="caret"></span>');
    });
});