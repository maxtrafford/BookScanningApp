from selenium import webdriver
from selenium.webdriver import Chrome , ChromeOptions
from Book_urls import WEB
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

def WEB_price(k,row):
    
    opts= ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('./chromedriver.exe',options = opts)
    driver.get(WEB["URL"]) # Opens chrome
    #print(k)
    time.sleep(0.15)
    driver.find_element_by_xpath("/html/body/main/section[3]/div/div[1]/div/div/form/div[1]/input").send_keys('email')
    driver.find_element_by_xpath("/html/body/main/section[3]/div/div[1]/div/div/form/div[2]/input").send_keys('password')
    driver.find_element_by_xpath("/html/body/main/section[3]/div/div[1]/div/div/form/div[3]/input").click()
    driver.find_element_by_xpath("/html/body/header/div/div/div/div/a[1]/img[1]").click()
    time.sleep(1.5)

    try : driver.find_element_by_xpath("/html/body/main/section[1]/div/div/div[1]/div[3]/div/form/div[1]/input").click()
    except: print('Could not click enter barcode WEB')
    else:
        time.sleep(0.2)
        try : driver.find_element_by_xpath("/html/body/main/section[1]/div/div/div[1]/div[3]/div/form/div[1]/input").send_keys(k)
        except: print('could not send keys to barcode WEB')
        else:
            time.sleep(0.2)
            driver.find_element_by_xpath("/html/body/main/section[1]/div/div/div[1]/div[3]/div/form/div[1]/button").click()
            time.sleep(2.5)
            range= "Sheet9!D"+str(row)
            try: temp = driver.find_element_by_xpath("/html/body/main/section[2]/div/div[3]/div[2]/div/div/div/div[2]/span/span[1]")
            except: # try again or error, if try again return value 0 
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, 500)") 
                try: driver.find_element_by_xpath("/html/body/div[5]/div/div/div[3]/button").click()
                except : 
                    print('An error has occured WEB')
                    b=[[0]]
                    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=range, valueInputOption='USER_ENTERED', body={'values':b}).execute()
                    #print(request)
                    driver.close()
                    driver.quit()
                else : 
                    b=[[0]]
                    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=range, valueInputOption='USER_ENTERED', body={'values':b}).execute()
                    #print(request)
                    driver.close()
                    driver.quit()
            else:

                temp_price=str(temp.get_attribute('innerHTML'))
                b = re.search('[0-9.]+', temp_price).group()
                #print(b)
                b=[[b]]
                #print(b)
                driver.find_element_by_xpath("/html/body/main/section[2]/div/div[3]/div[1]/a/i").click()
                driver.find_element_by_xpath("/html/body/main/div[6]/div/div/div[3]/button[1]").click()
                time.sleep(0.15)
                driver.close()
                driver.quit()
                request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=range, valueInputOption='USER_ENTERED', body={'values':b}).execute()
                #print(request)      


if __name__ == "__main__":

    k = '9781844166831'
    row = 2
    WEB_price(k,row)