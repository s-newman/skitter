from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from os import getcwd

"""The hostname of the server being tested."""
HOST = 'http://localhost'


def wait_for_load(browser, page):
    wait = WebDriverWait(browser, 10)
    wait.until(lambda browser: browser.current_url != HOST + page)


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
    wait_for_load(browser, '/')

    # Check if the proper page loaded
    assert browser.current_url == HOST + '/new-account'

    return None


def new_account(browser):
    ##
    #   Click sign up without filling out forms.  The following error should
    #   appear
    #       Please pick a username!
    ##
    browser.get(HOST + '/new-account')
    submit = browser.find_element_by_css_selector('input[type=submit]')
    submit.click()
    assert 'Please pick a username!' in browser.page_source

    ##
    #   Click sign up after putting garbage in username field, should redirect
    #   to `/newUser`
    ##
    browser.find_element_by_id('username').send_keys('fakenews')
    submit.click()
    wait_for_load(browser, '/new-account')

    # Check if the proper page loaded
    assert browser.current_url == HOST + '/newUser'

    return None


def dashboard(browser):
    ##
    #   Clicking on "Username" should redirect to `/profile`
    ##
    browser.get(HOST + '/dashboard')
    browser.find_element_by_class_name('main-username').click()
    wait_for_load(browser, '/dashboard')
    assert browser.current_url == HOST + '/profile'

    ##
    #   Clicking on "broseph" should redirect to `/profile/theOfficialBroseph`
    ##
    browser.get(HOST + '/dashboard')
    browser.find_element_by_class_name('main-username').click()
    wait_for_load(browser, '/dashboard')
    assert browser.current_url == HOST + '/profile'

    ##
    #   Clicking on a show replies button should change the button to "hide
    #   replies"
    ##
    browser.get(HOST + '/dashboard')

    # Wait a little bit for the skits to load
    time.sleep(3.5)

    # Click on the replies
    button = browser.find_element_by_class_name('show-replies')
    button.click()
    assert 'Hide' in button.text

    ##
    #   Clicking on a hide replies button should change the button to "show
    #   replies"
    ##
    button.click()
    assert 'Replies' in button.text

    ##
    #   Clicking on a reply button should create the reply input box and the
    #   reply submission button
    ##
    button = browser.find_element_by_class_name('add-reply')
    button.click()

    # Find the replies section for the associated skit
    skit_id = button.get_attribute('id').split('-')[1]
    parent = button.find_elements_by_xpath('..')[0]
    responses = parent.find_element_by_id('{}-response'.format(skit_id))

    # Check if the skit reply has been found - note this operates like assert
    # in that it will throw an exception if it doesn't work
    responses.find_element_by_class_name('new-skit-reply')

    ##
    #   Clicking on a post reply button should hide the reply input box and the
    #   reply submission button
    ##
    responses.find_element_by_class_name('new-skit-reply-submit').click()
    assert responses.get_attribute('innerHTML') == ''

    return None


def internal_link(browser, text, link):
    browser.get(HOST + '/profile/123')
    browser.find_element_by_link_text(text).click()
    wait_for_load(browser, '/profile')
    assert browser.current_url == HOST + link


def profile(browser):
    ##
    #   Clicking on "Skitter" should redirect to `/dashboard`
    ##
    internal_link(browser, 'Skitter', '/dashboard')

    ##
    #   Clicking on "Settings" should redirect to `/settings`
    ##
    internal_link(browser, 'Settings', '/settings')

    ##
    #   Clicking on "Log Out" should redirect to `/logout`
    ##
    internal_link(browser, 'Log Out', '/logout')

    return None


def logout(browser):
    ##
    #   Clicking on "Come back soon!" should redirect to `/`
    ##
    browser.get(HOST + '/logout')
    browser.find_element_by_link_text('Come back soon!').click()
    wait_for_load(browser, '/logout')
    assert browser.current_url == HOST + '/'

    return None


def settings(browser):
    ##
    #   Uploading a file larger than 1MB and clicking change, "File is too
    #   large!" should appear
    #   ->  Then, upload a file smaller than 1MB and click change, "File is too
    #       large!" should disappear
    ##
    browser.get(HOST + '/settings')

    # Upload big file
    browser.find_element_by_id('picture-upload').send_keys(getcwd() +
                                                           '/testing/big')
    assert 'File is too large!' in browser.page_source

    # Upload small file
    browser.find_element_by_id('picture-upload').send_keys(getcwd() + 
                                                           '/small')
    assert 'File is too large!' not in browser.page_source

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
        browser.quit()


if __name__ == '__main__':
    main()
