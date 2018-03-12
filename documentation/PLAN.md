# Skitter Project Plan

## Signup/Authentication: Java, MySQL/MariaDB
### Requirements:
1. SAML/Shibboleth integration
2. Account information stored in database
### Tests:
1. Adding and removing users
2. Test authentication
3. Security checks:
  - Session fixation
  - Password bruteforce
  - Username enumeration
### APIs:
1. `/isAuthenticated`
2. `/signIn`
3. `/newUser`
4. `/deleteUser`

## Homepage: HTML/CSS
### Requirements:
1. Homepage - landing page for skitter, prompts users to log in or create a new
   account, talks about how amazing skitter is and why you should get one
  - Integrated log-in page
  - Link to create account page
2. Create account - page/form for creating a new account on skitter
3. Dashboard - "homepage"/landing page for authenticated users
  - Will contain add/view/remove skit functionality (**nodejs**)
  - Will contain add/remove reply functionality (**ruby**)
4. Settings - Allows user to view and change their current settings
  - Will contain settings functionality (**php**)
5. User profile - Displays skits from specific user and shows information about
   them
  - Will contain add/remove reply functionality (**ruby**)
  - Will contain add/remove skit functionality *if the profile is the user's
    own profile* (**nodejs**)
  - Will contain link to settings page *if the profile is the user's own
    profile*
  - Will contain follow/unfollow functionality *if the profile is another
    user's profile*
6. Logout - landing page to confirm logout after users log out
7. Create flask app for handling page requests?
  - Would make it easier to put together pages
  - Can pass requests for all UI pages to the flask app to render the page
8. AngularJS used for dynamic content updates
### Tests:
1. Selenium to test functionality is consistent across browsers
2. Ensure there are no errors in Chrome developer view
3. Security checks:
  - XSS
4. HTML Validation
5. CSS Validation
6. Javascript Validation

## Settings: PHP
###Requirements:
1. View current settings
2. Change the following settings:
  - Username
  - User profile picture
  - Delete account
  - Private/public account
  - Email
3. MySQL DB backend to store user accounts - users created through J2EE
   signup/auth portal
4. CSRF nonce generation
5. Input sanitization
6. Picture re-processing
  - Use a known tool (GD/ImageMagick) to re-process and save the processed
    image
7. Sign out
### Tests:
1. RIPS (http://rips-scanner.sourceforge.net/) to test for PHP vulnerabilities
2. Test `/changeDisplayName`
3. Test `/changeProfileImage`
4. Test `/logout`
5. Security Checks:
  - CSRF
  - XSS
  - SQLi
  - File Upload restriction
  - Check for known vulns in image-processing libs
6. Test `/changeEmail`
7. Test `/changeAccountPrivacy`
8. Test user privacy
  - If private, the user should only be visible to their followers
### APIs:
1. `/changeDisplayName`
2. `/changeProfileImage`
3. `/logout`
4. `/changeEmail`
5. `/changeRealName`
6. `/changeAccountPrivacy`

## Add/View/Remove Skits (Tweets): NodeJS
### Requirements:
1. Add skits
  - Skits are no longer than 140 chars
  - Skits are not stored in the traditional database but will be stored and
    indexed using ElasticSearch
2. Remove skits
3. View skits
4. Kibana dashboard for ElasticSearch
### Tests:
1. Test `/addSkit`
  - 140-character limit
  - Confusables
2. Test `/removeSkit`
3. Test `/getSkits`
4. Security checks
  - ElasticSearch authentication management (XPack, HTTP Basic Auth)
  - Input sanitization
  - XSS
  - SQLi
### APIs:
1. `/addSkit`
2. `/removeSkit`
3. `/getSkits`

## Follow/Unfollow: Flask
### Requirements:
1. Allow users to search for other users
2. Visit other users’ pages and follow/unfollow them
  - Create user page with profile and past tweets
  - Usernames link to the user’s profile page
3. Skits of followed users are displayed on the homepage, with most recent first
  - Must dynamically update as new tweets are posted
4. Followers are stored in MySQL
  - Separate “follow” table that stores followed/follower relationships
5. Add central list of followed/following users to settings page
### Tests:
1. PEP8 Compliance
2. 10/10 PyLint rating
3. Test `/userSearch`
4. Test `/followUser`
5. Test `/unfollowUser`
6. Security Checks:
  - CSRF
7. Test `/getSkits`
8. Test central list of followed/following users
### APIs:
1. `/userSearch`
2. `/followUser`
3. `/unfollowUser`
4. `/getSkits`
  - Checks with the server if there are any new tweets from followed users

## Add/remove reply: Ruby on Rails
### Requirements:
1. Reply to Skits
  - Replies need to be presented with the original Skits
  - Replies are stored in ElasticSearch
  - Linking replies and original Skits inside ElasticSearch
  - http://www.rubydoc.info/gems/elasticsearch-api/Elasticsearch/API/Actions#update-instance_method
### Tests:
1. Test `/addSkitReply`
2. Test `/removeSkitReply`
3. Security checks
  - Timing attacks?
  - CSRF
### APIs:
1. `/addSkitReply`
2. `/removeSkitReply`
