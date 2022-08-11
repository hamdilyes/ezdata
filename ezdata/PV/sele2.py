from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import datetime
import glob
import os


def test_virta():
    options = Options()
    options.page_load_strategy = 'normal'
    driver = webdriver.Firefox(options=options)

    driver.get("https://admin.virta.fi/login.php")

    username = driver.find_element(by=By.NAME, value="username")
    password = driver.find_element(by=By.NAME, value="passwd")
    login_button = driver.find_element(by=By.ID, value="btn")

    username.send_keys("greentechnologie")
    password.send_keys("rjF7FF5vJw6b")
    login_button.click()

    WebDriverWait(driver, timeout=30).until(lambda d:
                                            d.current_url == "https://admin.virta.fi/index.php")

    driver.get("https://admin.virta.fi/report.php")
    el = driver.find_elements(by=By.CLASS_NAME, value="radio-key")
    now = datetime.datetime.now()
    today = now.strftime("%d.%m.%Y")
    before = now - datetime.timedelta(days=30)
    before = before.strftime("%d.%m.%Y")
    daterange = str(before)+" - "+str(today)

    WebDriverWait(el[11], timeout=30).until(
        lambda d: d.find_element(by=By.XPATH, value="./.."))
    el11 = el[11].find_element(by=By.XPATH, value="./..")
    el11.click()
    WebDriverWait(driver, timeout=30).until(
        lambda d: d.find_element(by=By.NAME, value="daterange"))
    datera = driver.find_element(by=By.NAME, value="daterange")
    datera.clear()
    datera.send_keys(daterange + Keys.ENTER)
    WebDriverWait(driver, timeout=30).until(lambda d:
                                            d.find_element(
                                                by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]'))
    csv = driver.find_element(
        by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]')
    csv.click()

    # driver.get("https://admin.virta.fi/report.php")
    # el = driver.find_elements(by=By.CLASS_NAME, value="radio-key")
    # el15 = el[15].find_element(by=By.XPATH, value="./..")
    # el15.click()
    # datera = driver.find_element(by=By.NAME, value="daterange")
    # print(daterange)
    # datera.clear()
    # datera.send_keys(daterange + Keys.ENTER)
    # time.sleep(10)
    # try:
    #     WebDriverWait(driver, timeout=30).until(lambda d:
    #                                             d.find_element(
    #                                                 by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]'))
    #     csv = driver.find_element(
    #         by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]')
    # except:
    #     try:
    #         WebDriverWait(driver, timeout=30).until(lambda d:
    #                                                 d.find_element(
    #                                                     by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div/div[2]/div/table/tbody/tr/td/a'))
    #         csv = driver.find_element(
    #             by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div/div[2]/div/table/tbody/tr/td/a')
    #     except:
    #         pass
    # csv.click()

    # driver.get("https://admin.virta.fi/report.php")
    # el = driver.find_elements(by=By.CLASS_NAME, value="radio-key")
    # el17 = el[17].find_element(by=By.XPATH, value="./..")
    # el17.click()
    # datera = driver.find_element(by=By.NAME, value="daterange")
    # datera.clear()
    # datera.send_keys(daterange + Keys.ENTER)
    # time.sleep(20)
    # WebDriverWait(driver, timeout=30).until(lambda d:
    #                                         d.find_element(
    #                                             by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]'))
    # csv = driver.find_element(
    #     by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]')
    # csv.click()

    driver.close()


if __name__ == "__main__":
    test_virta()
