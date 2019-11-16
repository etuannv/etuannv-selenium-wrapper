#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

__author__ = ["Tuan Nguyen"]
__copyright__ = "Copyright 2019, Tuan Nguyen"
__credits__ = ["Tuan Nguyen"]
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Production"
__author__ = "TuanNguyen"
__email__ = "etuannv@gmail.com"
__website__ = "https://etuannv.com"

import socket
hostname = socket.gethostname()
if 'MD104' in hostname:
    DEBUG=True
else:
    DEBUG=False



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import pickle
import logging
import random
import os
import time
import zipfile
import sys
from PIL import Image
from useragents import USER_AGENT_LIST
from useragents import MOBILE_USER_AGENT_LIST
from file_utils import readTextFileToList

class WebBrowser():
    """Class web browser"""
    def __init__(self, currentPath=None, driver = None, 
        timeout = 10, isDisableImage = False, 
        isDisableJavascript = False, downloadPath = None, 
        isMaximum = False, isHeadless = False, 
        proxyFilePath = None, changeProxyTotal=None, 
        isMobile=False, mobileUserAgentFilePath=None,
        userAgentFilePath=None
        ):
        self._currentPath = currentPath
        self._driver = driver
        self._timeout = timeout
        self._isDisableImage = isDisableImage
        self._isDisableJavascript = isDisableJavascript
        self._downloadPath = downloadPath
        self._isHeadLess = isHeadless
        self._isMaximum = isMaximum
        self._proxyFilePath = proxyFilePath
        self._changeProxyTotal = changeProxyTotal
        self._changeProxyCounter = 0
        self._currentProxyIp = 0
        self._isMobile = isMobile
        self._mobileUserAgentFilePath = mobileUserAgentFilePath
        self._restartBrowserCounter = 0
        self._userAgentFilePath = userAgentFilePath

        self.startBrowser()

    def getCurrentWindow(self):
        return self._driver.current_window_handle
    
    def swith2Window(self, window):
        self._driver.switch_to_window(window)

    def isPageLoaded(self, window):
        # logging.info("Checking if {} page is loaded.".format(self._driver.current_url))
        try:
            page_state = self._driver.execute_script('return document.readyState;')
            return page_state == 'complete'    
        except:
            return False
        
    def closeOtherLoadedWindows(self, window):
        for w in self._driver.window_handles:
            if w not in window:
                self._driver.switch_to.window(w)
                time.sleep(2)
                while not self.isPageLoaded(w):
                    
                    time.sleep(2)
                self._driver.close()
        # switch to main window
        self._driver.switch_to.window(window)

    def closeOtherWindows(self, window):
        for w in self._driver.window_handles:
            if w not in window:
                self._driver.switch_to.window(w)
                time.sleep(2)
                # while not self.isPageLoaded(w):
                #     time.sleep(2)
                self._driver.close()
        # switch to main window
        self._driver.switch_to.window(window)

    def getCookie(self):
        return self._driver.get_cookies()

    def clearCookie(self):
        return self._driver.delete_all_cookies()

    def saveCookie(self, filePath):
        pickle.dump( self._driver.get_cookies() , open(filePath,"wb"))
    
    def loadCookie(self, filePath):
        if os.path.isfile(filePath):
            cookies = pickle.load(open(filePath, "rb"))
            for cookie in cookies:
                self._driver.add_cookie(cookie)

    def getCurrentUrl(self):
        return self._driver.current_url

    def getPageSource(self):
        return self._driver.page_source
    
    # By Index
    # By Name or Id
    # By Web Element
    def switchToFrameByName(self, name, timeout=None):
        ''' Get one item by xpath'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located((By.NAME, name))
            )
            self._driver.switch_to_frame(name)
            return element
        except TimeoutException:
            logging.info(' Not found : %s', name)
            logging.debug('%s', TimeoutException)
            return None
        
    
    def switchToLastestWindow(self):
        # wait to make sure there are two windows open
        WebDriverWait(self._driver, 10).until(lambda d: len(d.window_handles) > 1)
        self._driver.switch_to_window(self._driver.window_handles[-1])
        # wait to make sure the new window is loaded
        WebDriverWait(self._driver, 10).until(lambda d: d.title != "")

    def closeCurrentWindows(self):
        self._driver.close()
        self._driver.switch_to_window(self._driver.window_handles[-1])

    
    def findVisibleByXpath(self, locator, timeout=None):
        ''' Get one item by xpath'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            )
            return element
        except TimeoutException:
            logging.info(' Find by xpath not found : %s', locator)
            logging.debug('%s', TimeoutException)
            return None
        

    def findByXpath(self, locator, timeout = None):
        ''' Get one item by xpath'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return element
        except TimeoutException:
            logging.info(' Find by xpath not found : %s', locator)
            logging.debug('%s', TimeoutException)
            return None

    def findByXpathFromElement(self, sel, locator , timeout = None):
        ''' Get one item by xpath'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(sel, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return element
        except TimeoutException:
            logging.info(' Find by xpath not found : %s', locator)
            logging.debug('%s', TimeoutException)
            return None

    def findAllByXpath(self, locator, timeout = None):
        ''' Get all items by xpath'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, locator)))
            return element
        except TimeoutException:
            logging.info(' Find by xpath not found : %s', locator)
            logging.debug('%s', TimeoutException)
            return []

    def findByClass(self, classname, timeout = None):
        ''' Get one item by class'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, classname)))
            return element
        except TimeoutException:
            logging.info(' Find by class not found : %s', classname)
            logging.debug('%s', TimeoutException)
            return None
            
    def findAllByClass(self, classname, timeout = None):
        ''' Get all item by class'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, classname)))
            return element
        except TimeoutException:
            logging.info(' Find by class not found : %s', classname)
            logging.debug('%s', TimeoutException)
            return []
    
    def selectDropdownByText(self, locator, text_value, timeout = None):
        tag = self.findByXpath(locator)
        if tag:
            select = Select(tag)
            select.select_by_visible_text(text_value)
        else:
            logging.info('Not found dropdown at xpath {}'.format(locator))
    
    def selectDropdownByValue(self, locator, value, timeout = None):
        tag = self.findByXpath(locator)
        if tag:
            select = Select(tag)
            select.select_by_value(value)
        else:
            logging.info('Not found dropdown at xpath {}'.format(locator))
    

    def isExistByXPath(self, locator, timeout = None):
        ''' Check if xpath is exists'''
        if not timeout:
            timeout = self._timeout
        try:
            WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False
        return True
    
                    
    def restartDriver(self):
        ''' Restart the browser'''
        logging.info("Restart browser")
        if self._driver:
            self._driver.close()
        time.sleep(1)
        self.startBrowser()

    def closeThisTab(self):
        ''' Exit the browser'''
        logging.info("Close current browser")
        if self._driver:
            self._driver.close()

    def exitDriver(self):
        ''' Exit the browser'''
        logging.info("Exit browser")
        if self._driver:
            self._driver.quit()

    def tryGetUrl(self, url, retry=5):
        get_result = False
        while retry > 0:
            retry -= 1
            get_result = self.getUrl(url)
            if get_result and 'This site can’t be reached' not in self.getPageSource():
                return True

            logging.info('Retry get url: {}'.format(url))
            time.sleep(2)
            self.restartDriver()
        
        return False


    def getUrl(self, url):
        if self._changeProxyTotal:
            self._changeProxyCounter+=1
            if self._changeProxyCounter > self._changeProxyTotal:
                self.restartDriver()
                self._changeProxyCounter = 0
        ''' Get an url '''
        try:
            self._driver.get(url)
            if self.hasCaptcha():
                logging.info("Page not loaded or has a captcha. Restart browser")
                self.restartDriver()
                self._restartBrowserCounter += 1
                if self._restartBrowserCounter > 5:
                    self._restartBrowserCounter = 0
                    # Skip this url
                    return False
                self.getUrl(url)
            
            return True
        except:
            logging.info("Fail to get %s", url)
            print("Unexpected error:", sys.exc_info()[0])
            return False
        
        
    
    def hasCaptcha(self):
        time.sleep(1)
        pagesource = self.getPageSource()

        if 'Blocked IP Address' in pagesource\
            or 'recaptcha-token' in pagesource\
            or 'I am not a robot' in pagesource\
            or 'not a robot' in pagesource\
            or 'Enter the characters you see below' in pagesource\
            or 'One more step' in pagesource\
            or 'Sorry! Something went wrong on our end' in pagesource:
            logging.info("Has captcha")
            return True
        else:
            return False
    
    def executeJavaScript(self,jsString):
        logging.info("Execute script {}".format(jsString))
        self._driver.execute_script(jsString)
        time.sleep(1)
    
    def scrollDown(self, number = 10):
        for i in range(0, number):
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    def scrollUp(self, number = 10):
        for i in range(0, number):
            self._driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
            time.sleep(1)
    def scrollTop(self):
        self._driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
    
    def scrollInfinity(self, iretry = 15):
        # scroll infinity
        # define initial page height for 'while' loop
        last_height = self._driver.execute_script("return document.body.scrollHeight")
        logging.info("Scrolling down ... ")
        retry = iretry
        page = 0
        while True:
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = self._driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                retry -= 1
                if retry < 0:
                    break
            else:
                last_height = new_height
                page += 1
                logging.info("Scroll down page: %d", page)
                retry = iretry

    def clickOnFly(self, element, x_offset = 10, y_offset=10, moveTimeout=1):
        ''' Click coordiate'''
        hover = ActionChains(self._driver).move_to_element(element).move_by_offset(x_offset, y_offset).click()
        hover.perform()
    
    def dismiss_alert(self):
        try:
            WebDriverWait(self._driver, 2).until(EC.alert_is_present())
            self._driver.switch_to_alert().accept()
            return True
        except TimeoutException:
            return False
        
    def getScreenShotByXpath(self, xpath, result_path):
        element = self.findByXpath(xpath)
        if not element:
            logging.info("Not found element at xpath: %d", xpath)

        location = element.location
        size = element.size

        self._driver.save_screenshot("temp.png")

        x = location['x']
        y = location['y']
        width = location['x']+size['width']
        height = location['y']+size['height']

        im = Image.open('temp.png')
        im = im.crop((int(x), int(y), int(width), int(height)))
        im.save(result_path)
        # Delete temp image
        if os.path.isfile('temp.png'):
            os.remove('temp.png')
            
        return result_path

    def hoverElement(self, element, moveTimeout=1):
        ''' Hover an element'''
        hover = ActionChains(self._driver).move_to_element(element)
        hover.perform()

    def clickElement(self, element, moveTimeout=1):
        try:
            ''' Click an element'''
            actions = ActionChains(self._driver)
            actions.move_to_element(element)
            actions.perform()
            time.sleep(moveTimeout)
            actions.click(element)
            actions.perform()
            return True
        except:
            logging.info("Can't click element")
            return False
    
    def clickElementToNewTab(self, element, moveTimeout=3):
        try:
            ''' Click an element'''
            actions = ActionChains(self._driver)
            actions.move_to_element(element)
            actions.perform()
            time.sleep(moveTimeout)
            
            if os.name == 'posix':
                actions.key_down(Keys.COMMAND, element).click(element).key_up(Keys.COMMAND, element)
            else:
                actions.key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL)
            actions.perform()
            return True
        except:
            logging.info("Can't click element")
            return False

    def sendKeys(self, key):
        ''' Send key to brower'''
        actions = ActionChains(self._driver)
        actions.send_keys(key)
        actions.perform()

    def getPlugin(self, proxy_host, proxy_port, proxy_user, proxy_pass):
        logging.info('set proxy {}:{} with username {}'.format(proxy_host, proxy_port, proxy_user))
        
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
        """ % (proxy_host, proxy_port, proxy_user, proxy_pass)
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        
        return pluginfile

    def startBrowser(self):
        ''' Start the browser'''
        logging.info("Start browser")

        chromeOptions = webdriver.ChromeOptions()

        # If have proxy path then config proxy
        if self._proxyFilePath:
            proxies = readTextFileToList(self._proxyFilePath)
            
            proxy_with_password = []
            # READ PROXY
            for proxy in proxies:
                if '@' in proxy:
                    part = proxy.split('@')
                    username, password = part[0].split(':')
                    host, port = part[1].split(':')
                    proxy_with_password.append({
                        'proxy_host': '{}'.format(host),
                        'proxy_port': port,
                        'proxy_user': username,
                        'proxy_pass': password,
                    })
            
            # if proxy with password 
            if proxy_with_password:
                randomIp = random.choice(proxy_with_password)
                self._currentProxyIp = randomIp['proxy_host']
                chromeOptions.add_extension(self.getPlugin(**randomIp))
            else:
                proxyip = random.choice(proxies)
                logging.info("proxy ip: {}".format(proxyip))
                self._currentProxyIp = proxyip.split(':')[0]
                chromeOptions.add_argument('--proxy-server={}'.format(proxyip))

        if self._isHeadLess:
            logging.info('Start browser in headless mode')
            chromeOptions.add_argument("--headless")
            chromeOptions.add_argument("--disable-gpu") 

        if DEBUG:
            chromeOptions.add_extension("chropath.zip")
            # chromeOptions.add_extension("edit_this_cookie.zip")

        
        # chromeOptions.add_argument('--disable-extensions')
        # chromeOptions.add_argument('--profile-directory=Default')
        # chromeOptions.add_argument("--incognito")
        # chromeOptions.add_argument("--disable-plugins-discovery");
        # chromeOptions.add_argument("--start-maximized")
        # chromeOptions.add_argument("--no-experiments")
        chromeOptions.add_argument("--disable-translate")
        # chromeOptions.add_argument("--disable-plugins")
        # chromeOptions.add_argument("--disable-extensions");
        # chromeOptions.add_argument("--no-sandbox")
        # chromeOptions.add_argument("--disable-setuid-sandbox")
        chromeOptions.add_argument("--no-default-browser-check")
        # chromeOptions.add_argument("--clear-token-service")
        chromeOptions.add_argument("--disable-default-apps")
        
        if self._userAgentFilePath:
            # READ USER AGENTS
            ua_list = readTextFileToList(self._userAgentFilePath)
            user_agent = random.choice(ua_list)
        else:
            user_agent = random.choice(USER_AGENT_LIST)
        
        logging.info('User-agent: {}'.format(user_agent))
        chromeOptions.add_argument('user-agent={}'.format(user_agent))

        chromeOptions.add_argument("test-type")
        chromeOptions.add_argument('--log-level=3')
        
        if(self._isMaximum):
            chromeOptions.add_argument("start-maximized")
        
        prefs = { "profile.default_content_setting_values.notifications": 2 }
        
        if self._isDisableImage:
            prefs["profile.managed_default_content_settings.images"] = 2

        if self._isDisableJavascript:
            prefs["profile.managed_default_content_settings.javascript"] = 2
        
        chromeOptions.add_experimental_option("prefs",prefs)
        # chromeOptions.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])

        if self._downloadPath:
            prefs = {'plugins': {'plugins_disabled': ['Chrome PDF Viewer']}, 'download': {'default_directory': self._downloadPath, "directory_upgrade": True}}
        
        if os.name == 'posix':
            if self._currentPath:
                chromedriver=os.path.join(self._currentPath,"chromedriver")
            else:
                chromedriver='chromedriver'
        else:
            if self._currentPath:
                chromedriver=os.path.join(self._currentPath,"chromedriver.exe")
            else:
                chromedriver='chromedriver.exe'
        
        
        if self._isMobile:
            if self._mobileUserAgentFilePath:
                mobile_agents = readTextFileToList(self._mobileUserAgentFilePath)
                random_agent = random.choice(mobile_agents)
            else:
                random_agent = random.choice(MOBILE_USER_AGENT_LIST)
            
            logging.info('Mobile User-agent: {}'.format(random_agent))
            mobile_emulation = {
                "deviceMetrics": 
                    { 
                        "width": 414, 
                        "height": 816, 
                        "pixelRatio": 3.0 
                    },
                "userAgent":  random_agent
                }
            
            chromeOptions.add_experimental_option("mobileEmulation", mobile_emulation)


        

        # self._driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions,desired_capabilities=desired_cap)
        self._driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

        # self._driver.delete_all_cookies()
        
        # if self._isMobile:
        #     self._driver.set_window_size(414,816)

        self._driver.set_page_load_timeout(60)
        # self._driver.set_window_position(0,0)
        #driver.set_window_position(-10000,0)
        # self._driver.switch_to_window(self._driver.current_window_handle)


    def tryClick(self, element, num = 10):
        ''' Try to click an element'''
        is_clicked = False
        step = 0
        while not is_clicked and step < num:
            try:
                is_clicked = self.clickElement(element, 5)
                is_clicked = True
            except: 
                time.sleep(1)
                logging.info("try click %s", element)
                is_clicked = False
            step+=1
        
        return is_clicked

    
    def tryClickByXpath(self, locator, num = 10):
        ''' Try to click an element'''
        is_clicked = False
        retry = num
        while not is_clicked and num > 0:
            num -= 1
            element = self.findByXpath(locator)
            if element:
                is_clicked = self.clickElement(element, moveTimeout=retry-num)
                if is_clicked:
                    return True
            # Else try click again    
            time.sleep(1)
            logging.info("try click {} x {}".format(num, locator))
        
        return is_clicked
