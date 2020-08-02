#-------------------------------------------------------------------------------
# Name:        Shufersal search
# Purpose:
#
# Author:      Barry Hammer
#
# Created:     02/08/2020
# Copyright:   (c) Barry Hammer 2020
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Links I used for reference:
# https://stackoverflow.com/questions/8286352/how-to-save-an-image-locally-using-python-whose-url-address-i-already-know
# https://stackoverflow.com/questions/35176639/compare-images-python-pil
# https://www.youtube.com/watch?v=fUfvBnREBFc
# https://www.seleniumeasy.com/python/example-code-using-selenium-webdriver-python
#-------------------------------------------------------------------------------
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from PIL import Image
from PIL import ImageChops
import urllib.request
import ctypes
import PySimpleGUI as sg

###################################
# Start session
###################################
sg.ChangeLookAndFeel('Tan')
layout = [
                 [sg.Text("Please enter search criteria", font = 'Helvetica')],
                 [sg.Text('E-mail: ', font = 'Helvetica', size=(15, 1)), sg.InputText()],
                 [sg.Text('Password:', font = "Helvetica", size=(15, 1)), sg.InputText('', password_char='*')],
                 [sg.Text('Hebrew name: ', font = 'Helvetica', size=(15, 1)), sg.InputText()],
                 [sg.Button('Submit Data')]
        ]

window = sg.Window('Enter search criteria', layout)

event, values = window.read()
window.close()

email = values[0]
password_text = values[1]
user_name = values[2]

#options = Options()
#options.add_argument("--headless"), chrome_options=options,
driver = webdriver.Chrome(executable_path=r"C:/Users/Family Hammer/Downloads/chromedriver.exe")

###################################
# 1. Navigate to site, verify logo
###################################

driver.get("https://www.shufersal.co.il/online/he/")

assert u"שופרסל" in driver.title

urllib.request.urlretrieve("https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/cmscontent/hde/h73/9038553808926", r"C:\Users\Family Hammer\Downloads\Compare\local.png")
img1 = Image.open(r"C:\Users\Family Hammer\Downloads\Compare\local.png")
img2 = Image.open(r"C:\Users\Family Hammer\Downloads\Compare\shufersal.png")

diff = ImageChops.difference(img1, img2)

if diff.getbbox():
    print("images are different")
    driver.quit()

###################################
# 2. Log in to site, verify name
###################################

login_link = driver.find_element_by_xpath('//*[@id="loginDropdownContainer"]/button')
login_link.click()

name = driver.find_element_by_xpath('//*[@id="j_username"]')
password = driver.find_element_by_xpath('//*[@id="j_password"]')

name.clear()
password.clear()
name.send_keys(email)
enter_site = password.send_keys(password_text + Keys.ENTER)

try:
    # wait 5 seconds before looking for element
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="contactInner"]/div/div[1]/div[1]/a/strong'))
    )
except:
    # else quit
    print("Could not find element")
    driver.quit()

welcome_text = driver.find_element_by_xpath('//*[@id="contactInner"]/div/div[1]/div[1]/a/strong')
assert (user_name) in welcome_text.text

###################################
# 3. Search for milk products
###################################

chalav = u"חלב"
search_box = driver.find_element_by_xpath('//*[@id="js-site-search-input"]')
search_box.send_keys(chalav + Keys.ENTER)

try:
    # wait 5 seconds before looking for element
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']/div[2]/div[2]/h1"))
    )
except:
    # else quit
    print("Could not find element")
    driver.quit()

search_criteria = driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div[2]/h1')
assert chalav in search_criteria.text

###################################
# 4. Use slider for lowest price
###################################
'''

NOTE: Currently, I keep getting an error 'move target out of bounds' when attempting to move the slider on the page.
I got the X location of the slider by using this script:
    en2 =  driver.find_element_by_xpath('//*[@id="product-facet"]/ul[2]/li[5]/div[2]')
    location = en.location
    size = en.size
    print(location)
    print(size)
Using this on a test slider at https://www.seleniumeasy.com/test/drag-drop-range-sliders-demo.html, I was able to get the result I was looking for.
Because this is taking too long to figure out for now, I am leaving this as a comment.
I am instead searching for the lowest price by URL, and proceeding from there.

slider =  driver.find_element_by_xpath('//*[@id="product-facet"]/ul[2]/li[5]/div[2]')
move = ActionChains(driver)
move.click_and_hold(en).move_by_offset(-1416, 0).release().perform()

'''
driver.get('https://www.shufersal.co.il/online/he/search?q=%D7%97%D7%9C%D7%91:relevance:priceValue_min:2:priceValue_max:2')

###################################
# 5. Add to cart, find price
###################################

item = driver.find_element_by_xpath('//*[@id="mainProductGrid"]/li[1]/div[1]/div[4]/button[1]').click #Add first item to cart
price = driver.find_element_by_xpath('//*[@id="cartContainer"]/div/div/footer/div[2]/div/div/div[1]/span').text
t = price.split()
total = t[3] #Get third element, which is the actual price, leaving text behind

ctypes.windll.user32.MessageBoxW(0, "The total amount with shipping is NIS: {}.".format(total), "Result message box", 1)

###################################
# Quit session
###################################
driver.quit()