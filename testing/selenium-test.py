from selenium import webdriver

def index():
    # Enter trash credentials and hit log in, "Invalid credentials." should appear

    # Enter trash credentials and hit sign up, should redirect to `/new-account`
    return None

def new_account():
    # Upload file larger than 1MB, "File is too large!" should appear

    ### Click sign up, "File upload is too large." should appear

    # Click sign up without filling out forms, 
    ### "Please correct the following errors:
    ### Please fill out all form fields!
    ### Please upload a profile picture." should appear

    # Click sign up after uploading picture,
    ### "Please correct the following errors:
    ### Please fill out all form fields!" should appear

    # Click sign up after putting garbage in username field and uploading picture,
    ### "Please correct the following errors:
    ### Please fill out all form fields!" should appear

    # Click sign up after putting garbage in username field, and email in email fields and uploading picture, should redirect to `/newUser`
    return None

def dashboard():
    # Clicking on "Username" should redirect to `/profile`

    # Clicking on "broseph" should redirect to `/profile/theOfficialBroseph`

    # Clicking on a show replies button should change the button to "hide replies"

    # Clicking on a reply button should create the reply input box and the reply submission button
    return None

def profile():
    # Clicking on "Skitter" should redirect to `/dashboard`

    # Clicking on "Settings" should redirect to `/settings`

    # Clicking on "Log Out" should redirect to `/logout`
    return None

def logout():
    # Clicking on "Come back soon!" should redirect to `/`
    return None

def settings():
    # Uploading a file larger than 1MB and clicking change, "File is too large!" should appear
    
    ### Upload a file smaller than 1MB and click change, "File is too large!" should disappear
    return None

def main():
    index()
    new_account()
    dashboard()
    profile()
    logout()
    settings()

if __name__ == '__main__':
    main()