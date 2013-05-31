$(document).ready(function() {
    debug = true;
    
    $('div.comment-form form').submit(function() {
            
        $('div.comment-error').remove();
    
	    name = $('#id_name').val();
		email = $('#id_email').val();
		url = $('#id_url').val();
		comment = $('#id_comment').val();
		content_type = $('#id_content_type').val();
		object_pk = $('#id_object_pk').val();
		timestamp = $('#id_timestamp').val();
		security_hash = $('#id_security_hash').val();
		honeypot = $('#id_honeypot').val();
	    
	    $.post('/ajax/comment/post/', {
			    name: name,
			    email: email,
			    url: url,
			    comment: comment,
			    content_type: content_type,
			    object_pk: object_pk,
			    timestamp: timestamp,
			    security_hash: security_hash,
			    honeypot: honeypot,
			}, 
			function(data) {
			
			    if (data.status == "success") {
				    // If the post was a success, disable the Post button to
				    // prevent accidental duplication.
				    $('input.submit-post').attr('disabled', 'disabled');
				
				    // If this is the first comment, I add the "## comment(s) so far"
				    // banner that I use to introduce the comments section.
				    if ($('div#comments').children().length == 0) {
				        $('div#comments').prepend(
				            '<h2 class="comment-hd">1 comment so far:</h2>'
				        )
				    }
				
				    // Here I build the HTML to use for the comment.  I set the
				    // style to "display:none" so that I can fade it in with an
				    // animation.
				    comment_html = '<li class="comment" style="display: none;">' +
				        '<div class="comment-body"><p>' + comment +
				        '</p></div><div class="clear"></div>' +
				        '<p class="posted-by">Posted by <a href="' + url +
				        '">' + name + '</a> 0 minutes ago.</p></li>'
				
				    // Then I add the comment at the bottom of the comments section
				    // and fade it in.
				    $('ul#comments').append(comment_html);
				    $('li.comment:last').show('slow');
				
				    // I hide the comment form to prevent duplication, and
				    // replace it with a success message for the user.
				    $('.comment-form').hide()
				        .html('<p class="comment-thanks">Comment successfully' +
				              ' posted. Thank you!</p>')
				        .show(1000);
				        
				} else if (data.status == "debug") {
				    if (debug) {
				        // If the site is currently in development, list the debug
				        // errors.
				        $('div.comment-form').before('<div class="comment-error">' +
				            data.error + '</div>');
				    } else {
				        // Otherwise, display a generic server error message.
				        $('div.comment-form').before('<div class="comment-error">' +
				            'There has been an internal error with the server. ' +
				            'Please contact a site administrator.</div>');
				    }
				} else {
				    // If there were errors with the form, I add them to the
				    // page above my comment form with a "comment-error" div.
				    $('div.comment-form').before('<div class="comment-error">' +
				        data.error + '</div>');
				}
		    }
		, "json");


        return false;
    });
});
