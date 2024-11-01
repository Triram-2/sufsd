import asyncio
import random
import os
import logging
import sys
import pickle
import re

from logging import info

from selenium_driverless import webdriver
from selenium_driverless.types.by import By


# Инициализация браузера.
async def init_browser(proxy = None, headless = True, maximize_window = False):
    try:
        options = webdriver.ChromeOptions()
        if proxy:
            options.single_proxy = f'http://{proxy}/'
        options.startup_url = 'https://google.com/'
        options.headless = headless

        browser = await webdriver.Chrome(options = options)
        if maximize_window:
            await browser.maximize_window()
        await asyncio.sleep(random.uniform(2, 3))
        info(f'Один из браузеров инициализирован с прокси: {proxy}.')

        return browser
    except Exception as error:
        info(f'Ошибка при инициализации браузера: {error}')


# Переход по ссылке.
async def go_to_url(browser, url):
    try:
        try:
            await browser.get(url, timeout=150)
        except:
            try:
                await browser.get(url, timeout=250)
            except:
                await browser.get(url, timeout=300)
        info(f'Браузер перешёл на {url}.')
        await asyncio.sleep(random.uniform(3, 5))
    except Exception as error:
        info(f'Ошибка при переходе на {url}: {error}.')


# Нажатие по кнопке.
async def click(browser, by, value, ID = None):
    if not ID:
        try:
            if by == 'ID':
                button_next_page = await browser.find_element(By.ID, value, timeout = 30)
            elif by == 'NAME':
                button_next_page = await browser.find_element(By.NAME, value, timeout = 30)
            elif by == 'XPATH':
                button_next_page = await browser.find_element(By.XPATH, value, timeout = 30)
            elif by == 'TAG NAME' or 'TAG_NAME' or 'TAG':
                button_next_page = await browser.find_element(By.TAG_NAME, value, timeout = 30)
            elif by == 'CLASS NAME' or 'CLASS_NAME' or 'CLASS':
                button_next_page = await browser.find_element(By.CLASS_NAME, value, timeout = 30)
            elif by == 'CSS SELECTOR' or 'CSS':
                button_next_page = await browser.find_element(By.CSS_SELECTOR, value, timeout = 30)
            else:
                raise TypeError(f'Неизвестный by: {by}')
        except:
            info(f'Браузер не смог найти {value} по {by}.')
            button_next_page = 'Не найдено/ошибка'
    else:
        try:
            if by == 'ID':
                button_next_page = await browser.find_elements(By.ID, value, timeout = 30)
            elif by == 'NAME':
                button_next_page = await browser.find_elements(By.NAME, value, timeout = 30)
            elif by == 'XPATH':
                button_next_page = await browser.find_elements(By.XPATH, value, timeout = 30)
            elif by == 'TAG NAME' or 'TAG_NAME' or 'TAG':
                button_next_page = await browser.find_elements(By.TAG_NAME, value, timeout = 30)
            elif by == 'CLASS NAME' or 'CLASS_NAME' or 'CLASS':
                button_next_page = await browser.find_elements(By.CLASS_NAME, value, timeout = 30) 
            elif by == 'CSS SELECTOR' or 'CSS':
                button_next_page = await browser.find_elements(By.CSS_SELECTOR, value, timeout = 30)
            else:
                raise TypeError(f'Неизвестный by: {by}')
            button_next_page = button_next_page[ID]
        except:
            info(f'Браузер не смог найти {ID} {value} по {by}.')
            button_next_page = 'Не найдено/ошибка'
    if button_next_page != 'Не найдено/ошибка':
        await button_next_page.click()
        info(f'Браузер нажал на кнопку {by}:{value}.')
        await asyncio.sleep(random.uniform(2, 4))
    else:
        info('Произошла ошибка при попытке найти кнопку.')
        await asyncio.sleep(random.uniform(3, 5))


# Настройка логов.
async def init_logging(to_console = True, filename = f'{os.path.dirname(__file__)}/logs.log'):
    if to_console and not filename:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO, filename=filename)
        if to_console:
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


# Аутентификация в аккаунт.
async def auth(browser, url, path_to_cookies):
    try:
        await go_to_url(browser, url)
        await asyncio.sleep(random.uniform(0.5, 1.5))

        try:
            for cookie in pickle.load(open(path_to_cookies, 'rb')):
                await browser.add_cookie(cookie)
        except:
            for cookie in pickle.load(open(path_to_cookies, 'rb')):
                await browser.add_cookie(cookie)
        
        await asyncio.sleep(random.uniform(0.5, 1.5))
        await go_to_url(browser, url)
        info('Браузер авторизовался.')
    except Exception as error:
        info(f'Ошибка при попытке авторизации: {error}')
        info('Завершение работы программы...')
        quit()


# Сохранение файлов cookie.
async def save_cookie(browser, path, close_browser = False):
    try:
        await asyncio.sleep(random.uniform(3, 5))
        with open(path, 'wb') as file:
            pickle.dump(await browser.get_cookies(), file)
        info(f'Сохранены куки браузера.') 
        if close_browser:
            try:
                await browser.quit()
                info('Работа браузера завершена.')
            except:
                ...
    except Exception as error:
        info(f'Ошибка при попытке сохранить cookie: {error}')


# Полностью скроллит страницу.
async def scroll_page(browser, by = 'class_name', value = None, sleep = [12, 15]):
    try:
        if not by or not value:
            by = by.upper()
        last_num = 0
        count = 0
        while True:
            await browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            await asyncio.sleep(random.uniform(2, 3))
            if not by or not value:
                raise ValueError('Только скроллинг - без прожатий кнопки.')
            info("Браузер пробует нажать на кнопку 'Загрузить ещё'...")
            if by == 'ID':
                button = await browser.find_element(By.ID, value, timeout = 10)
            elif by == 'NAME':
                button = await browser.find_element(By.NAME, value, timeout = 10)
            elif by == 'XPATH':
                button = await browser.find_element(By.XPATH, value, timeout = 10)
            elif by == 'TAG NAME' or 'TAG_NAME' or 'TAG':
                button = await browser.find_element(By.TAG_NAME, value, timeout = 10)
            elif by == 'CLASS NAME' or 'CLASS_NAME' or 'CLASS':
                button = await browser.find_element(By.CLASS_NAME, value, timeout = 10)
            elif by == 'CSS SELECTOR' or 'CSS':
                button = await browser.find_element(By.CSS_SELECTOR, value, timeout = 10)
            else:
                raise TypeError(f'Неизвестный by: {by}')
            await button.click()
            info("Браузер проскроллил страницу и нажал на кнопку 'Загрузить ещё'...")
            await asyncio.sleep(random.uniform(sleep[0], sleep[1]))
            blocks = await browser.find_elements(By.TAG_NAME, 'div')
            current_num = len(blocks)
            if current_num == last_num:
                count += 1
            last_num = current_num
            if count == 2:
                raise ValueError("Сайт залагал, перестал нажимать кнопку 'Загрузить ещё'.")
    except Exception as error:
        info(f'Вероятно страница полностью проскроллена, иначе возникла какая-то ошибка. Вывод: {error}')


# Отыскивает элемент, возвращает очищенный текст элемента.
async def parse_element(browser_or_WebElement, by, value, ID = None, no_clean = False, full_clean = False, only_nums = False):
    try:
        by = by.upper()
        if not ID:
            try:
                if by == 'ID':
                    element = await browser_or_WebElement.find_element(By.ID, value, timeout = 30)
                elif by == 'NAME':
                    element = await browser_or_WebElement.find_element(By.NAME, value, timeout = 30)
                elif by == 'XPATH':
                    element = await browser_or_WebElement.find_element(By.XPATH, value, timeout = 30)
                elif by == 'TAG NAME' or 'TAG_NAME' or 'TAG':
                    element = await browser_or_WebElement.find_element(By.TAG_NAME, value, timeout = 30)
                elif by == 'CLASS NAME' or 'CLASS_NAME' or 'CLASS':
                    element = await browser_or_WebElement.find_element(By.CLASS_NAME, value, timeout = 30)
                elif by == 'CSS SELECTOR' or 'CSS':
                    element = await browser_or_WebElement.find_element(By.CSS_SELECTOR, value, timeout = 30)
                else:
                    raise TypeError(f'Неизвестный by: {by}')
            except:
                info(f'Браузер не смог найти {value} по {by}.')
                return 'Не найдено/ошибка'
        else:
            try:
                if by == 'ID':
                    element = await browser_or_WebElement.find_elements(By.ID, value, timeout = 30)
                elif by == 'NAME':
                    element = await browser_or_WebElement.find_elements(By.NAME, value, timeout = 30)
                elif by == 'XPATH':
                    element = await browser_or_WebElement.find_elements(By.XPATH, value, timeout = 30)
                elif by == 'TAG NAME' or 'TAG_NAME' or 'TAG':
                    element = await browser_or_WebElement.find_elements(By.TAG_NAME, value, timeout = 30)
                elif by == 'CLASS NAME' or 'CLASS_NAME' or 'CLASS':
                    element = await browser_or_WebElement.find_elements(By.CLASS_NAME, value, timeout = 30) 
                elif by == 'CSS SELECTOR' or 'CSS':
                    element = await browser_or_WebElement.find_elements(By.CSS_SELECTOR, value, timeout = 30)
                else:
                    raise TypeError(f'Неизвестный by: {by}')
                element = element[ID]
            except:
                info(f'Браузер не смог найти {ID} {value} по {by}.')
                return 'Не найдено/ошибка'
        element = await element.text
        if only_nums:
            element = re.sub(r'[^0-9,.]', '', element)
        if not no_clean:
            element = element.strip()
        if full_clean:
            element = re.sub('[\n\r]+', '', element)
            element = element.replace('\n', '')
            element = re.sub('\s+', ' ', element)
            element = element.strip()
        return element
    except Exception as error:
        info(f'Ошибка при попытке спарсить {value} по {by}: {error}')


# Изменяет прокси в браузере, перезаходит на страницу.
async def change_proxy(browser, proxy, refresh = False):
    try:
        await browser.set_single_proxy(proxy)
        await asyncio.sleep(random.uniform(2, 3))
        if refresh:
            await browser.get(await browser.current_url)
    except Exception as error:
        info(f'Ошибка при попытке изменить proxy в браузере на {proxy}: {error}')


# Проходит по всем страницам.
async def parse_pages(browser, by_for_num_pages, value_for_num_pages, by_for_next_page, value_for_next_page, func_for_every_page = None, args_for_funs_for_every_page = None, ID_for_value_for_num_pages = None, ID_for_value_for_next_page = None, add_func_for_first_page = None, args_for_func_for_first_page = None, skip_pages = None):
    async def next_page(browser, by_for_next_page, value_for_next_page):
        by_for_next_page = by_for_next_page.upper()
        if not ID_for_value_for_next_page:
            try:
                if by_for_next_page == 'ID':
                    button_next_page = await browser.find_element(By.ID, value_for_next_page, timeout = 30)
                elif by_for_next_page == 'NAME':
                    button_next_page = await browser.find_element(By.NAME, value_for_next_page, timeout = 30)
                elif by_for_next_page == 'XPATH':
                    button_next_page = await browser.find_element(By.XPATH, value_for_next_page, timeout = 30)
                elif by_for_next_page == 'TAG NAME' or 'TAG_NAME' or 'TAG':
                    button_next_page = await browser.find_element(By.TAG_NAME, value_for_next_page, timeout = 30)
                elif by_for_next_page == 'CLASS NAME' or 'CLASS_NAME' or 'CLASS':
                    button_next_page = await browser.find_element(By.CLASS_NAME, value_for_next_page, timeout = 30)
                elif by_for_next_page == 'CSS SELECTOR' or 'CSS':
                    button_next_page = await browser.find_element(By.CSS_SELECTOR, value_for_next_page, timeout = 30)
                else:
                    raise TypeError(f'Неизвестный by: {by_for_next_page}')
            except:
                info(f'Браузер не смог найти {value_for_next_page} по {by_for_next_page}.')
                button_next_page = 'Не найдено/ошибка'
        else:
            try:
                if by_for_next_page == 'ID':
                    button_next_page = await browser.find_elements(By.ID, value_for_next_page, timeout = 30)
                elif by_for_next_page == 'NAME':
                    button_next_page = await browser.find_elements(By.NAME, value_for_next_page, timeout = 30)
                elif by_for_next_page == 'XPATH':
                    button_next_page = await browser.find_elements(By.XPATH, value_for_next_page, timeout = 30)
                elif by_for_next_page == 'TAG NAME' or 'TAG_NAME' or 'TAG':
                    button_next_page = await browser.find_elements(By.TAG_NAME, value_for_next_page, timeout = 30)
                elif by_for_next_page == 'CLASS NAME' or 'CLASS_NAME' or 'CLASS':
                    button_next_page = await browser.find_elements(By.CLASS_NAME, value_for_next_page, timeout = 30) 
                elif by_for_next_page == 'CSS SELECTOR' or 'CSS':
                    button_next_page = await browser.find_elements(By.CSS_SELECTOR, value_for_next_page, timeout = 30)
                else:
                    raise TypeError(f'Неизвестный by: {by_for_next_page}')
                button_next_page = button_next_page[ID_for_value_for_next_page]
            except:
                info(f'Браузер не смог найти {ID_for_value_for_next_page} {value_for_next_page} по {by_for_next_page}.')
                button_next_page = 'Не найдено/ошибка'
        if button_next_page != 'Не найдено/ошибка':
            await button_next_page.click()
            info(f'Браузер переключился на следующую страницу.')
            await asyncio.sleep(random.uniform(2, 4))
        else:
            info('Произошла ошибка при попытке найти кнопку для следующей страницы.')
            await asyncio.sleep(random.uniform(3, 5))
    try:
        num_pages = await parse_element(browser, by_for_num_pages, value_for_num_pages, only_nums=True, ID=ID_for_value_for_num_pages)
        info(f'Всего страниц: {num_pages}')
        await asyncio.sleep(random.uniform(0.5, 1.5))
    except Exception as error:
        info(f'Ошибка при попытке получить количество страниц: {error}')
    
    if skip_pages:
        num_pages -= skip_pages
    if num_pages <= 0:
        info(f'Браузер прошёл все страницы на сайте.')
        return

    try:
        if add_func_for_first_page:
            await add_func_for_first_page(*args_for_func_for_first_page)
        if func_for_every_page:
            await func_for_every_page(*args_for_funs_for_every_page)
        for i in range(num_pages - 1):
            await next_page(browser, by_for_next_page, value_for_next_page)
            if func_for_every_page:
                await func_for_every_page(*args_for_funs_for_every_page)
            await asyncio.sleep(random.uniform(3, 5))
        await asyncio.sleep(random.uniform(2, 3))
        info(f'Браузер прошёл все страницы на сайте.')

    except Exception as error:
        info(f'Ошибка при проходе по страницам: {error}')
