from selenium import webdriver
from selenium.webdriver import Chrome , ChromeOptions
from Book_urls import ZIF
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


def ZIF_price(k,row):
    
    opts= ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('./chromedriver.exe',options = opts)
    driver.get(ZIF["URL"]) # Opens chrome
    #print(k)

    time.sleep(2)
    try : driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/div[3]/div/div[2]/div/form/div[2]/input").click()
    except: print('Could not click enter barcode ZIF')
    else:
        try : driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/div[3]/div/div[2]/div/form/div[2]/input").send_keys(k)
        except: print('could not send keys to barcode ZIF')
        else:
            range= "Sheet9!F"+str(row)
            driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/div[3]/div/div[2]/div/form/div[3]/button").click()
            time.sleep(2)
            
            try: temp = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/div/div/div/div/div[3]/div[1]/label")
            except:
                time.sleep(2)
                try: driver.find_element_by_xpath("")
                except : print('An error has occured5')
                else: 
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
                driver.close()
                driver.quit()
                request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=range, valueInputOption='USER_ENTERED', body={'values':b}).execute()
                #print(request)  

if __name__ == "__main__":

    k = '9780099429159'
    row = 2
    ZIF_price(k,row)