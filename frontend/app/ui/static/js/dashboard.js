// Interval to retrieve skits (note 1000 = # of milliseconds in a second)
let refreshTimer = 3 * 1000;

$(document).ready(function() {
    // Get the initial listing of skits

    getSkits();
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
    $('.skits').on('click', 'button', function(event) {
        // Show skit replies
        if($(event.target).hasClass('show-replies')) {
            console.log('Showing replies...');
            // Change button to hide replies
            $(event.target).removeClass('show-replies');
            $(event.target).addClass('hide-replies')
            event.target.innerHTML = 'Hide';
            let skitID = event.target.id.split('-')[1];

            // Retrieve replies from server
            let getReplies = $.get('/getSkitReplies?skitID=' + event.target.id, function(data) {
                console.log('Getting skit replies...');
                console.log(data);
                // Add replies to DOM
                //$(event.target).siblings('#' + skitID + '-replies').html(newSkitReply('dude', '/profile/dude', null, 'hey man this reply sucks'));
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
            let skitID = event.target.id.split('-')[1];
            $(event.target).siblings('#' + skitID + '-replies').empty();
        }
    });

    // Reply to skit button clicked
    $('.skits').on('click', '.add-reply', function(event) {
        // Display input box
        let skitID = event.target.id.split('-')[1];
        $(event.target).siblings('#' + skitID + '-response').html(
            '<form class="new-skit-reply">' +
            '<input class="new-skit-reply-input" placeholder="What\'s on your mind?" />' +
            '<input class="new-skit-reply-submit" type="submit" value="Post!" />' +
            '</form>');

            // Post reply
            $('.new-skit-reply').submit(function(innerEvent) {
                // Create a JSON string to send
                let postData = {
                    // TODO
                };

                // Attempt to post skit reply
                console.log('Attempting to post skit reply:', postData);
                let skitReplyPost = $.post('/addSkitReply', postData, function(data) {
                    console.log('Reply posted.');
                    console.log(data);
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

    // Load latest skits every minute
    let timer = setInterval(getSkits, refreshTimer);
});

// Temporary variable to prove that skits are being updated.  Remove once implemented fully.
var counter = 123;

// Getter for skits
function getSkits() {
    $.get('/getSkits', function(data) {
        console.log('Getting skits...');
        console.log(data);
        // TODO
        for (var i = 0; i < data['data'].length; i++) {
            let skitAuthor = data['data'][i]['skit']['username'];

            $('.skits').append(newSkit('broseph', '/profile/theOfficialBroseph', null, counter, '12222'));
        }
        // Add skits to the DOM
        // $('.skits').append(newSkit('broseph', '/profile/theOfficialBroseph', null, counter, '12222'));
        // counter++;  // Remove from prod.
    });
}


// Constructor for replies
function newSkitReply(username, profilePath, picturePath, content, skitReplyID) {
    // Set the profile picture to the default if one is not specified
    if(picturePath === null) {
        picturePath = defaultProfile;
    }

    return '<article id="' + skitReplyID + '" class="skit-reply">' +
        '<img src="' + picturePath + '" class="skit-profile-pic" height=64 width=64 />' +
        '<a class="username" href"' + profilePath + '">' + username + '</a>' +
        '<p>' + content + '</p>' +
        '</article>';
}

// Constructor for skits
function newSkit(username, profilePath, picturePath, content, skitID) {
    // Set the profile picture to the default if one is not specified
    if(picturePath === null) {
        picturePath = defaultProfile;
    }

    // Ain't that ugly as hell?
    return '<article id="' + skitID + '" class="skit">' +
        '<img src="' + picturePath + '" alt="Skit Profile Picture" class="skit-profile-pic" height=64 width=64 />' +
        '<a class="username" href="' + profilePath + '">' + username + '</a>' +
        '<p>' + content + '</p>' +
        '<button id="toggle-' + skitID + '" type="button" class="show-replies">Replies</button>' +
        '<button id="reply-' + skitID + '" type="button" class="add-reply">Respond</button><br />' +
        '<section id="' + skitID + '-response"></section>' +
        '<section id="' + skitID + '-replies"></section>' +
        '</article>';
}

// Function to get a specific section from the clicked button
function getSection(event, type) {
    return document.getElementById(event.target.id.split('-')[1] + '-' + type);
}