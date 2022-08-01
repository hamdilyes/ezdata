from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


def test_google():
    driver = webdriver.Firefox()

    driver.get("https://google.com")

    # title = driver.title
    # assert title == "Google"

    search_box = driver.find_element(by=By.NAME, value="q")

    search_box.send_keys("Guadeloupe" + Keys.ENTER)

    # search_button = driver.find_element(by=By.CLASS_NAME, value="gNO89b")
    # search_button.click()

    # driver.close()


if __name__ == "__main__":
    test_google()
