'''
CORMIK BACKEND

F37 SDK ALTRE MACCHINE
F32 SDK DECESPUGLIATORI
F30 SDK MOTOSEGHE
F36 SDK TOSASIEPI
'''

import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

url = "https://cormik.ev-portal.com/Service/ProdRegGetMachModels"

SDK_type = ["F37", "F32", "F30", "F36"]

products = pd.DataFrame()

for type in range(len(SDK_type)):
  querystring = {"machType": SDK_type[type]}
  payload = ""
  headers = {
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0",
      "Accept": "application/json, text/javascript, */*; q=0.01",
      "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding": "gzip, deflate, br",
      "X-Requested-With": "XMLHttpRequest",
      "Connection": "keep-alive",
      "Referer": "https://cormik.ev-portal.com/Service/ProdReg",
      "Cookie": "ASP.NET_SessionId=vroxq4vpbmrw2padvbamv4d5; __RequestVerificationToken=VML0Us1Ao1u9VFQ94mRHQqsHckXXDll0VH7Emrv4Y-fZwXdLgme1vx6bw14d4g-U-JEhXk5HX-nXIraRo98_9_xCpQtxKFkfcrASFThLjX41; _ga=GA1.2.246622703.1648073401; _gid=GA1.2.739061368.1648073401; _gat_gtag_UA_134955900_1=1",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin"
  }

  r = requests.request("GET", url, data=payload, headers=headers, params=querystring)
  data = r.json()
  df = pd.json_normalize(data)
  df.drop([0], inplace=True)
  df.drop(df.columns[[2]], axis=1, inplace=True)
  print(df)
  products = products.append(df)

products.to_csv('shindaiwa_codes.csv')