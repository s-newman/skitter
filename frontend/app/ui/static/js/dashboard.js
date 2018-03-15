$(document).ready(function() {
    // Post a skit when they click "Post!"
    $('#post-skit').submit(function(event) {
        // Create a JSON string to send
        let postData = {
            // TODO
        };

        // Attempt to post skit
        console.log('Attempting to post skit:', postData);
        let skitPost = $.post('/addSkit', postData, function() {
            console.log('Skit posted.');

            // Load latest skits
        });

        // Log error if post failed
        skitPost.fail(function() {

            console.log('Failed to post skit.')
        });

        event.preventDefault();
    });
    
    // Show or hide skit replies
    $('button').click(function(event) {
        // Show skit replies
        if($(event.target).hasClass('show-replies')) {
            console.log('Showing replies...');
            // Change button to hide replies
            $(event.target).removeClass('show-replies');
            $(event.target).addClass('hide-replies')
            event.target.innerHTML = 'Hide';

            // Retrieve replies from server
            //let getReplies = $.get('/getSkitReplies', function(data) {
                console.log('Getting skit replies...');

                // Add replies to DOM
                getSection(event, 'replies').innerHTML = newSkitReply('dude', '/profile/dude', null, 'hey man this reply sucks');
                /*
                *******************
                * TODO: Implement *
                *******************
                */
            //});
        }

        // Hide skit replies
        else if($(event.target).hasClass('hide-replies')) {
            console.log('Hiding replies...');
            // Change button to show replies
            $(event.target).removeClass('hide-replies');
            $(event.target).addClass('show-replies');
            event.target.innerHTML = 'Replies';

            // Remove replies from DOM
            getSection(event, 'replies').innerHTML = '';
        }
    });

    // Reply to skit button clicked
    $('.add-reply').click(function(event) {
        // Display input box
        getSection(event, 'response').innerHTML = '<form class="new-skit-reply">' +
            '<input class="new-skit-reply-input" placeholder="What\'s on your mind?" />' +
            '<input class="new-skit-reply-submit" type="submit" value="Post!" />' +
            '</form>';

            // Post reply
            $('.new-skit-reply').submit(function(innerEvent) {
                // Create a JSON string to send
                let postData = {
                    // TODO
                };
        
                // Attempt to post skit reply
                console.log('Attempting to post skit reply:', postData);
                let skitReplyPost = $.post('/addSkitReply', postData, function() {
                    console.log('Reply posted.');
                });
        
                // Log error if post failed
                skitReplyPost.fail(function() {
        
                    console.log('Failed to reply to skit.')
                });
        
                // Remove skit reply form
                innerEvent.target.parentNode.innerHTML = '';
        
                innerEvent.preventDefault();
            });
    });

});

// Load latest skits
$.get('/getSkits', function() {
    console.log('Getting skits...');
    // TODO
});

// Constructor for replies
function newSkitReply(username, profilePath, picturePath, content) {
    // Set the profile picture to the default if one is not specified
    if(picturePath === null) {
        picturePath = defaultProfile;
    }

    return '<article class="skit-reply">' +
        '<img src="' + picturePath + '" class="skit-profile-pic" height=64 width=64 />' +
        '<a class="username" href"' + profilePath + '">' + username + '</a>' +
        '<p>' + content + '</p>' +
        '</article>';
}

// Function to get a specific section from the clicked button
function getSection(event, type) {
    return document.getElementById(event.target.id.split('-')[1] + '-' + type);
}