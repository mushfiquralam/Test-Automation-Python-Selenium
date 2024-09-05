from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def automate_toy_search(chromedriver_path, website_url="https://www.walltouchbd.com/customer/auth/login", username="1851742939", password="zxc1ZXC!", query="toys"):
    service = Service(chromedriver_path)

    #Chrome options configurations
    chrome_options=Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(website_url)
    driver.maximize_window()

    # login using username and password
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'user_id'))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'si-password'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-id"]/button'))).click()

    driver.refresh() #reloads the page

    assert driver.current_url == 'https://www.walltouchbd.com/', f"Failed. Expected URL 'https://www.walltouchbd.com/', but got '{driver.current_url}'"
    print("Login successful")

    # Send keys to the search and search for it
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/header/div[2]/div[1]/div/div[1]/form/input[1]'))).send_keys(query)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/header/div[2]/div[1]/div/div[1]/form/button'))).click()

    assert driver.current_url == 'https://www.walltouchbd.com/products?name=toys&data_from=search&page=1', f"Failed. Expected URL 'https://www.walltouchbd.com/products?name=toys&data_from=search&page=1', but got '{driver.current_url}'"
    print("Correct search results")

    link_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ajax-products"]/div[1]/div/div/div[1]/div[1]/a')))
    link_href = link_element.get_attribute('href')
    print(link_href)
    # Click on the first item
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ajax-products"]/div[1]/div/div/div[1]/div[2]'))).click()

    assert link_href in driver.current_url, "Failed to access the first item!"
    print("Accessed first item successfully.")

    driver.quit()
    
def check_path(path):
    substring = "chromedriver.exe"

    if substring in path:
        return True
    else:
        return False

# Read path from file
def get_path_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            path = file.readline().strip()
            return path
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    file_path = "chromedriver_path.txt"
    
    while True:
        path = get_path_from_file(file_path)
        if path and check_path(path):
            break
        print("The path does not contain 'chromedriver.exe'. Please check the file and try again.")

    automate_toy_search(path)

