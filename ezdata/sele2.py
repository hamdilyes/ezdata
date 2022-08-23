from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import datetime
import glob
import os
import time


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

    # 3 rapports depuis l'onglet Rapports
    driver.get("https://admin.virta.fi/report.php")
    el = driver.find_elements(by=By.CLASS_NAME, value="radio-key")
    now = datetime.datetime.now()
    today = now.strftime("%d.%m.%Y")
    today_err = now.strftime("%m.%d.%Y")
    before_ = now - datetime.timedelta(days=30)
    before = before_.strftime("%d.%m.%Y")
    before_err = before_.strftime("%m.%d.%Y")
    before_week = now - datetime.timedelta(days=7)
    before_week = before_week.strftime("%d.%m.%Y")
    daterange = str(before)+" - "+str(today)
    daterange_week = str(before_week)+" - "+str(today)
    daterange_err = str(before_err)+" - "+str(today_err)

    WebDriverWait(el[11], timeout=30).until(
        lambda d: d.find_element(by=By.XPATH, value="./.."))
    el11 = el[11].find_element(by=By.XPATH, value="./..")
    el11.click()
    WebDriverWait(driver, timeout=30).until(
        lambda d: d.find_element(by=By.NAME, value="daterange"))
    datera = driver.find_element(by=By.NAME, value="daterange")
    datera.clear()
    datera.send_keys(daterange)
    datera.send_keys(Keys.ENTER)
    time.sleep(10)
    WebDriverWait(driver, timeout=30).until(lambda d:
                                            d.find_element(
                                                by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]'))
    csv = driver.find_element(
        by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]')
    csv.click()

    driver.get("https://admin.virta.fi/report.php")
    el = driver.find_elements(by=By.CLASS_NAME, value="radio-key")
    el15 = el[15].find_element(by=By.XPATH, value="./..")
    el15.click()
    datera = driver.find_element(by=By.NAME, value="daterange")
    datera.clear()
    datera.send_keys(daterange_week)
    datera.send_keys(Keys.ENTER)
    time.sleep(10)
    WebDriverWait(driver, timeout=30).until(lambda d:
                                            d.find_element(
                                                by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]'))
    csv = driver.find_element(
        by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]')
    csv.click()

    driver.get("https://admin.virta.fi/report.php")
    el = driver.find_elements(by=By.CLASS_NAME, value="radio-key")
    el17 = el[17].find_element(by=By.XPATH, value="./..")
    el17.click()
    WebDriverWait(driver, timeout=30).until(
        lambda d: d.find_element(by=By.NAME, value="daterange"))
    datera = driver.find_element(by=By.NAME, value="daterange")
    datera.clear()
    datera.send_keys(daterange)
    datera.send_keys(Keys.ENTER)
    time.sleep(10)
    WebDriverWait(driver, timeout=30).until(lambda d:
                                            d.find_element(
                                                by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]'))
    csv = driver.find_element(
        by=By.XPATH, value='/html/body/div[4]/div[1]/div/div/div[2]/div/div[4]/div/div/div[1]/button[1]')
    csv.click()

    # 1 rapport avec les erreurs depuis Aperçu -> Détails
    driver.get("https://admin.virta.fi/maintenance.php?component=details_table")
    WebDriverWait(driver, timeout=30).until(
        lambda d: d.find_element(by=By.ID, value="daterange"))
    datera = driver.find_element(by=By.ID, value="daterange")
    datera.clear()
    datera.send_keys(daterange_err)
    datera.send_keys(Keys.ENTER)
    time.sleep(10)
    WebDriverWait(driver, timeout=30).until(lambda d:
                                            d.find_element(
                                                by=By.ID, value='errorMessagesCSV'))
    csv = driver.find_element(
        by=By.ID, value='errorMessagesCSV')
    csv.click()
    time.sleep(10)

    driver.close()


if __name__ == "__main__":
    test_virta()
