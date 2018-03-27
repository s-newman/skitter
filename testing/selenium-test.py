from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

"""The hostname of the server being tested."""
HOST = 'http://localhost'


def index(browser):
    ##
    #   Enter trash credentials and hit log in, "Invalid credentials."
    #   should appear
    ##
    browser.get(HOST + '/')
    browser.find_element_by_id('username').send_keys('fakenews')
    browser.find_element_by_id('password').send_keys('factswha')
    browser.find_element_by_id('log-in').click()
    assert 'Invalid credentials.' in browser.page_source

    ##
    #   Enter trash credentials and hit sign up, should redirect to
    #   `/new-account`
    ##
    browser.find_element_by_id('sign-up').click()

    # Give it a little bit for the next page to load
    wait_for_load = WebDriverWait(browser, 10)
    wait.until(lambda browser: browser.current_url != HOST + '/')

    # Check if the proper page loaded
    assert browser.current_url == HOST + '/new-account'

    return None


def new_account(browser):
    ##
    #   Upload file larger than 1MB, "File is too large!" should appear.
    #   ->  Then, click sign up, "File upload is too large." should appear
    ##

    ##
    #   Click sign up without filling out forms.  The following error should
    #   appear:
    #       Please correct the following errors:
    #       Please fill out all form fields!
    #       Please upload a profile picture.
    ##

    ##
    #   Click sign up after uploading picture.  The following error should
    #   appear:
    #       Please correct the following errors:
    #       Please fill out all form fields!
    ##

    ##
    #   Click sign up after putting garbage in username field and uploading
    #   picture.  The following error should appear:
    #       Please correct the following errors:
    #       Please fill out all form fields!
    ##

    ##
    #   Click sign up after putting garbage in username field, and email in
    #   email fields and uploading picture, should redirect to `/newUser`
    ##
    return None


def dashboard(browser):
    ##
    #   Clicking on "Username" should redirect to `/profile`
    ##

    ##
    #   Clicking on "broseph" should redirect to `/profile/theOfficialBroseph`
    ##

    ##
    #   Clicking on a show replies button should change the button to "hide
    #   replies"
    ##

    ##
    #   Clicking on a reply button should create the reply input box and the
    #   reply submission button
    ##
    return None


def profile(browser):
    ##
    #   Clicking on "Skitter" should redirect to `/dashboard`
    ##

    ##
    #   Clicking on "Settings" should redirect to `/settings`
    ##

    ##
    #   Clicking on "Log Out" should redirect to `/logout`
    ##
    return None


def logout(browser):
    ##
    #   Clicking on "Come back soon!" should redirect to `/`
    ##
    return None


def settings(browser):
    ##
    #   Uploading a file larger than 1MB and clicking change, "File is too
    #   large!" should appear
    #   ->  Then, upload a file smaller than 1MB and click change, "File is too
    #       large!" should disappear
    ##
    return None


def main():
    # Add all browsers that will be tested
    browsers = [webdriver.Firefox(), webdriver.Chrome()]

    # Test all pages with each browser
    for browser in browsers:
        index(browser)
        new_account(browser)
        dashboard(browser)
        profile(browser)
        logout(browser)
        settings(browser)


if __name__ == '__main__':
    main()
