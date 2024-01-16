import os
import zipfile
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from pathlib import Path

PROXY_PASS = 'proxy-password' # password
def init_proxy_config(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    return [manifest_json, background_js]



def get_chromedriver(profile_id: str, *, user_agent=None):
    # path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()

    # pluginfile = 'proxy_auth_plugin.zip'

    # proxy_config = init_proxy_config(proxy['host'], proxy['port'], proxy['username'], proxy['password'])

    # with zipfile.ZipFile(pluginfile, 'w') as zp:
    #     zp.writestr("manifest.json", proxy_config[0])
    #     zp.writestr("background.js", proxy_config[1])
    # chrome_options.add_extension(pluginfile)

    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    
    # block show notifications from websites
    chrome_options.add_argument('--disable-notifications')  

    user_data_directory = rf"{Path.cwd()}\user-profiles\{profile_id}"
    # user_data_directory = "./user-profiles/"+profile_id

    chrome_options.add_argument(f"user-data-dir={user_data_directory}") #Path to your chrome profile

    # w = webdriver.Chrome(chrome_options=options)

    # service = Service(executable_path='./chromedriver.exe')
    
    driver = webdriver.Chrome(
        # os.path.join(path, 'chromedriver'),
        # service=service,
        options=chrome_options)
    return driver
