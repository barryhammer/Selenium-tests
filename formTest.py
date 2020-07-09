from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

#Create new session
driver = webdriver.Chrome(executable_path=r"C:/Users/Family Hammer/Downloads/chromedriver.exe")
sendXPath = "//*[@id='contact_form']/fieldset/div[13]/div/button"

#driver.maximize_window()

driver.get("https://www.seleniumeasy.com/test/input-form-demo.html")
element = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, sendXPath)))

fName = driver.find_element_by_name("first_name")
lName = driver.find_element_by_name("last_name")

state = driver.find_element_by_name("state")
select_state = Select(state)
#zip = driver.find_element_by_name("zip")
#webName = driver.find_element_by_name("website")
#hosting = driver.find_elements_by_class_name("col-md-4")
#projDesc = driver.find_element_by_name("comment")
sendBtn = driver.find_element_by_xpath(sendXPath)

fName.send_keys("Barry")
lName.send_keys("Hammer")
select_state.select_by_visible_text('New York')

sendBtn.click()

print("All good!")

driver.quit()