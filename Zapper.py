from selenium import webdriver
from selenium.webdriver import Chrome , ChromeOptions
from Book_urls import ZAP
import time
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account



SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SAMPLE_SPREADSHEET_ID = 'Spreadsheet ID'
service = build('sheets', 'v4', credentials=creds)
# Call the Sheets API
sheet = service.spreadsheets()

def ZAP_price(k,row):
    
    opts= ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('./chromedriver.exe',options = opts)
    driver.get(ZAP["URL"]) # Opens chrome
    #print(k)

    time.sleep(0.15)
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[1]/form/div/div[1]/input").send_keys("email")
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[1]/form/div/div[2]/input").send_keys("password")
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[1]/form/div/div[3]/button").click()
    driver.find_element_by_xpath("/html/body/div[1]/div/section[1]/div/div/div[3]/div/div/div/div/div/a/span/span").click() # Clicks sell my stuff
    driver.find_element_by_xpath("/html/body/div[2]/div/div/section[3]/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/section/div/div/div[1]/div/div/div[3]/div[2]/div/form/div[2]/div[1]/div[2]/div[2]").click()
    time.sleep(1)
    try : driver.find_element_by_xpath("/html/body/div[2]/div/div/section[3]/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/section/div/div/div[1]/div/div/div[3]/div[2]/div/form/div[1]/div[1]/input").click()
    except: print('Could not click enter barcode ZAP') # Click barcode 
    else:
        time.sleep(1)
        try : driver.find_element_by_xpath("/html/body/div[2]/div/div/section[3]/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/section/div/div/div[1]/div/div/div[3]/div[2]/div/form/div[1]/div[1]/input").send_keys(k)
        except: print('could not send keys to barcode ZAP') # send keys to barcode 
        else:
            time.sleep(1)
            range= "Sheet9!E"+str(row)
            driver.find_element_by_xpath("/html/body/div[2]/div/div/section[3]/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/section/div/div/div[1]/div/div/div[3]/div[2]/div/form/div[1]/div[2]/button").click()
            time.sleep(1)
            
            try: temp = driver.find_element_by_xpath("/html/body/div[2]/div/div/section[3]/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/section/div/div/div[2]/div/div/div[5]/div/div/p")
            except:
#                time.sleep(2)
#                try: driver.find_element_by_xpath("")
#                except : print('An error has occured4')
#                else: 
                b=[[0]]
                request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=range, valueInputOption='USER_ENTERED', body={'values':b}).execute()
                #print(request)
                driver.close()
                driver.quit()
            else:
                temp_price=str(temp.get_attribute('innerHTML'))
                b = re.search('[0-9.]+', temp_price).group()
                print(b)
                b=[[b]]
                #print(b)
                time.sleep(0.15)
                driver.find_element_by_xpath("/html/body/div[2]/div/div/section[3]/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/section/div/div/div[2]/div/div/div[3]/div/div/div/span/span").click()
                time.sleep(0.5)
                driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div/div/section[2]/div/div/div/div/div/div[2]/section/div/div/div[3]/div/div/div[1]/div").click()
                time.sleep(0.3)
                # time.sleep(20)
                driver.close()
                driver.quit()
                request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=range, valueInputOption='USER_ENTERED', body={'values':b}).execute()
                #print(request)  

if __name__ == "__main__":

    k = '9781743363508'
    row = 2
    ZAP_price(k,row)