/* A collection of helper functions for Skitter. */

// Get a cookie from the browser based on the cookie's name
function getCookie(name) {
    // Cookie names all end with an equals sign
    name = name + "=";

    // Cookies are delimited by semicolons
    let cookieArray = document.cookie.split(';');
    for(cookie in cookieArray) {
        // Check if the name occurs in the cookie
        let nameLocation = cookie.indexOf(name);

        // Name was found, return cookie value
        if(nameLocation != -1) {
            return cookie.substring(name.length + nameLocation, cookie.length - nameLocation);
        }
    }

    // Cookie was not found
    return "";
}

// Add a cookie to the browser
function addCookie(name, value) {
    console.log('Adding new cookie: ' + name + '=' + value);
    document.cookie += name + '=' + value;
}