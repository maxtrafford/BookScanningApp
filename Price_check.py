from Musicmagpie import MUS_price
from Sellitback import SEL_price
from Webuybooks import WEB_price
from Zapper import ZAP_price
from Ziffit import ZIF_price
import threading



def price(input,row):

    websites =[MUS_price,SEL_price,WEB_price,ZIF_price,ZAP_price]
    websites =[]
    for x in websites:
        th=threading.Thread(group=None,target=x,args=(input,row))
        th.start()
        


    

if __name__ == "__main__":
    input='9780061456398'
    row=2
    price(input,row)