/***********************
 * HEADER
 ***********************/

/***************************
 * POLL CREATOR FUNCTIONS
 ***************************/
 function saveCreatorTitle(poll_id){
	 var newtitle = document.getElementById('poll-editor').value;
	 $.post('/create-poll/edit-title/', { pid:poll_id, new_title:newtitle },
			  function(data){		 	
		 		$('.poll-title-poll').show();
		 		$('#poll-editable-title').text(data);
		 		$('.poll-title-edit').hide();
	 		}
	  );
	return false;
 }

function setAllowUserAnswer(pid, choice){
	$('#set-allow-user-answer-indicator').show();
	$.get("/create-poll/allow-user-answer/" + pid + "/" + choice + "/",
			function(data){
				$('#set-allow-user-answer-indicator').hide();
			});	
}

function creatorActive(pid, choice){
	$('#poll-activity-indicator').show();
	$('#poll-activity').load("/create-poll/poll-active/" + pid + "/" + choice + "/",
			function(data){
				$('#poll-activity-indicator').hide();
			});
	return false;
}

function imgControlPanel(pid, pfid, pollfile){
	$("#poll-create-img-control-panel").replaceWith(
			"<div id=\"poll-create-img-control-panel\" style=\"display:none;\">" +
				"<img src=\"" + pollfile + "\">" +
				"<span class=\"poll-create-cp-links\"><a href=\"#\" onclick=\"return setMainFile('" + pid + "', '" +  pfid + "');\">Set as the main file</a> | " +
				"<a href=\"#\" onclick=\"return deleteFile('" + pid + "', '" +  pfid + "');\">Delete this file</a></span>" +
				"<span id=\"poll-create-cp-feedback\" style=\"display:none;\"></span>" +
			"</div>");
	$("#poll-create-img-control-panel").slideDown();

}

function setMainFile(pid, pfid){
	$("#poll-create-img-control-panel").load('/create-poll/set-main-file/' + pid + '/' + pfid + '/');
	$("#poll-create-file-wrapper").load('/create-poll/reload-files/' + pid + '/');
	return false;
}

function deleteFile(pid, pfid){
	$("#poll-create-img-control-panel").load('/create-poll/delete-file/' + pid + '/' + pfid + '/');
	$("#poll-create-file-wrapper").load('/create-poll/reload-files/' + pid + '/');
	return false;
}

function showVideo(pid){
	$('#poll-create-video-box').load('/create-poll/show-video/' + pid + '/');
	return false;
}

function addAnswer(id){
	var answer;
	$(".blue_sm_i_answer").show();
	answer = document.getElementById('id_answer').value;
	$("#poll-answers").load("/create-poll/add-answer/?a=" + encodeURIComponent(answer) + "&id=" + id,
		function (data){
			$(".blue_sm_i_answer").hide();
			$("#poll-answers").slideDown();
		}
	)
	document.getElementById('id_answer').value = "";
	return false;
}

function addTag(id){
	var tag;
	tag = document.getElementById('id_tag').value;
	$(".blue_sm_i_tag").show();
	$("#poll-tags").load("/create-poll/add-tag/?t=" + encodeURIComponent(tag) + "&id=" + id,
		function (data){
			$(".blue_sm_i_tag").hide();
			$("#poll-tags").slideDown();
	});
	document.getElementById('id_tag').value = "";
	return false;
}


function deletePollTag(tid, pid){
	$(".blue_sm_i_tag").show();
	$("#poll-tags").load("/create-poll/delete-poll-tag/?&tid=" + tid + "&pid=" + pid,
		function (data){
			$(".blue_sm_i_tag").hide();
			$("#poll-tags").slideDown();
	});
	return false;
}

function deleteAnswer(id){
	$(".blue_sm_i_answer").show();
	$("#poll-answers").load("/create-poll/delete-answer/?&id=" + id,
		function (data){
			$(".blue_sm_i_answer").hide();
			$("#poll-answers").slideDown();
	});
	return false;
}

function showCreateLink() {
	$("#poll-create-url").fadeIn();
	return false;
}

function showCreateFiles(){
	$("#poll-create-file").fadeIn();
	return false;
}

function countChars(){
	var cnt = 400 - document.getElementById('id_description').value.length;
	$("#poll-create-desc-char-count").text("(" + cnt + " chars left)");
	return false;
}

function titleEditKeyHandler(e, pid){
    var key;
     if(window.event){
          key = window.event.keyCode;     //IE
     }
     else{
          key = e.which;     //firefox
     }
    if (key == 13)
    {
        return saveCreatorTitle(pid);
    }
}

function addTagKeyHandler(e, pid){
    var key;
     if(window.event){
          key = window.event.keyCode;     //IE
     }
     else{
          key = e.which;     //firefox
     }
    if (key == 13)
    {
        return addTag(pid);
    }
}

function addAnswerKeyHandler(e, pid){
    var key;
     if(window.event){
          key = window.event.keyCode;     //IE
     }
     else{
          key = e.which;     //firefox
     }
    if (key == 13)
    {
        return addAnswer(pid);
    }
}

/*************************
 * SEARCH FUNCTIONS
 ***********************/
function changeSearch(){
	 type = document.getElementById('id_type').value;
	 terms = document.getElementById('id_searchbox').value;

	 if (terms == ""){
		 terms = null;
	 }
	 
	 if (type == '0'){
		 if(terms){
			 window.location = "/search/" + terms + "/";
		 } else{		 
			 window.location = "/search/";
		 }
	 } else{
		 if(terms){
			 window.location = "/tag/" + terms + "/";
		 } else {
			 window.location = "/tag/";
		 }
	 }
 }
 
function searchTags(e){
	var tag;
	tag = document.getElementById("id_tag").value;
	$("#poll_create_tags_suggestions").load("/create-poll/search-tags/?tag=" + encodeURIComponent(tag));
}

 function headerSearchHandler(e){
	//the purpose of this function is to allow the enter key to
	//point to the correct button to click.
    var key;
     if(window.event)
          key = window.event.keyCode;     //IE
     else
          key = e.which;     //firefox
    if (key == 13)
    {
        window.location = "/search/" + encodeURIComponent(document.getElementById("searchBox").value) + "/";
    }
}

function searchHandler(e){
	// the purpose of this function is to allow the enter key to
	// point to the correct button to click.
    var key;
     if(window.event)
          key = window.event.keyCode;     //IE
     else
          key = e.which;     //firefox
    if (key == 13)
    {
        return doSearch();
    }
}

function focusHeaderSearchBox(type){
	var searchBox;
	if (type == 'reset'){
		searchBox = document.getElementById("searchBox");
		searchBox.value = "Search...";
		return false;
	}
	
	searchBox = document.getElementById("searchBox");
	searchBox.value = "";
	return false;
}


function doSearch(terms){
	var search_terms;
	if (terms){
		search_terms = terms;
		document.getElementById("id_searchbox").value = terms;
	} else{
		search_terms = document.getElementById("id_searchbox").value;
	}
	
	type = document.getElementById('id_type').value;
	if (type == '0'){
		window.location = "/search/" + encodeURIComponent(search_terms) + "/";
	} else {
		window.location = "/tag/" + encodeURIComponent(search_terms) + "/";
	}
	return false;
	
	
	/*$("#search-listings").hide();
	$(".blue_orange_i").show();
	$("#search-listings").load("/search/terms/"  + encodeURIComponent(search_terms) + "/",
			function (data){
				$(".blue_orange_i").hide();
				$("#search-listings").fadeIn();
			});
	window.location = "#" + encodeURIComponent(search_terms)
	return false;*/
}

/**********************
 * POLL VIEW FUNCTIONS 
 **********************/
 
function flagInappropriate(pid){
	 $("#flag-inappropriate").hide();
	 $("#flag-inappropriate").load("/view-poll/flag-inappropriate/?pid=" + pid, function(){
		 $("#flag-inappropriate").fadeIn();
	 });
		return false;
 }
 
function watchPoll(pid){
	$("#poll-view-watch-it").load("/view-poll/watch-poll/?type=a&pid=" + pid);
	return false;
}

 function stopWatchPoll(pid, divid){
	 if (divid){
		 $("#" + divid).load("/view-poll/watch-poll/?type=d&pid=" + pid);
	 } else{
		 $("#poll-view-watch-it").load("/view-poll/watch-poll/?type=d&pid=" + pid);	 
	 }
	 
	 return false;
}
 
function voteAnswer(){
	var voteIt = confirm("Are you sure?");
	if (voteIt) { 
	  
	  var poll_id = document.getElementById("poll_id").value;
	  var radio_id = 0;
	  for(var i = 0; i < document.forms.vote_answer_form.answers.length; i++){
	    if (document.forms.vote_answer_form.answers[i].checked == true){
	      answer_id = document.forms.vote_answer_form.answers[i].value;
	    }
	  }
	  
	  // sanity check
	  if (document.forms.vote_answer_form.spillover_answers){
		  for(var i = 0; i < document.forms.vote_answer_form.spillover_answers.length; i++){
		    if (document.forms.vote_answer_form.spillover_answers[i].checked == true){
		      answer_id = document.forms.vote_answer_form.spillover_answers[i].value;
		    }
		  }
	  }
	
	  $("#vote-on-answer").hide();
	  $('#answer-radio-indicator').show();
	  $.getJSON("/view-poll/answer_poll/?answer_id=" + encodeURIComponent(answer_id)
	    + "&poll_id=" + encodeURIComponent(poll_id),
	    function (data){
		  $("#vote-on-answer").html(data.pvr)
		  $("#vote-on-answer").fadeIn();

		  $("#poll-chart").html('<img src="' + data.chart + '"/>');
		  $("#poll-chart").fadeIn();
		  $('#answer-radio-indicator').hide();
	  	});
		  
	}
  return false;
}


function getAnswersForPoll(answer, pid){
	if (answer == '0'){		
		// handle the spillover answer id
		$("#spillover-results-link").slideUp();
		$("#spillover-results-span").load("/view-poll/get-spillover-answers/?&pid=" + pid);
		$("#spillover-results-span").fadeIn();
	} else {
		var id = "#voters-for-results-" + answer;
		if ($(id).css('display') != 'none'){
			$(id).hide();
		} else{
			var indicator_id = "#get-results-indicator-" + answer;
			$(indicator_id).show();
			$(id).load("/view-poll/get-voters/?aid=" + answer + "&pid=" + pid,
				function(data){
					$(id).fadeIn();
					$(indicator_id).hide();
				}
			);
		}
	}
	return false;
}

function postComment(url, type, comment_id, depth, user, indicator_id){
	var comment = document.getElementById("id_comment").value;
		
	$("#" + indicator_id).show();	
	jQuery.post(url, {'comment': comment}, 
		function(data) {
			  // increment comment count
			 $(".comments-count-title").load("/poll-comments/update-count/?pid=" + data[0].fields.object_id);
			 $(".comments-count-title").load("/poll-comments/update-comments/?pid=" + data[0].fields.object_id);
			 $.get("/email-on-comment/" + data[0].pk + "/");
			 $("#" + indicator_id).hide();
			 if (type == 'new-comment'){
				 $("#comment-form").hide();
				 var htmlStr = '<div class="comment" style="margin-left:' + depth + 'em;"><div>' +
				 	'<div class="comment-body"><p>' + data[0].fields.comment + '</p></div>' +
				 	'<p class="posted-by">Posted by <a href="/profile/' + user + '/">' + user + '</a></p>'+ 
				 '</div></div>'
				 $("#new-post-comment").html(htmlStr);
				 $("#new-post-comment").fadeIn("slow");			 
			 } else {
				 depth = depth + 1;
				 $("#new-cmnt-reply-" + comment_id).hide();
				 $("#new-thread-comment-" + comment_id).html(
						 	'<div class="comment"  style="margin-left:' + depth + 'em;">' +
			 					'<div> <div class="comment-body"><p>' + data[0].fields.comment + '</p></div>' +
			 					'<p class="posted-by">Posted by <a href="/profile/' +user + '/">' + user + '</a></p></div>' +
			 				'</div>');
				 $("#new-thread-comment-" + comment_id).fadeIn();
				 ("#c" + comment_id).hide();
		 }		 
	}, "json");

	return false;
}


function writeObj(obj, message) {
	  if (!message) { message = obj; }
	  var details = "*****************" + "\n" + message + "\n";
	  var fieldContents;
	  for (var field in obj) {
	    fieldContents = obj[field];
	    if (typeof(fieldContents) == "function") {
	      fieldContents = "(function)";
	    }
	    details += "  " + field + ": " + fieldContents + "\n";
	  }
	  console.log(details);
}



function deleteComment(id){
	var del;
	del = confirm("Are you sure you want to delete your comment?")
	if (del) {
		$("#del-comment-indicator-" + id).show();
		url = '/delete-comment/' + id + '/';
		$.post(url, 
			function(){
				$("#del-comment-indicator-" + id).hide();
				$('#comment-' + id).fadeOut();			
			});
		
	}
	return false;
}

function addDemographicFilter(){
	alert(addDemographicFilter.counter);
  if (typeof addDemographicFilter.counter == 'undefined'){
    addDemographicFilter.counter = 0;
  }
  $('#apply_filters').fadeOut("slow");

  $('#demographic_filter_' + addDemographicFilter.counter).load('/view-poll/demographic_form/', {counter:addDemographicFilter.counter}, 
		  function (form){
				  $('#demographic_filter_' + addDemographicFilter.counter).fadeIn();
	});
  return false;
}

function getDemographicValueForm(){
  var id = '#id_demographic_' + addDemographicFilter.counter ;
  var demographic = $(id)[0].value;
  $(id)[0].disabled = true;

  var demo_value = '#demographic_value_' + addDemographicFilter.counter
  $(demo_value)[0].disabled = true;
  $(demo_value).load('/view-poll/demographic_value_form/', {demographic:demographic, counter:addDemographicFilter.counter}, function (form){
				  $(demo_value).fadeIn();
	});
  return false;
}

function addedDemoValue(){
  var demo_value = '#id_demo_value_' + addDemographicFilter.counter;
  $(demo_value)[0].disabled = true;

  $('#apply_filters').css('visibility', 'visible').fadeIn("slow");

  addDemographicFilter.counter++;
  return false;
}

/**
 * The url to call this function should only appear when the form is all filled out
 * should send a list together as all /sex-male/age-greater_than-30/
 */
function applyFilters(url){
  var filter_count = addDemographicFilter.counter;

  for (var i=0; i < filter_count; i++){
    var demo_id = '#id_demographic_' + i ;
    var demo_value = '#id_demo_value_' + i;
    var demographic = encodeURIComponent($(demo_id)[0].value);

    if ($(demo_value)[0].type == 'text')
      var demographic_value = encodeURIComponent($(demo_value)[0].value);
    else
      var demographic_value = encodeURIComponent($(demo_value)[0].options[$(demo_value)[0].selectedIndex].text); // need to check for -

    demographic_value = demographic_value.replace(/-/g, '|||')

    url = url + demographic + '-' + demographic_value + '/';
  }
  window.location = url


  return false;
}

 /*******************
  * PROFILE
  ******************/
 
 function getMoreActivity(username){
	  var phase = document.getElementById('activity-phase-count').value;
	  $('#more-activity-indicator').show();
	  $.get('/profile/' + username + '/more-activity/?phase=' + phase, 
			function(data){		  		
		  		if (data == '0'){
		  			$('#activity-more-btn').text("Looks like there's nothing left!");
		  			$('#activity-more-btn').css({'cursor':'default', 'background-color':'#024997', 'color':'#fff'});
		  		}else{
		  			$('#activity-more').hide();
		  			$('#activity-more').replaceWith(data);
		  			$('#activity-more').show("slow");
		  		}		  	
		  		$('#more-activity-indicator').hide();
	  		}
	  );
	  document.getElementById('activity-phase-count').value = parseInt(phase) + 1;
	  return false;
	  
 }
  
 function friendUser(userId){
	  $("#user-friend").hide();
	  $("#user-friend").load("/friend/?id=" + userId);
	  $("#user-friend").fadeIn();
	  return false;
  }
  
 function mailUser(user, mail_id){
	 var subject_id = "id_subject";
	 var body_id = "id_body";
	 var send_form_id = "profile-message-form";
	 var sent_confirm_id = "profile-message-sent";
	 var indicator_id = "profile-message-send";
	 var clear_subject = true;
	 var old_body;
	 if (mail_id){
		 subject_id = subject_id + "_" + mail_id;
		 body_id = body_id + "_" + mail_id;
		 send_form_id = send_form_id + "-" + mail_id;
		 sent_confirm_id = sent_confirm_id + "-" + mail_id;
		 indicator_id = indicator_id + "-" + mail_id;
		 // doing a threaded reply
		 // dont clear the subject
		 clear_subject = false;
	 }
	 var subject = document.getElementById(subject_id);
	 var body = document.getElementById(body_id);
	 $('#' + indicator_id).show();
	 $("#" + sent_confirm_id).hide();
	 
	 $.post("/profile/" + user + "/mail/", { subject:subject.value, body:body.value, mid:mail_id }, 
		function (data){
 		 	// callback
		 	if (clear_subject){
		 		document.getElementById(subject_id).value = "";
		 	}
 		 	document.getElementById(body_id).value = "";
 		 	$("#" + send_form_id).fadeOut(function (){
 		 		$("#" + sent_confirm_id).html(data);
 		 		$('#' + indicator_id).hide();
 		 		$("#" + sent_confirm_id).fadeIn();
 		 	}); 		 	
	 	}
	 );	 
	 return false;
 }
 
 function markAllMail(){
	 var sure = confirm("Mark all mail as read?");
	 if (sure){
		 $.get("/mark-mail-as-read/");
		 $('#top-new-msgs').text("");
		 $('.msg').css("background-color","#dddddd");
		 $('.msg').css("border","1px solid #000");
	 }
	 return false;
 }
 
 function fadeMailBody(id, sent_mode){
	 if (!sent_mode){
		 $.get('/profile/mail/mail/view/?id=' + id);
	 }	 
	 var divid;
	 divid = "message-row-" + id;
	 if (document.getElementById(divid).style.display == "none"){
		 $('#' + divid).fadeIn();
		 $('#msg-' + id).css("background-color","#dddddd");
		 $('#msg-' + id).css("border","1px solid #000");
		 
	 } else {
		 $('#' + divid).fadeOut();
	 }
	 return false;
 }

 function updateUserChartType(chart_type){
	 $("#default-chart-setting-callback").hide();
	 $("#default-chart-setting-callback").load("/profile/settings/update-setting/?type=100&chart_type=" + chart_type, 
		function (data) {
		 $("#default-chart-setting-callback").fadeIn();
	 	}
	 );
 }
 
 function settingsLinkNewWindow(newVal){
	 $("#link-new-window-callback").hide();
	 $("#link-new-window-callback").load("/profile/settings/update-setting/?type=101&val=" + newVal, 
		function (data) {
		 $("#link-new-window-callback").fadeIn();
	 	}
	 );	 
 }
 
 function updateSetting(divId, type, newVal){
	 $("#" + divId + "-callback").hide();
	 $("#" + divId + "-indicator").show();
	 $("#" + divId + "-callback").load("/profile/settings/update-setting/?type=" + type + "&val=" + newVal, 
		function (data) {
		 $("#" + divId + "-callback").fadeIn();
		 $("#" + divId + "-indicator").hide();
	 	}
	 );	 
 }
  
 function settingsWhichPic(newVal){
	 $("#which-pic-callback").hide();
	 $("#which-pic-callback").load("/profile/settings/update-setting/?type=200&val=" + newVal, 
		function (data) {
		 $("#which-pic-callback").fadeIn();
	 	}
	 );	 
 }
 
/****************
* LOGIN
******************/

 function showLoginBlock(id, next){
		$("#" + id).hide();
		$("#" + id).load("/login-block/?next=" + encodeURIComponent(next),
				function(data){
					$("#" + id).slideDown("fast");
				}
			);

		return false;
	}

function forgotIt(type){
	$("#id_forgot_it").fadeIn();
	if (type == 'user'){
		$("#forgot_pw").hide();
		$("#forgot_user").fadeIn();
		
	} else {		
		$("#forgot_user").hide();
		$("#forgot_pw").fadeIn();		
	}
	return false;
}

function forgotUser(){
	var email = document.getElementById("id_forgot_it_input").value;
	$("#id_forgot_it").hide();
	$("#id_forgot_it").load("/forgot-username/?email=" + encodeURIComponent(email), 
		function (data){
			$("#id_forgot_it").fadeIn();
		});
	return false;
}

function forgotPassword(){
	var conf = confirm('This will reset your password and email it to you.  Ok?');
	if (conf){
		var email = document.getElementById("id_forgot_it_input").value;
		$("#id_forgot_it").hide();
		$("#id_forgot_it").load("/forgot-password/?email=" + encodeURIComponent(email), 
			function (data){
				$("#id_forgot_it").fadeIn();
			});
	}
	return false;
}

/****************
* REGISTER
******************/
function checkUsername(){
	var username = document.getElementById("id_username").value;
	$("#usermatch").load("/register/checkname?n=" + encodeURIComponent(username));
	return false;
}

function showRegHelp(thingie){
	$(".help-" + thingie).fadeIn();
}

function hideRegHelp(thingie){
	$(".help-" + thingie).fadeOut();
}


/****************
* MISC
******************/
function showShare(){
	hideflash();
	return addthis_open(this, '', '[URL]', '[TITLE]');
}

function hideShare(){
	
	showflash();
	return addthis_close();
}

function hideflash()
{
    /* hide all flash in the page */
    flash = document.getElementsByTagName('embed')
    for (var i = 0; i < flash.length; i++) 
    { 
            flash[i].style.visibility = 'hidden';
    }
}

function showflash()
{
    /* show all flash */
    flash = document.getElementsByTagName('embed')
    for (var i = 0; i < flash.length; i++) 
    { 
            flash[i].style.visibility = 'visible';
    }
}




/*****************************************************************************/

/*****************************************************************************/

/*****************************************************************************/


//prepare the form when the DOM is ready
$(document).ready(function() {
	// prepare auto completes
	$('#id_tag').autocomplete("/create-poll/search-tags/");
	$('#searchBox').autocomplete("/create-poll/search-tags/");

});

