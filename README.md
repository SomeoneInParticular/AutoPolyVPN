⚠️ **This tool has currently only been tested to work on Ubuntu 22.04 w/ Firefox for the PolyQuartz user group!** ⚠️

# Running the script

1. Ensure you have a working install of [openconnect](https://www.infradead.org/openconnect/index.html), and ensure it accesible in your system's `PATH`
2. Install the Firefox Web Driver ["Gecko"](https://github.com/mozilla/geckodriver/releases), and ensure it accesible in your system's `PATH`
3. Install the Python version of [Selenium](https://www.selenium.dev/)
4. [Optional] If you installed Selenium in a virtual environment, make sure it is active before proceeding
5. Run `python poly_vpn.py` and, when prompted, enter your PolyMTL Username and Password.
6. If your credentials are accepted, the OpenConnect VPN will attempt to boot using `sudo`, prompting you to enter your `sudo` password as it does so.
7. If everything worked, the console is now maintaining a VPN connection to PolyMTL!  
