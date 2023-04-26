from requests import get
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime

df = pd.read_csv('wallets.csv')
mydict=[]

for index in range(len(df)):
    index_dict={}
    transactions=[]
    if type(df['Wallet Address'][index])!=float and len(df['Wallet Address'][index]) == 42:
        API_KEY = 'your_key'
        address = df['Wallet Address'][index]

        BASE_URL = "https://api.etherscan.io/api"
        ETHER_VALUE = 10**18

        def make_api_url(module, action , address, **kwargs) :
            kwargs = {"tag":"latest"}
            url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"
            for key, value in kwargs.items():
                url +=f"&{key}={value}"
            return url    
        
        def get_transactions(address):
            get_transactions_url = make_api_url("account" , "txlist" , address, startblock=0 , endblock=99999999, page=1, offset=10000, sort="asc")
            response = get(get_transactions_url)
            data = response.json()["result"]
            
            get_internal_tx_url = make_api_url("account","txlistinternal", address, starblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
            response2  = get(get_internal_tx_url)
            data2 = response2.json()["result"]
            
            get_erc20_tx_url = make_api_url("account","tokentx", address, tag='latest')
            responseERC20  = get(get_erc20_tx_url)
            dataERC20 = responseERC20.json()["result"]

            get_erc721_tx_url = make_api_url("account","tokennfttx", address, tag='latest')
            responseERC721 = get(get_erc721_tx_url)
            dataERC721 = responseERC721.json()["result"]

            get_erc1155_tx_url = make_api_url("account","token1155tx", address, tag='latest')
            responseERC1155 = get(get_erc1155_tx_url)
            dataERC1155= responseERC1155.json()["result"]

            data.extend(data2)
            data.sort(key=lambda x: int(x['timeStamp']))

            data.extend(dataERC20)
            data.sort(key=lambda x: int(x['timeStamp']))

            data.extend(dataERC721)
            data.sort(key=lambda x: int(x['timeStamp']))

            data.extend(dataERC1155)
            data.sort(key=lambda x: int(x['timeStamp']))

        
            for tx in data:
                tra={}
                to = tx["to"]
                from_adr = tx["from"]
                try:
                    value = int(tx["value"])/ETHER_VALUE
                except:
                    value = 1
                if "gasPrice" in tx:
                    gas = int(tx["gasUsed"]) * int(tx["gasPrice"])/ETHER_VALUE
                else:
                    gas = int(tx["gasUsed"]) /ETHER_VALUE   
                time = datetime.fromtimestamp(int(tx['timeStamp']))
                tra = {
                   "To":to,
                   "From":from_adr,
                   "Value":value,
                   "Gas":gas,
                   "Time":time
                }
                
                transactions.append(tra)
            return transactions   

        a=get_transactions(address)
        index_dict = {
            'Wallet Address':df['Wallet Address'][index],
            'Transactions':a,
  
            }

        mydict.append(index_dict)

        dfnew = pd.DataFrame(mydict)    

        dfnew.to_csv("save.csv",index=False)