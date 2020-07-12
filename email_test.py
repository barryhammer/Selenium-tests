'''
Sources & websites:
    https://stackoverflow.com/questions/53917157/find-the-recaptcha-element-and-click-on-it-python-selenium/53917309#53917309
    https://putsmail.com/tests/new
    https://endtest.io/mailbox
    https://dev.to/liviufromendtest/how-to-test-emails-with-selenium-5c5m
'''

'''
NOTE: This test is failing because the email field is seen as a list, which is not allowing me to send text. Need to review further to fix.
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=r"C:/Users/Family Hammer/Downloads/chromedriver.exe")

recipient = driver.find_element_by_id("recipient-value")
subject_line = driver.find_elements_by_id("email_test_subject")
body = driver.find_elements_by_class_name("CodeMirror-lines")
send_email = driver.find_elements_by_name("commit")

driver.get("https://putsmail.com/tests/new")

recipient.send_keys("sledgeh101@gmail.com")
subject_line.send_keys("Test subject line")
body.send_keys("Test email text")
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

driver.implicitly_wait(10)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "commit"))).click()

print("All done.")

driver.close()
