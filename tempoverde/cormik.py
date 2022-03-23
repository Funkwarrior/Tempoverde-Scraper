'''
CORMIK BACKEND

F37 SDK ALTRE MACCHINE
F32 SDK DECESPUGLIATORI
F30 SDK MOTOSEGHE
F36 SDK TOSASIEPI
'''

import requests
import pandas as pd

url = "https://cormik.ev-portal.com/Service/ProdRegGetMachModels"

SDK_type = ["F37", "F32", "F30", "F36"]
SDK_info=[]

for type in range(len(SDK_type)):
  querystring = {"machType": SDK_type[type]}

  print(querystring)
  payload = ""
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
      "Accept": "application/json, text/javascript, */*; q=0.01",
      "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding": "gzip, deflate, br",
      "X-Requested-With": "XMLHttpRequest",
      "Connection": "keep-alive",
      "Referer": "https://cormik.ev-portal.com/Service/ProdReg",
      "Cookie": "ASP.NET_SessionId=cn0uvrsz55msxislpwynppwu; __RequestVerificationToken_L0NsaWVudE5ldw2=SKDF8gJiDAVvPdMBJNIQ1jW0VYRinOkJpo6QqHyYhjjRdThcNX9Fgf6ZxstA8m1zDPGJBrJf_6EF3DGb2CvtRsUVhfVHMmtmBKapxdsTfbM1; __RequestVerificationToken=p_iG0RIykEUTYK_DOBt-h0mmjSYL4mGCPMHTw5UEtVKD1t3ZcjeMkk2gZkO6lp7Jbqxy2IVPw9EKLbImyTpZYwSXnXtNxjhObP9n2FS4UrE1",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin"
  }

  r = requests.request("GET", url, data=payload, headers=headers, params=querystring)
  data = r.json()

  for p in data:
    print
