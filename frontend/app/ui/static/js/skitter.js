/* A collection of helper functions for Skitter. */

// The location of the default profile picture
var defaultProfile = '/static/img/default-profile.png';

/**
 * Gets the value of a cookie from the browser.
 * @param {string} cname The name of the cookie to get from the browser.
 */
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

/**
 * Adds a cookie to the browser.  Courtesy of w3schools: https://www.w3schools.com/js/js_cookies.asp
 * @param {string} cname The name of the cookie to create
 * @param {string} cvalue The value of the cookie to create
 */
function setCookie(cname, cvalue) {
    document.cookie = cname + "=" + cvalue + ";path=/";
}