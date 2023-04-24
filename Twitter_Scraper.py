
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Linkedin_Scraper import *
import os
import wget
from time import sleep
import pandas as pd
from collections import OrderedDict


def twitterLogin(firstname, lastname):
#need take input from GUI
    driver = initialisedWebScraping()
    driver.get("https://twitter.com/login")

    sleep(5)
    username = driver.find_element(By.XPATH, "//input[@type='text']")
    username.send_keys("user")
    next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
    next_button.click()

    sleep(2)
    password = driver.find_element(By.XPATH, "//input[@type='password']")
    password.send_keys("test")
    log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
    log_in.click()

    return (twitterSearch(driver, firstname, lastname))

#search for target
def twitterSearch(driver, firstname, lastname):
    target = firstname+ " " +lastname
    sleep(5)
    search_box = driver.find_element(By.XPATH,"//input[@data-testid='SearchBox_Search_Input']")
    search_box.send_keys(target)
    search_box.send_keys(Keys.ENTER)

    sleep(2)
    people = driver.find_element(By.XPATH,"//span[contains(text(),'People')]")
    people.click()

    return (twitterScrape(driver, firstname, lastname))

def twitterScrape(driver, firstname, lastname):
    searchName = firstname + lastname
    sleep(5)
    Names=[]
    Handles=[]
    Bios=[]
    NewBios = []
    BioChild = []
    ProfileUrls = []
    DisplayPics = []
    Professions = []
    Websites = []
    BirthYears = []
    
    Locations = []
    scrapedInfo = {}
    information = []

    userCell = driver.find_elements(By.XPATH, "//div[@data-testid='primaryColumn']/div/div[3]/div/section/div/div/div/div/div/div")
   
    newUserCell = userCell[:2]
    for i in range(len(newUserCell)):
        Name = newUserCell[i].text.splitlines()[0]
        Handle = newUserCell[i].text.splitlines()[1]
        try:
            Bio = newUserCell[i].text.splitlines()[3]
        except:
            Bio = ""
            Bio = "None"
        Names.append(Name)
        Handles.append(Handle)
        Bios.append(Bio)
        handleWithoutAt2 = "https://twitter.com/" + Handle[1:]
        ProfileUrls.append(handleWithoutAt2)
        scrapedInfo.update({Handles[i]:[Names[i]]})

    for i in range(len(ProfileUrls)):
        driver.get(ProfileUrls[i])
        sleep(3)
        try:
            for j in range(len(Bios)):
                NewBio = driver.find_element(By.XPATH, "//div[@data-testid='UserDescription']")
                BioChild = NewBio.find_elements(By.TAG_NAME, 'span')
                BioCount = len(BioChild)
                for x in range(len(BioChild)):
                    BioChild[x] = BioChild[x].text
                if BioCount >1:
                    NewBios.append(''.join(BioChild))
                    break
                else:
                    NewBios.append(Bios[i])
                    break
        except:
            NewBio = ""
            NewBio = "None"
            NewBios.append(NewBio)
        try:
            Profession = driver.find_elements(By.XPATH,"//span[@data-testid='UserProfessionalCategory']/span/span")[0].text
        except:
            Profession = ""
            Profession = "None"
        Professions.append(Profession)
        scrapedInfo[Handles[i]].append(Professions[i])
        try:
            Location = driver.find_elements(By.XPATH,"//span[@data-testid='UserLocation']/span/span")[0].text
        except:
            Location = ""
            Location = "None"
        Locations.append(Location)
        scrapedInfo[Handles[i]].append(Locations[i])
        try:
            Website = driver.find_elements(By.XPATH,"//a[@data-testid='UserUrl']/span")[0].text
        except:
            Website = ""
            Website = "None"
        Websites.append(Website)
        scrapedInfo[Handles[i]].append(Websites[i])  
        try:
            BirthYear = driver.find_elements(By.XPATH,"//span[@data-testid='UserBirthdate']")[0].text
        except:
            BirthYear = ""
            BirthYear = "None"
        BirthYears.append(BirthYear)
        scrapedInfo[Handles[i]].append(BirthYears[i]) 

        sleep(3)
        driver.get(ProfileUrls[i]+"/photo")
        sleep(3)
        ProfilePic = driver.find_elements(By.XPATH, "//html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div/div/div/img")[0].get_attribute('src')
        DisplayPics.append(ProfilePic)
        sleep(3)
        scrapedInfo[Handles[i]].append(DisplayPics[i])
        scrapedInfo[Handles[i]].append(ProfileUrls[i])

    #write to excel with respective columns
    filename = str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S").replace("-","")) + " "+ searchName + "TwitterData.xlsx"
    fullPath = os.getcwd().replace('\\','\\\\')
    df = pd.DataFrame(zip(Handles, Names, NewBios, DisplayPics, Professions, Locations, Websites, BirthYears, ProfileUrls)
                     ,columns=['Handle', 'Name', 'Biography', "Display Picture", "Profession", "Location", "Website", "Birth Year", "Profile URL"])
    df.head()
    df.to_excel(fullPath +'\\\\' + filename,index=False)
    return filename


