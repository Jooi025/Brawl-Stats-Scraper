from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import json

chrome_binary_path = "chrome-win64\chrome.exe"
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.binary_location = chrome_binary_path

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get('https://pixelcrux.com/Brawl_Stars/Brawlers/#')

# click the "back to all brawlers" button
def return_main_menu():
    driver.find_element(By.XPATH,"//a[normalize-space()='Back to All Brawlers']").click()

# wait for the element to load
def wait_loading(condition:tuple):
    timeout = 30
    try:
        elementPresent = EC.element_to_be_clickable(condition)
        WebDriverWait(driver, timeout).until(elementPresent)
        return True
    except TimeoutException:
        print("Timed out")
        return False

count = 1
# dictionary to be save to json
brawlersStats = {}
sleep(10)
while True:
    # wait for main menu to load
    if not(wait_loading((By.XPATH, f"(//div[@class='brawler-portrait'])[{count}]"))):
        break
    
    try:
        clickable = driver.find_element(By.XPATH, f"(//div[@class='brawler-portrait'])[{count}]")
    except NoSuchElementException:
        break
    
    # click on brawler
    clickable.click()

    # wait for brawler stats page to load
    if not(wait_loading((By.CSS_SELECTOR,"div[id='brawler-stats-anchor'] div[class='module-header'] h2"))):
        break

    # stats of the current brawler
    brawlerStat = {}
    # get the current brawler name
    brawlerName = driver.find_element(By.CSS_SELECTOR,"div[id='brawler-stats-anchor'] div[class='module-header'] h2").text
    
    title = ["Base"] + [element.text for element in driver.find_elements(By.CLASS_NAME,"theme-color-1e") if element.text]
    allStats = [element.text for element in driver.find_elements(By.CLASS_NAME,"brawler-stat-list") if element.text]
    
    if not(len(title) == len(allStats)):
        print("Note: The title and stats array not equal")

    for i in range(len(allStats)):
        tempDict = {}
        stats = allStats[i].split("\n")
        for j in range(0,len(stats),2):
            tempDict[stats[j]] = stats[j+1]
        brawlerStat[title[i]] = tempDict

    print(brawlerStat)
    brawlersStats[brawlerName] = brawlerStat
    return_main_menu()
    count += 1

# write to json
with open("raw_stats.json", "w") as f:
    jsonObject = json.dumps(brawlersStats, indent=4)
    f.write(jsonObject)