import getpass
import subprocess

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

POLYQUARTZ_URL = "https://ssl.vpn.polymtl.ca/+CSCOE+/logon.html?reason=12&gmsg=4646594365627376797244686E65676D#form_title_text"


def login_with_credentials(driver):
    """
    Use Selenium to acquire a valid VPN cookie and return it to the user
    :param driver: The web driver to use for "spoofing" a log-in
    :return: The VPN cookie obtained through the spoof
    """
    # Connect to the PolyQuartz URL directly
    print("Connecting to PolyQuartz URL...")
    driver.get(POLYQUARTZ_URL)

    # Wait until the website loads before proceeding
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "group_list"))
    )
    print("Connected!")

    # "Click" the button; required to redirect to the login w/ a valid SAML token
    elem = driver.find_element(By.NAME, 'Login')
    elem.submit()
    del elem

    # Wait until the website loads before proceeding
    print("Obtaining SAML Token for CISCO Log-In...")
    WebDriverWait(driver, 5).until(
        EC.title_is("Polytechnique Montréal - Sign In")
    )

    # Request the user submit their email, and submit it to the webpage
    username = input("Username: ")
    username_elem = driver.find_element(By.NAME, 'identifier')
    username_elem.send_keys(username)
    username_elem.send_keys(Keys.RETURN)

    # Wait until the password field shows up
    password_elem = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.NAME, 'credentials.passcode'))
    )

    # TODO: Re-prompt the user every time the password fails
    # TODO: Allow the user to 'back out' and enter a different username

    # Request the user submit their password, and submit it to the webpage
    print("Attempting to submit credentials...")
    while True:
        # Request and submit a password
        password = getpass.getpass()
        password_elem.send_keys(password)
        password_elem.send_keys(Keys.RETURN)

        # Try and wait until the VPN page loads
        try:
            WebDriverWait(driver, 5).until(
                EC.title_is("Cisco Secure Client Installation")
            )
            break
        except TimeoutException as e:
            # Check if an error has appeared on the website
            target = driver.find_element(By.CLASS_NAME, 'error-16')

            # If we can't, time out as normal
            if target is None:
                raise e

            # Otherwise, try and reset the field to try again
            password_elem.clear()
            print("Credential submission failed. Please try again.")

    # Get the cookies from this web-page and tidy up
    vpn_cookie = driver.get_cookie('webvpn')['value']
    print("Obtained VPN Cookie!")
    return vpn_cookie



def get_webvpn_cookie():
    # Initiate a Firefox web driver
    print("Starting Firefox web driver...")
    opts = Options()
    opts.add_argument('--headless')
    web_driver = webdriver.Firefox(options=opts)
    print("Web driver started!")

    # Run the script, closing the driver when it finishes for any reason
    try:
        return login_with_credentials(web_driver)
    finally:
        print("Closing Selenium Client...")
        web_driver.close()
        web_driver.quit()
        print("Selenium Client Closed")


def main():
    # Get the VPN cookie using Selenium
    print('Program starting...')
    vpn_cookie = get_webvpn_cookie()
    print(vpn_cookie)

    # Use it to launch an OpenConnect VPN connection
    openconnect_cmd = [
        "sudo",
        "openconnect",
        "--protocol=anyconnect",
        "--authgroup=PolyQuartz",
        "-C", f"{vpn_cookie}",
        "https://ssl.vpn.polymtl.ca/"
    ]
    subprocess.run(openconnect_cmd, check=True)


if __name__ == "__main__":
    main()