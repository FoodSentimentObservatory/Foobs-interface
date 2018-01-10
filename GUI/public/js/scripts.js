var availableTags = [];
var listOfTweets = [];
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
	var div = createAContainerForKeywords();
		
	var letters = /^[A-Za-z.-\s]+$/;
	document.getElementById("check").value = "some groups";
	document.getElementById("errorArea").innerHTML = ""
	if (keyword[0].value.length>0){
		layout = '<div id="closeButton"><button type="button" class="close" aria-label="Close">\
 			<span aria-hidden="true">&times;</span></button></div><div class="btn-group" data-toggle="buttons" style="width: 100%;">'
		var listOfKeywordGroupEntities = createLabelsForKeywords(keyword, letters)
		console.log(listOfKeywordGroupEntities[0]);
		layout = layout + listOfKeywordGroupEntities[1] + "<input type='hidden' name='group' value="+listOfKeywordGroupEntities[0]+"></div>"
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
//creates the div that will contain the keyword groups from KeywordSearch page
//and clusterSpecForm
function createAContainerForKeywords(){
	var div = document.createElement("div");
		div.style.width = "100%";					
		div.style.background = "white";
		div.style.color = "black";
		div.style.border = "1px solid #E6E6FA";
		div.style.borderRadius = "10px";
		div.style.padding = "1em";
		div.style.marginBottom = "1em";
		div.style.minHeight= '100px';
		div.style.paddingBottom= '3em';

	return div;	
}
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

	if (formAction.match(/^.*connectToScript$/)){
			var discourse = document.forms["searchSpecs"]["searchnoteID"].value;
			if (discourse == ""){
				alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Oh snap!</strong> \
			    You must select a search definition.</div>"
			    document.getElementById("searchDefs").innerHTML = alertMessageDiv;
			    return false;
			}
	}else if(formAction.match(/^.*clusterFromDataSet$/)){
			console.log('something')
			return true;
	}else if(formAction.match(/^.*collectionClusterParams$/)){
			var collection = document.forms["searchSpecs"]["collectionId"].value;
			if (collection==""){
				alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Oh snap!</strong> \
			    You forgot to select a collection.</div>"
			    document.getElementById("clusterCollectionError").innerHTML = alertMessageDiv;
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
				$('input[name="collectionRow"]').prop('disabled', true);
				document.getElementById('twoCollectionId').value = vals;
				loadingScreen()
				
			}
		}
	
};
function loadingScreen(){
	$(".se-pre-con").show();
    $("#whitie").hide();	
}
//checking if there are any groups specified, if not, throw an error
function checkForGroups() {
	var groups = document.forms["keywordGroupForm"]["check"].value;
	console.log(groups);
	if (groups == "display error"){
		alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Oh snap!</strong> \
		You forgot to add any keyword groups :( </div>"
		//document.getElementById("errorArea").innerHTML = alertMessageDiv;
		return false;
	}else {
		document.getElementById("check").value="no groups";
		//document.getElementById("errorArea").innerHTML = "";
		$(".se-pre-con").show();
    	$("#mainContainer").hide(); 
    	return true;
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
	$(".se-pre-con").fadeOut("slow");
});
$(window).bind("pageshow", function() {
  $("#whitie").show();
  $(".se-pre-con").fadeOut("slow");
});
	

function setDb(dbName, notDbName){
	$(".collapse").collapse("hide");
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
		

	layout = "<div class='info'><h4>"+searchName+"</h4><div class='tabbable-panel'><div class='tabbable-line'>\
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
function setKeywordsCluster(keywords){
	document.getElementById('keywordsCluster').value = keywords;
	console.log(document.getElementById('keywordsCluster').value);
	//function to create a json array for each point
}
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
	document.getElementById('tweetsCount').value = localStorage['countOfTweets'];

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
		checkboxInputs += "<div class='checkbox checkbox-success checkbox-inline'><input type='hidden' name='keywordGroups' value = '0'><input type='checkbox' name='keywordGroups' id='"+keywordGroups[i]+"' \
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
	var x = document.forms["dbSelect"]["inputTypes"].value;
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
//disbles the input fields that are not needed for the selected functionality
//closes the other accordions
function changeFormAction(formAction){
	if (formAction == 'filterKeywords'){
		document.getElementById('searchSpecs').action="/connectToScript";
			$('input[name="keywords"]').prop('disabled', false);
			$('input[name="endof"]').prop('disabled', false);
			$('input[name="start"]').prop('disabled', false);
			$('input[name="twoCollectionId"]').prop('disabled', true);
			$('input[name="collectionRow"]').prop('disabled', true);
			$('input[name="collectionId"]').prop('disabled', true);
			$('input[name="keywordsCluster"]').prop('disabled', true);
			$('input[name="searchnoteIDForCluster"]').prop('disabled', true);
			$('input[name="searchnoteID"]').prop('disabled', false);
			$('input[name="task"]').prop('disabled', false);
		document.getElementById('task').value='/keywordSearch';
		$("#selectCollection").collapse("hide");
		$("#clusteringOptions").collapse("hide");	
	}else if(formAction== 'selectCollection'){
		document.getElementById('searchSpecs').action="/visualiseCollections";
			$('input[name="keywords"]').prop('disabled', true);
			$('input[name="endof"]').prop('disabled', true);
			$('input[name="start"]').prop('disabled', true);
			$('input[name="twoCollectionId"]').prop('disabled', false);
			$('input[name="keywordsCluster"]').prop('disabled', true);
			$('input[name="task"]').prop('disabled', true);
			$('input[name="searchnoteIDForCluster"]').prop('disabled', true);
			$('input[name="searchnoteID"]').prop('disabled', true);
			$('input[name="collectionRow"]').prop('disabled', false);
			$("#filterKeywords").collapse("hide");
			$("#clusteringOptions").collapse("hide");
			$('input[name="collectionId"]').prop('disabled', true);		
	}else {
		$('input[name="keywords"]').prop('disabled', true);
		$('input[name="twoCollectionId"]').prop('disabled', true);
		$('input[name="searchnoteID"]').prop('disabled', true);
		$('input[name="collectionRow"]').prop('disabled', true);
		if(formAction == 'clusterACollection'){
			document.getElementById('searchSpecs').action="/collectionClusterParams";	
				$('input[name="endof"]').prop('disabled', true);
				$('input[name="start"]').prop('disabled', true);
				$('input[name="keywordsCluster"]').prop('disabled', true);
				$('input[name="task"]').prop('disabled', true);
				$('input[name="searchnoteIDForCluster"]').prop('disabled', true);
				$("#selectedDataSource").collapse("hide");	
				$('input[name="collectionId"]').prop('disabled', false);
		}else{
			document.getElementById('searchSpecs').action="/clusterFromDataSet";
				$('input[name="endof"]').prop('disabled', false);
				$('input[name="start"]').prop('disabled', false);
				$('input[name="keywordsCluster"]').prop('disabled', false);
				$('input[name="searchnoteIDForCluster"]').prop('disabled', false);
				$('input[name="task"]').prop('disabled', false);	
				$("#listCollections").collapse("hide");	
				$('input[name="collectionId"]').prop('disabled', true);
			document.getElementById('task').value='/specifyClusterParams';	
		}
	}
	console.log(document.getElementById('searchSpecs').action);
};
function closeAccordions(){
		$("#selectCollection").collapse("hide");
		$("#filterKeywords").collapse("hide");
}
//for the filter keywords functionality
function specifyTaskDataToBeShown(task){
	if (task=='clusterDataset'){
		var extention='_key';
	}else if (task=='filter'){
		var extention="";
	}else if(task =='scat'){
		var extention = "_collection";
		document.getElementById('locationSpot').innerHTML="";
		document.getElementById('map').style.visibility = 'hidden';
		document.getElementById('searchData').innerHTML="";
	}else{
		var extention = "_collection_forCluster";
		document.getElementById('locationSpot').innerHTML="";
		document.getElementById('map').style.visibility = 'hidden';
		document.getElementById('searchData').innerHTML="";
	}
	var database = document.getElementById('dbName').value+extention;
	var listNotDbs = document.getElementById('notDbName').value.split(";");
	var notDatabase = "";
	for (var i = 0; i < listNotDbs.length; i++) {
		notDbNameId = listNotDbs[i]+extention;
		if (notDatabase == ""){
			notDatabase=notDbNameId;
		}else{
			notDatabase+= ";"+notDbNameId;
		}
	}

	selectDataToBeShown(database,notDatabase);


};
//for the collection functionality
function selectCollectionDataToBeShown(radioId){
	
	var listNotDbs = document.getElementById('notDbName').value.split(";");
	var notDatabase = "";
	if (radioId=="scat"){
		var extention = "_collection";
	}else{
		var extention = "_collection_forCluster";
	}
	var database = document.getElementById('dbName').value + extention;
	for (var i = 0; i < listNotDbs.length; i++) {
		notDbNameId = listNotDbs[i]+extention;
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

function setHiddenValues(keywordString, searchQuery, location, fromDate, toDate){
	document.getElementById('keywordsToCluster').value = keywordString;
	

	console.log(document.getElementById('searchQuery').value);
};

function createDonuts(clustersString){
	if (clustersString.includes(";")==true){
		var mainClustersList = clustersString.split(';')
	}else{
		var mainClustersList = [clustersString];
	}

	
	for (i=0; i<mainClustersList.length; i++){
		var total = 0;
		var clustersList = mainClustersList[i].split(',');
		var listOfClusters = [];
		
		for (j=0; j<clustersList.length; j++){
			var cluster = clustersList[j].split('|');
			total += parseInt(cluster[2]);
			console.log(cluster);
			listOfClusters.push(cluster)
		}
		document.getElementById('nameOfGroup').innerHTML = "<h4>"+listOfClusters[0][1]+"</h4>";
		donutGen(listOfClusters, total);
	}
};

function donutGen(listOfClusters, total){
	var clustersJson = [];
	var colors_array = [];
	var allTweetsStr = document.getElementById('tweetsList').value;
	console.log(allTweetsStr);
	var listOfStrTweets = allTweetsStr.split(';');
	listOfTweets = [];
	for (var i = 0; i < listOfStrTweets.length; i++) {
		var tweetDataList = listOfStrTweets[i].split('|');
		listOfTweets.push(tweetDataList);
	}
	console.log(listOfTweets);
	for(i=0;i<listOfClusters.length; i++){
		var cluster = new Cluster(listOfClusters[i]);
		var color = getRandomColor();
		colors_array.push(color);
		clustersJson.push(cluster);
	}
	var jsonPointListStr=JSON.stringify(clustersJson);
	var jsonPointList = JSON.parse(jsonPointListStr);

	var keywordsChart = Morris.Donut({
	  element: 'pies',
	  data: jsonPointList,
	  colors: colors_array 
  }).on('click', function(i, row){
    var layout="";
    for (var i = 0; i < listOfTweets.length; i++) {
    	console.log(listOfTweets);
    	console.log(row.label);
    	if (row.label == listOfTweets[i][2]){
    		layout += "<div class='col-xs-8' id='tweet'><div class='col-xs-6' id='author'>\
                <span style='color:#FFF;'>"+listOfTweets[i][6]+"</span> <span style='color:#D3D3D3;'>@"+listOfTweets[i][1]+"</span></div>\
            <div class='col-xs-3' id='time'>"+listOfTweets[i][4]+"</div>\
            <div class='col-xs-3'><a href='"+listOfTweets[i][7]+"' target='_blank'>Show tweet on Twitter</a></div>\
            <div class='col-xs-12' id='tweetText'>"+listOfTweets[i][0]+"<br></div></div>";	
    	}
    }
    document.getElementById('tweets').innerHTML="";
    document.getElementById('tweets').innerHTML=layout;
    });
      keywordsChart.options.data.forEach(function(label, i){
      var textValue = label['label']+": "+label['value'];	
      var legendItem = $('<span></span>').text(textValue).prepend('<i>&nbsp;</i>');
      legendItem.find('i').css('backgroundColor', keywordsChart.options.colors[i]);
    $('#legend').append(legendItem)
  })
};

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
function Cluster(cluster){
	this.label = cluster[0];
	this.value = cluster[2];
};

$('#radioBtn a').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    $('#'+tog).prop('value', sel);
    
    $('a[data-toggle="'+tog+'"]').not('[data-title="'+sel+'"]').removeClass('active').addClass('notActive');
    $('a[data-toggle="'+tog+'"][data-title="'+sel+'"]').removeClass('notActive').addClass('active');
    if(document.getElementById('checkIfKeywords').value=="Y"){
    	showAddKeywordButton('eitherOrContent','Add a keyword group');
    	document.getElementById("check").value="display error";
    }else if (document.getElementById('checkIfKeywords').value=="N"){
    	hiddenInputs = "<input type='hidden' name='groups' value='no groups'/><input type='hidden' name='group' value='no groups'/>"
    	document.getElementById('eitherOrContent').innerHTML=hiddenInputs;
    }

});

function showKeywordGroups(keywordGroup, task){
	if (task =='dataset'){
		if (keywordGroup=='no groups'){
			$('input[id="clusterFromKGroups"]').prop('disabled', true);
			$('input[id="segmentFromKGroups"]').prop('disabled', true);
		}else{
			layout="<p>"+keywordGroup+"</p>";
			document.getElementById('showkeywordGroup').innerHTML=layout;
		}
	}else{
		$('input[id="clusterFromSearch"]').prop('disabled', true);
		$('input[id="segmentFromSearch"]').prop('disabled', true);

		layout="<p>"+keywordGroup+"</p>";
		document.getElementById('showkeywordGroup').innerHTML=layout;
	}
	
};
function showAddKeywordButton(divId, buttonTitle,keywordInputName){
	layout = "<div class='col-sm-10' id='keywordGroupShow'><div id='errorArea'></div></div><div id='keywordGroupModalDiv' class='keywordGroupModal col-xs-8'>\
    <button type='button' class='btn btn-success btn-lg' data-toggle='modal' data-target='#kGroupModal'>"+buttonTitle+"</button></div>"

    document.getElementById(divId).innerHTML=layout;
    document.getElementById('keywordInputName').value=keywordInputName;
};
function createLabelsForKeywords(keyword, letters){
	var searchString='';
	var keywordLayout ="";
	for (let i=0; i<keyword.length; i++){
		if (keyword[i].value.length>0 ){
			if (keyword[i].value.match(letters)){
				keywordLayout+="<div class='label label-success col-sm-5 addSpace'>"+ keyword[i].value+"</div>";
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
	var keywordEntitiesArray = [searchString, keywordLayout];
	return keywordEntitiesArray;	
};
function saveAndDisplayKeywords(){
	var div = createAContainerForKeywords();
	var keyword = document.getElementsByName("kgroups")
	var keywordInputName = document.getElementById('keywordInputName').value;	
	var letters = /^[A-Za-z.-\s]+$/;
	document.getElementById("check").value = "some groups";
	document.getElementById("errorArea").innerHTML = "";
	if (keyword[0].value.length>0){
		layout = '<div id="buttonForClose"><button type="button" class="close" aria-label="Close">\
 			<span aria-hidden="true">&times;</span></button></div><div class="btn-group" data-toggle="buttons" style="width: 100%;">';
 		var keywordEntitiesArray = createLabelsForKeywords(keyword, letters);
		console.log(keywordEntitiesArray[0]);
		layout = layout + keywordEntitiesArray[1] + "<input type='hidden' name='"+keywordInputName+"' id='"+keywordInputName+"' value="+keywordEntitiesArray[0]+">\
		</div><div class='enrichCheckBox col-sm-12' id='enrichCheckBox'><input type='checkbox' name='keywordEnrichments' id='keywordEnrichments' value='enrich'>\
		Enrich keywords </div>";
		
		div.innerHTML = layout;
		
		document.getElementById("errorMessageArea").innerHTML = "";
		document.getElementById("keywordGroupShow").appendChild(div);

		document.getElementById('keywordGroupModalDiv').style.display='none';
		console.log(document.getElementById(keywordInputName).value);
		if (keywordInputName=='groupCluster'){

			setKeywordsToCluster(document.getElementById(keywordInputName).value);
		}else{
			setKeywordsForSegment(document.getElementById(keywordInputName).value);
		}
		
	}else{
		alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Oh snap!</strong> \
		You must give at least one word.</div>"
		document.getElementById("errorMessageArea").innerHTML = alertMessageDiv;
		return false;
	}	
};
function setKeywordsToCluster(keywords){
	if (keywords.indexOf(" OR ")!= -1){
		newStr = keywords.replace(/,/g,"+");
		newKeywordStr = newStr.replace(/ OR /g, ",");
	}else{
		newKeywordStr = keywords;
	}
	console.log(keywords);
	document.getElementById('keywordsToCluster').value = newKeywordStr;
	console.log(document.getElementById('keywordsToCluster').value);
	document.getElementById("errorClusterArea").innerHTML = "";
};
function setKeywordsForSegment(keywords){
	if (keywords.indexOf(",") != -1){
		newKeywordStr = keywords.replace(/,/g, ";");
	}else{
		newKeywordStr = keywords
	}
	document.getElementById('keywordsForSegments').value = newKeywordStr;
	console.log(document.getElementById('keywordsForSegments').value);
	document.getElementById("errorSegmentArea").innerHTML = "";

};

function toggleKeywordContent(divId){
	var x = document.getElementById(divId);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
};
function hideOtherContent(selectedContent){
	if(selectedContent=="searchWords"){
		document.getElementById('showkeywordGroup').style.display = 'none';
		document.getElementById('addOwnWordsClusters').innerHTML="";
	}else if(selectedContent=="keywordGroups"){
		document.getElementById('searchKeywords').style.display = 'none'
		document.getElementById('addOwnWordsClusters').innerHTML="";		
	}else{
		document.getElementById('searchKeywords').style.display = 'none';
		document.getElementById('showkeywordGroup').style.display = 'none';

	}
}; 
function validateClusterForm(){
	var enrichedCheckbox = document.getElementsByName('keywordEnrichments');
	if (document.forms["clusterForm"]["keywordsToCluster"].value==""){
		alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Whops</strong> \
		You forgot to specify keywords for clusters.</div>";
		document.getElementById("errorClusterArea").innerHTML = alertMessageDiv;
		return false;
	}else if (document.forms["clusterForm"]["keywordsForSegments"].value==""){
		alertMessageDiv= "<div class='alert alert-danger' role='alert'><strong>Whops</strong> \
		You forgot to specify keywords for cluster segments.</div>";
		document.getElementById("errorSegmentArea").innerHTML = alertMessageDiv;
		return false;
	}else if (enrichedCheckbox.length>0){
			console.log(enrichedCheckbox);	
			if (enrichedCheckbox[0].checked){
				document.getElementById('enrichKeywords').value='enrich';
			}else{
				document.getElementById('enrichKeywords').value='do not';
			}
			$(".se-pre-con").show();
        $("#mainContainer").hide();
	}else{
		$(".se-pre-con").show();
        $("#mainContainer").hide();
		return true;
	}		
};
function checkForNoResultKeywords(check){
	if (check=='0'){
		message = "<div class='alert alert-info'>All selected keywords returned some results.</div>";
		document.getElementById('keywordInfo').innerHTML=message;
	}
};
function checkForResults(numberOfTweets,groupName){
	if (numberOfTweets=='0'){
		$("#error").html("No results were found for <strong>'"+groupName+"'</strong>.");
      $('#noResultsAlert').modal("show");
	}
}
function readText(that){
	var reader = new FileReader();
	if(that.files && that.files[0]){
				var reader = new FileReader();
				reader.onload = function (e) {  
					var output=e.target.result;
					document.getElementById('keywordsToCluster').value = output;
					console.log(output);
				};
				reader.readAsText(that.files[0]);
			}
	var linkList = that.value.split("\\");		
	document.getElementById("uploadFile").value = linkList[2];		
};
function setLocalStorageForCount(countOfTweets){
	localStorage.setItem( 'countOfTweets', countOfTweets );
}

