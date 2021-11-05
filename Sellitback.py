

from selenium import webdriver
from selenium.webdriver import Chrome , ChromeOptions
from Book_urls import SEL
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

def SEL_price(k,row):
    
    opts= ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('./chromedriver.exe',options = opts)
    driver.get(SEL["URL"]) # Opens chrome
    #print(k)

    #Upgrade would be a wait drive
    time.sleep(2)

    try : driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div/input").click()
    except: print('Could not click enter barcode SEL')
    else:
        try : driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div/input").send_keys(k)
        except: print('could not send keys to barcode SEL')
        else:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div/div/button").click()
            time.sleep(2)
            range= "Sheet9!C"+str(row)
            try: temp = driver.find_element_by_xpath("/html/body/div/div/div[1]/div/div/div/div[3]/div/div[2]/span")
            except:
                    b=[[0]]
                    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=range, valueInputOption='USER_ENTERED', body={'values':b}).execute()
                    #print(request)
                    driver.close()
                    driver.quit()
            else :
                temp_price=str(temp.get_attribute('innerHTML'))
                try :b = re.search('[0-9.]+', temp_price).group()
                except:
                    b=[[0]]
                    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=range, valueInputOption='USER_ENTERED', body={'values':b}).execute()
                    #print(request)
                    driver.close()
                    driver.quit()
                else:
                    #print(b)
                    b=[[b]]
                    #print(b)
                    driver.close()
                    driver.quit()
                    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=range, valueInputOption='USER_ENTERED', body={'values':b}).execute()
                    #print(request)


if __name__ == "__main__":

    k = '9780061456398'
    row =2
    SEL_price(k,row)