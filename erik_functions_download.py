'''
Help functions to download various content from the web

ToDo:
google maps cuts
eniro cuts

Eniro:
https://kartor.eniro.se/?c=58.405467,15.619426&z=14&l=aerial


'''
import os.path
import sys

import wget
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options as Options_chrome
from selenium.webdriver.opera.options import Options as Options_opera
from selenium.webdriver.firefox import
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.opera import OperaDriverManager
#from webdriver_manager.firefox import


# Download file from url to a local path
def download_file(url, dst_dir, update=False):
    print('Downloading ' + url)
    wget.download(url, out=dst_dir)
    print('Downloaded ' + url)


def get_webdriver(manger='firefox', wait=1):
    DRIVER_PATH_CHROME = r'C:\Program Files\Google\Chrome\Application'
    DRIVER_PATH_FIREFOX = r'C:\Program Files\Mozille Firefox'
    BINARY_FIREFOX = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    print(BINARY_FIREFOX)

    sys.path.append(DRIVER_PATH_CHROME)
    sys.path.append(DRIVER_PATH_FIREFOX)

    options = Options_opera()
    options.headless = True
    options.add_argument('--window-size=1920,1200')

    #driver = webdriver.Firefox(firefox_binary=BINARY_FIREFOX)
    driver = webdriver.Firefox(executable_path=BINARY_FIREFOX)

    '''
    if manger=='firefox':
        webDriver = webdriver.Firefox(options=options)
        webDriver.implicitly_wait(wait)
    elif manger == 'chrome':
        webDriver = webdriver.Chrome(options=options)
        webDriver.implicitly_wait(wait)
    elif manger == 'opera':
        webDriver = webdriver.Opera(options=options)
        webDriver.implicitly_wait(wait)
    else:
        webDriver = False
    '''
    driver.implicitly_wait(1)

    return driver


def download_geo_eniro_screenshot(driver, gps_longitude, gps_latitude, dir_dst, zoom=13, filename=None):
    path_save = os.path.join(dir_dst, filename)
    url = r'https://kartor.eniro.se/?c=58.405467,15.619426&z=15&l=aerial'

    driver.get(url)
    driver.get_screenshot_as_file(path_save)


if __name__ == '__main__':
    dir_dst = r'C:\ai\datasets\gis\eniro\linkoping'
    filename = 'linkoping.png'

    driver = get_webdriver()

    for zoom in range(13,15 + 1):
        print(zoom)
        filename = filename + str(zoom)
        download_geo_eniro_screenshot(driver, 1, 1, zoom=zoom ,dir_dst=dir_dst, filename=filename)

    driver.quit()