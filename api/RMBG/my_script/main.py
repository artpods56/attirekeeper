from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from functools import wraps
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

chrome_profile_path = Path("C:/Users/artpo/AppData/Local/Google/Chrome/User Data/")

chrome_options = Options()
chrome_options.add_argument(f'user-data-dir={chrome_profile_path}')
chrome_options.add_argument("profile-directory=Default")
chrome_options.add_experimental_option('detach', True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Setup Chrome driver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


def delay_decorator(delay=1):
    """Decorator that adds a delay after the execution of a function or method."""
    def wrapper_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            time.sleep(delay)
            return result
        return wrapper
    return wrapper_function

class DriverWrapper:
    def __init__(self, driver):
        self.driver = driver

    @delay_decorator(delay=1)
    def get(self, url):
        return self.driver.get(url)

    @delay_decorator(delay=1)
    def find_element(self, by, value):
        return self.driver.find_element(by, value)
    
    def execute_script(self, script, element):
        return self.driver.execute_script(script, element)

#driver = DriverWrapper(driver)

#driver.get('https://www.vinted.pl/items/new')
driver.get('https://antcpt.com/score_detector/')


# sample_image_path = Path("D:/Projects/bg_remover_model/RMBG-1.4/img_sample.jpeg")

# #check if sample_image_path has been found
# if not sample_image_path.exists():
#     print(f"File not found: {sample_image_path}")
# else:
#     print(f"File found: {sample_image_path}")
#     sample_image_path = str(sample_image_path)

    
# file_input_element = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//*[@data-testid='add-photos-input']"))
# )

# driver.execute_script("arguments[0].style.visibility = 'visible';", file_input_element)

# file_input_element.send_keys(sample_image_path)

# time.sleep(random.randint(2, 6))
# title_input_field = driver.find_element(By.XPATH, "//*[@id='title']")
# time.sleep(random.randint(2, 6))
# title_input_field.send_keys("sample title")

# time.sleep(random.randint(2, 6))
# desc_input_field = driver.find_element(By.XPATH, "//*[@id='description']")
# time.sleep(random.randint(2, 6))
# desc_input_field.send_keys("sample description")

# time.sleep(random.randint(2, 6))
# category_selector = driver.find_element(By.XPATH, "//*[@data-testid='catalog-select-dropdown-input']")
# time.sleep(random.randint(2, 6))
# category_selector.click()

# time.sleep(random.randint(2, 6))

# driver.find_element(By.XPATH, "//*[@id='catalog-5']").click()
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='catalog-2050']").click()
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='catalog-257']").click()
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='catalog-1819']").click()


# #brand selector
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@data-testid='brand-select-dropdown-input']").send_keys('levi')
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@data-testid='brand-select-dropdown-input']").click()
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='brand-10']").click()
# time.sleep(random.randint(2, 6))

# #size selector
# driver.find_element(By.XPATH, "//*[@id='size_id']").click()
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='size-1643']").click()
# time.sleep(random.randint(2, 6))

# #condition selector
# driver.find_element(By.XPATH, "//*[@id='status_id']").click()
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='status-2']").click()

# #color selector
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='color']").click()
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='suggested-color-9']").click()
# time.sleep(random.randint(2, 6))
# driver.find_element(By.TAG_NAME, 'body').click()
# time.sleep(random.randint(2, 6))



# #material selector
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='material']").click()
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='material-44']").click()
# time.sleep(random.randint(2, 6))
# driver.find_element(By.TAG_NAME, 'body').click()

# #price selector
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='price']").send_keys("100")
# time.sleep(random.randint(2, 6))
# #package size selector
# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@id='package-size-2']").click()
# time.sleep(random.randint(2, 6))

# time.sleep(random.randint(2, 6))
# driver.find_element(By.XPATH, "//*[@data-testid='upload-form-save-draft-button']").click()
# time.sleep(random.randint(2, 6))
