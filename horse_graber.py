from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getHorses():
  options = webdriver.ChromeOptions()
  options.add_argument('--headless=new')
  driver = webdriver.Chrome(options=options)
  templist2 = []
  horseMetadata = getHorseMetadata()
  i = 0
  size = len(horseMetadata)
  lastProgress = 0
  for h in horseMetadata:
    i = i+1
    progress = int(i / size * 100)
    if lastProgress != progress:
      lastProgress = progress
      print(f"{progress}%")

    href = h[2]
    horseID = h[0]
    horseName = h[1]
    country_age, owner, import_type, color_sex, sire, dam, dam_sire = getHorseDetails(driver, href)
    templist2.append([horseID, horseName, country_age, owner, import_type, color_sex, sire, dam, dam_sire, href])
  
  driver.close()
  df = pd.DataFrame(templist2, columns=["horseID", "name", "country_age", "owner", "import_type", "color_sex", 'sire', "dam", "dam_sire", "url"])
  return df


def getHorseMetadata():
  options = webdriver.ChromeOptions()
  options.add_argument('--headless=new')
  driver = webdriver.Chrome(options=options)

  url = 'https://racing.hkjc.com/racing/information/English/Horse/ListByLocation.aspx?Location=HK'

  driver.get(url)
  # wait until the page is loaded
  delay = 3 # seconds
  try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/table[2]')))
  except TimeoutException:
    print("Loading took too much time!")

  # get list element
  links = driver.find_elements(by=By.TAG_NAME, value="a")

  # get horse name and horse details href
  templist = []
  for link in links:
    href = link.get_attribute("href")
    horseID = href[-4:]
    text = link.text
    if "HorseId" in href:
      templist.append([horseID, text, href])

  driver.close()
  return templist
    


def getHorseDetails(driver, url):
  driver.get(url)
  delay = 3 # seconds
  try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/table[3]")))
  except TimeoutException:
    print("Loading took too much time!", url)
  
  country_age = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td[3]").text
  owner = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]").text
  import_type = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[3]/td[3]").text
  color_sex = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[3]").text
  sire = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[5]/td[3]").text
  dam = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[6]/td[3]").text
  dam_sire = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[7]/td[3]").text

  return country_age, owner, import_type, color_sex, sire, dam, dam_sire



def getHorsesHistory():
  options = webdriver.ChromeOptions()
  options.add_argument('--headless=new')
  driver = webdriver.Chrome(options=options)
  horse_history = []
  horseMetadata = getHorseMetadata()
  i = 0
  for h in horseMetadata:
    i = i+1
    href = h[2]
    horseID = h[0]
    horseName = h[1]
    print("{:.0%} - {}".format(i / len(horseMetadata), horseID))
    getHorseHistory(driver, href, horseID, horse_history)
  
  driver.close()
  df = pd.DataFrame(horse_history)
  return df

def getHorseHistory(driver, url, horseID, horse_history=[]):
  driver.get(url)

  # wait until the page is loaded
  delay = 3 # seconds
  try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/table[3]")))
  except TimeoutException:
    print("Loading took too much time!", url)

  # get list element
  table = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/table[3]")
  trs = table.find_elements(by=By.TAG_NAME, value="tr")
  for tr in trs:
    tds = tr.find_elements(by=By.TAG_NAME, value="td")
    if len(tds) > 15: 
      row_data = [horseID]
      for td in tds:
        row_data.append(td.text)
      horse_history.append(row_data)
      
# get horse list
metadata = getHorsesHistory()
metadata.to_csv("horses_history.csv", header=False, index=False)


# horse = getHorses()
# horse.to_csv("horses.csv", index=False)