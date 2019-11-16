# etuannv-selenium-wrapper

*This is Python selenium wrapper which is written by etuannv.com*

How to use


```browser = WebBrowser(
    currentPath=None,   # current working path
    driver = None,      # copy another driver
    timeout = 10,       # default web browser timeout
    isDisableImage = False,         # is disable load images
    isDisableJavascript = False,    # is disable javascript on the web browser
    downloadPath = None,            # default download page
    isMaximum = False,              # browser load maximum 
    isHeadless = False,             # start browser in headless mode (hindden the browser)
    proxyFilePath = None,           # proxy file path 
    changeProxyTotal=None,          # Auto change proxy after x times load page
    isMobile=False,                 # Does it browser mobile 
    mobileUserAgentFilePath=None,   # Mobile user agent file path
    userAgentFilePath=None          # User agent file path
);
```
