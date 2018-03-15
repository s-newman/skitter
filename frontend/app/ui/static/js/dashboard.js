$(document).ready(function() {
    // Post a tweet when they click "Post!"
    $('#post-skit').submit(function() {
        // Create a JSON string to send
        let postData = {

        };

        // Attempt to post skit
        console.log('Attempting to post skit:', postData);
        let skitPost = $.post('/addSkit', postData);

        // Log error if post failed
        skitPost.fail(function() {

            console.log('Failed to post skit.')
        })

        // Log success if post worked
        skitPost.done(function() {
            // Load latest skits
        })
    });

    $('button').click(function(event) {
        // Show skit replies
        if($(event.target).hasClass('show-replies')) {
            console.log('Showing replies...');
            // Change button to hide replies
            $(event.target).removeClass('show-replies');
            $(event.target).addClass('hide-replies')
            event.target.innerHTML = 'Hide';

            // Retrieve replies from server
            let getReplies = $.get('/getSkitReplies', function(data) {
                console.log('Getting skit replies...');
                // Add replies to DOM
                /*
                *******************
                * TODO: Implement *
                *******************
                */
            });
        }

        // Hide skit replies
        else if($(event.target).hasClass('hide-replies')) {
            console.log('Hiding replies...');
            // Change button to show replies
            $(event.target).removeClass('hide-replies');
            $(event.target).addClass('show-replies');
            event.target.innerHTML = 'Replies';

            // Remove replies from DOM
        }
    });

    // Reply to skit
});

// Load latest skits
$.get('/getSkits', function() {
    console.log('Getting skits...');
    // TODO
});
