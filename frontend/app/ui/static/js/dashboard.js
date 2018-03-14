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


    // Show skit replies

    // Hide skit replies

    // Reply to skit
});

// Load latest skits
$.get('/getSkits', function() {
    console.log('Getting skits...');
    // TODO
});

// Show skit replies
$('.skits').on('click', 'show-replies', function() {
    $.get('/getSkitReplies', function() {
        console.log('Getting skit replies...');
    });
});

// Hide skit replies

// Reply to skit