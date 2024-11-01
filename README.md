# SUFSD (Standart Utilits For Selenium_Driverless)



## What is this?

When parsing different sites, you almost always have to copy+paste some functions; this module was created to make such code easier. It includes the most commonly used functions when parsing. In the future it will be very actively replenished.



## Installation

`pip install -U sufsd`



## Dependencies



- Python >= 3.8
- Google-Chrome installed (Chromium not tested)



## Usage

```python
import asyncio
import os
import base64
import logging

from sufsd import init_browser
from sufsd import init_logging
from sufsd import go_to_url
from sufsd import scroll_page
from sufsd import parse_element
from sufsd import By

LINK = 'https://pypi.org/project/sufsd'
PATH_TO_DIR = os.path.dirname(__file__)

async def main():
    await init_logging(to_console=True, filename= f'{PATH_TO_DIR}/logs.log')
    try:
        browser = await init_browser(
            proxy=False,
            headless=False,
            maximize_window=True)
        
        await go_to_url(browser, LINK)
        
        logging.info(f'Current version: {await parse_element(browser, By.XPATH, "/html/body/main/div[1]/div/div[1]/h1", only_nums=True)}')

        await scroll_page(browser)
        
        logging.info(f'Title page: {await browser.title}.')
        
        bytes_for_pdf = await browser.print_page()
        
        with open(f'{PATH_TO_DIR}/sufsd.pdf', 'wb') as file:
            file.write(base64.b64decode(bytes_for_pdf))
        
        logging.info('Created file sufsd.pdf.')
        
    except Exception as error:
        logging.info(f'ERROR: {error}')
    
    finally:
        await browser.quit()
        logging.info('The browser was closed.')


if __name__ == '__main__':
    asyncio.run(main())
```



## Utils implemented so far

`init_browser(proxy = None, headless = True, maximize_window = False) #async`

Browser initialization, taking into account human delays, keeping logs.
     

**Parameters:**    

- proxy (`str`)  -  Proxy in the format `ip:port` or `user@password:ip:port`

- headless (`bool`)  -  Headless on/off.

- maximize_window (`bool`)  -  Maximize_window on/off

**Return type:**   `class selenium_driverless.webdriver.Chrome`

------

`go_to_url(browser, url) #async`

Сonfidently go to the link (it is impossible not to get to the site due to any lags/proxy speed limits), taking into account human delays, keeping logs.

**Parameters:**    

- browser (`Chrome`)  -  Browser selenium_driverless.webdriver.Chrome.

- url (`str`)  -  Link to site.

**Return type:**    `None`

------

`click(browser, by, value, ID = None) #async`

Click to button, finded by value. If ID is specified, it uses find_elements(by, value), and then element = finded_elements[ID]

**Parameters:**

- browser (`Chrome`)  -  Browser selenium_driverless.webdriver.Chrome.

- by (`str`)  -  One of the locators at `By`.

- value (`str`)  -  The actual query to find by.

- ID (`int`)  -  ID for the WebElement, if there are several of them.

**Return type:**    `None`

------

`init_logging(to_console = True, filename = f'{os.path.dirname(__file__)}logs.log') #async`

Enabling logs.

**Parameters:**   

- to_console (`bool`)  -  On/off logging to console.
- filename (`str | bool`)  -  On/off logging to filename. Filename=False to off logging to file.

**Return type:**  `None`

------

`auth(browser, url, path_to_cookies) #async`

The browser goes to the url and re-enters the site with cookies from path_to_cookies, keeping logs.

**Parameters:**    

- browser (`Chrome`)  -  Browser selenium_driverless.webdriver.Chrome.

- url (`str`)  -  Link to site.

- path_to_cookies (`str`)  -  Path to file with cookies.

**Return type:**    `None`

------

`save_cookie(browser, path, close_browser = False) #async`

Saves the browser cookie to a file located at path if close_browser then closes the browser, keeping logs.

**Parameters:**    

- browser (`Chrome`)  -  Browser selenium_driverless.webdriver.Chrome.

- path (`str`)  - Path to file.

- close_browser (`bool`)  -  If True then closes the browser.

**Return type:**    `None`

------

`scroll_page(browser, by = 'class_name', value = None, sleep = [12, 15]) #async`

Full scrolling of the page, with pressing the "Upload more" button by class class_name, given that the site may lag, keeping logs.

**Parameters:**

- browser(`Chrome`)  -  Browser selenium_driverless.webdriver.Chrome.

- by (`str`)  -  One of the locators at `By` for button "Upload more".

- value (`str`)  -  The actual query to find the button "Upload more" by.

- sleep (`list`)  -  The delay between "Upload more" button presses, a random number from the interval.

**Return type:**    `None`

------

`parse_element(browser_or_WebElement, by, value, ID = None, no_clean = False, full_clean = False, only_nums = False) #async`

Searches for a WebElement by value, takes its text, clears it using strip(). If ID is specified, it uses find_elements(by, value), and then element = finded_elements[ID]. If no_clean does not use strip(). If only_nums returns only numbers from the text WebElement. If full_clean completely removes line breaks and extra spaces(replacing with one).

**Parameters:**

- browser_or_WebElement (`Chrome | WebElement`)  -  Browser or WebElement where the subsequent WebElement will be searched.

- by (`str`)  -  One of the locators at `By`.

- value (`str`)  -  The actual query to find by.

- ID (`int`)  -  ID for the WebElement, if there are several of them.

- no_clean (`bool`)  -  True for off use strip().

- full_clean (`bool`)  -  True for completely removes line breaks and extra spaces(replacing with one).

- only_nums (`bool`)  -  True for returns only numbers, ',' and '.' from the text WebElement.

**Return Type:**    `str`

------

`change_proxy(browser, proxy, refresh = False) #async`

Modifies the proxy browser to a proxy. If refresh, it goes back to the page.

**Parameters:**

- browser (`Chrome`)  -  Browser selenium_driverless.webdriver.Chrome.

- proxy (`str`)  -  Proxy format 'ip:port' or 'user:password@ip:port'

- refresh (`bool`)  -  On/off refresh to site after changing the proxy.

**Return type:**    `None`

------

`parse_pages(browser, by_for_num_pages, value_for_num_pages, by_for_next_page, value_for_next_page, func_for_every_page, args_for_func_for_every_page, ID_for_value_for_num_pages = None, ID_for_value_for_next_page = None, add_func_for_first_page = None, args_for_funs_for_first_page = None, skip_pages = None) #async`

Complete passage through all pages of the site by clicking the next page button(browser.find_element(by_for_next_page, value_for_next_page)), on each page using the asynchronous function func_for_every_page(args_for_func_for_every_page). If func_for_first_page is specified, the preface on the first page will use func_for_first_page(args_for_func_first_page). If skip_pages is specified, the browser will pass fewer (recent) pages on skip_pages.

**Parameters:**

browser (`Chrome`)  -  Browser selenium_driverless.webdriver.Chrome.

by_for_num_pages (`str`)  -  One of the locators at `By` for place, where is specified num_pages.

value_for_num_pages (`str`)  -  The actual query to find by place, where is specified num_pages.

by_for_next_page (`str`)  -  One of the locators at `By` for button "Next page".

value_for_next_page (`str`)  -  The actual query to find button "Next page" by.

func_for_every_page (`func`)  -  The function that will be used on each page.

args_for_func_for_every_page (`list`)  -  Arguments for `func_for_every_page`

ID_for_value_for_num_pages (`int`)  -  ID for the WebElement with num_pages, if there are several of them.

ID_for_value_for_next_page (`int`)  -  ID for the WebElement with button "Next page", if there are several of them.

add_func_for_first_page (`func`)  -  The function that will be used preface on the first_page.

args_for_func_for_first_page (`list`)  -  Arguments for `add_func_for_first_page`

skip_pages (`int`)  -  The number of pages to skip at the end.

**Return type:**    `None`

------

### **By Element Locator**

Set of supported locator strategies. Their supported aliases are also indicated on the right, the case is not important.

- ​    `ID='id'`
- ​    `NAME='name'`
- ​    `XPATH='xpath'`
- ​    `TAG_NAME='tag name'`  Also:`tag_name` , `tag`
- ​    `CLASS_NAME='class name'` Also:`class_name` , `class`
- ​    `CSS_SELECTOR='css selector'` Also:`css`
- ​    `CSS='css selector'` Also:`css`



## Author

Developer: https://t.me/VHdpcj
