import requests
from bs4 import BeautifulSoup
import telebot
import re
import json
import time
import pytesseract
from PIL import Image
TELEGRAM_TOKEN = "1700323195:AAHFdOVNMCvjnFyN9Dqpt-QSyHlGih8ybUg"
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "✅ اهلا بك في بوت البحث عن سوال ضمن موقع جيك 👇🏻👇🏻\n"
                          "1- قم بارسال صوره واضحه للسوال .\n"
                          "2- سوف يتم الرد عليك بروابط 80% تحتوي على سوالك ، اذا كان سوالك من ضمن روابط قم بنسخ الرابط و إرساله إلى @Chegg_1 \n"
                          " حيث ان هذا الكروب  مختص بجلب حلول الروابط على شكل ملف .\n"
                          "• اذا لم يكن سوالك موجود نصا فسوف تظهر لك اساله مشابه بطريقه الحل .\n"
                          "• اذا كنت ترغب بحل سوالك نصا عليك الاشتراك بباقه رفع اسئله خارجيه عن طريق ارسال رساله الادمن\n "
                          "@eng2028")

@bot.message_handler(content_types=['photo'])
def echo_all(message):
    bot.reply_to(message, "Wait to Send Links 🕺✌🏿")
    raw = message.photo[-1].file_id
    path = raw+'.jpg'
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    image = Image.open(path)
    t = pytesseract.image_to_string(image)
    c=re.sub('\s+', ' ', t)
    url = "https://gateway.chegg.com/se-search-bff/graphql"
    payload = json.dumps({
        "operationName": "getSearchResults",
        "variables": {
            "profile": "study-decks-intent-srp",
            "query": f"{c}",
            "page": 1,
            "experiments": "|",
            "seasonOverride": ""
        },
        "query": "query getSearchResults($profile: String, $query: String, $page: Int, $experiments: String, $seasonOverride: String) {n  search(n    profile: $profilen    query: $queryn    page: $pagen    experiments: $experimentsn    seasonOverride: $seasonOverriden  )n}n"
    })
    headers = {
        'authority': 'gateway.chegg.com',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'accept': '*/*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://www.chegg.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.chegg.com/',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'C=0; O=0; V=e5682c6278fee869f4bc792129577dd46029fe896e3123.42530419; optimizelyEndUserId=oeu1613364877041r0.3478582229951177; _pxvid=e7cd23e0-6f49-11eb-a714-0242ac120005; _ga=GA1.2.2010358793.1613364878; _rdt_uuid=1613364878624.3f9e3600-162e-4857-aaea-b4f2e5fcf364; adobeujs-optin=%7B%22aam%22%3Atrue%2C%22adcloud%22%3Atrue%2C%22aa%22%3Atrue%2C%22campaign%22%3Atrue%2C%22ecid%22%3Atrue%2C%22livefyre%22%3Atrue%2C%22target%22%3Atrue%2C%22mediaaa%22%3Atrue%7D; _ym_uid=1613364879184249252; _ym_d=1613364879; _gcl_au=1.1.38970177.1613364879; _fbp=fb.1.1613364879617.1349988882; s_ecid=MCMID%7C02419299262521729501329844910627507216; LPVID=UwZDRlMzRiNzM2YWUwOTEx; al_cell=main-1-control; __gads=ID=76c2234048de2418:T=1613364891:S=ALNI_Mbr0m7561uRpONQ0jz1wX3wWN3-hw; _scid=fb693712-3acc-4efb-ba76-9f7dc41e981a; _cs_c=1; chgmfatoken=%5B%20%22account_sharing_mfa%22%20%3D%3E%201%2C%20%22user_uuid%22%20%3D%3E%20dc95b057-4cd5-42d7-a7a0-d032f5634163%2C%20%22created_date%22%20%3D%3E%202021-04-01T14%3A05%3A02.094Z%20%5D; U=8f7f40dc435e0439ea4720520dfb04a3; gid=1; gidr=MA; _sctr=1|1617260400000; _gid=GA1.2.1435849481.1617423490; _ym_isad=2; intlPaQExitIntentModal=hide; user_geo_location=%7B%22country_iso_code%22%3A%22IQ%22%2C%22country_name%22%3A%22Iraq%22%2C%22region%22%3A%22NI%22%2C%22region_full%22%3A%22Nineveh%22%2C%22city_name%22%3A%22Mosul%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22ar-IQ%22%5D%7D%7D; AMCVS_3FE7CBC1556605A77F000101%40AdobeOrg=1; AMCV_3FE7CBC1556605A77F000101%40AdobeOrg=-408604571%7CMCIDTS%7C18721%7CMCMID%7C02419299262521729501329844910627507216%7CMCAAMLH-1618117921%7C6%7CMCAAMB-1618117921%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1617520321s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0%7CMCCIDH%7C209593919; BIBSESSID=276b4fc9-46d8-460a-9d93-c34bb7796fd7; userRole=not_logged_in; PHPSESSID=r80hre980ksj7v43bpcpk73k6i; CSessionID=fb4d511a-9289-4de3-a425-766b542368a2; exp=A184B%7CA311C%7CA803B%7CC024A%7CA560B%7CA259B%7CA294A%7CA207B; expkey=02967087967FAC83DC3A4CD4E23C4A55; _cs_cvars=%7B%221%22%3A%5B%22Page%20Name%22%2C%22Federated%20Search%22%5D%2C%223%22%3A%5B%22Page%20Type%22%2C%22search%22%5D%2C%224%22%3A%5B%22Auth%20Status%22%2C%22Logged%20Out%22%5D%7D; LPSID-51961742=XOm5r-m8Sxi5sE_2GTFoqg; _px3=ba4f8036e6e0b40a84f9c1fad047df0ede9d075b453b0d01c8d845c7d1c947af:IcM/t864t2qrg5XdOErwaph1fh2qENl8nGyC6Sk/FEbTr7Y0sZlaKf2UVwLGeI8oh0M6TN1e88F8AD6DGynbZg==:1000:15BQGNY1nBlKsqn7agAVReY+Ljs01bmlJb8zJnXqEdC/Y6rsKaqJaUlENDlfPB09KLpGKU4AaFCdB//jcdvc4B3UvKPnkgOiFFcic02jNyF4oKEM5V3jrNa4ieiabuYajKOhp//R4PlXynlUuP1gmuIDtKEWBRJwYWoUe2puGFI=; _px=IcM/t864t2qrg5XdOErwaph1fh2qENl8nGyC6Sk/FEbTr7Y0sZlaKf2UVwLGeI8oh0M6TN1e88F8AD6DGynbZg==:1000:5pZEjngSZTL9YFsP53P4il5EaxCZ60KfA3Qz+r+ihJl20Nd5nRpM1cQr8zH/5iZi/K7Ok2guwVwCKkWTQw8n+JEdNxCKOjHkIev8YaSsy21ZTumKFRVyMKo5FWFZFfgSANpOPEo1CTV79Y8DIgCg+v6zAHDs9zZ8HH3KmPJ5BqAFervslP7V82IMd5hkakzYA9RBQVGtFt0R6HzuTLNCoCPPUsgdQMEmDpUpgaRdQ1WUP1TTTWSDRQxTjUsJmqMD0hLUOBven2qPPfPzCC6srA==; OptanonConsent=isIABGlobal=false&datestamp=Sat+Apr+03+2021+22%3A20%3A35+GMT-0700+(Pacific+Daylight+Time)&version=6.10.0&hosts=&consentId=a2d8edd1-7602-4574-b839-ee8f1426bc47&interactionCount=1&landingPath=NotLandingPage&groups=snc%3A1%2Cfnc%3A1%2Cprf%3A1%2CSPD_BG%3A1%2Ctrg%3A1&AwaitingReconsent=false; _uetsid=997df7f0943311eb9334b1f5d5de9e36; _uetvid=3299c18092ab11ebbca6e38e920ff97f; _cs_id=663c1ad2-2033-aa61-f229-172a7c82ba74.1613364894.4.1617513641.1617513597.1.1647528894955.Lax.0; _cs_s=2.1; __CT_Data=gpv=7&ckp=tld&dm=chegg.com&apv_79_www33=7&cpv_79_www33=7; s_pers=%20buFirstVisit%3Dcore%252Ccs%252Cothers%7C1775226805043%3B%20gpv_v6%3Dchegg%257Cweb%257Ccore%257Cfederated%2520search%7C1617515592829%3B; s_sess=%20buVisited%3Dcore%3B%20s_ptc%3D0.01%255E%255E0.00%255E%255E0.00%255E%255E0.00%255E%255E0.40%255E%255E0.65%255E%255E7.92%255E%255E0.47%255E%255E9.04%3B%20cheggCTALink%3Dfalse%3B%20SDID%3D29D11A448BDCB5D9-2ED4C18128F59858%3B%20s_sq%3Dcheggincriovalidation%253D%252526pid%25253Dchegg%2525257Cweb%2525257Ccore%2525257Cfederated%25252520search%252526pidt%25253D1%252526oid%25253Dhttps%2525253A%2525252F%2525252Fwww.chegg.com%2525252Fsearch%2525252F%25252525E2%2525252580%252525258FTwo%2525252520water%2525252520tanks%2525252520are%2525252520connected%2525252520to%2525252520each%2525252520other%2525252520th%252526ot%25253DA%3B; SU=IfIH858aO4BqP7EGpN_Y905KrrGBCQEFIQ3TEjltJ4nwpnXC5A_Khgg409QT1IGaJDEZ7mGvSiXme4RpI-w6JPAvDlqC_mNr6ixfvPhlZe76hH4Vw4uOBJ3MttdSqiJk; exp=A184B%7CA311C%7CA803B%7CC024A%7CA560B%7CA259B%7CA294A%7CA207B%7CA110B%7CA966C%7CA270C%7CA278C%7CA935B%7CA360B%7CA448A%7CA890H; expkey=5C68A88FE58C19D51D9B72FF9D8A2423; id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJkYzk1YjA1Ny00Y2Q1LTQyZDctYTdhMC1kMDMyZjU2MzQxNjMiLCJhdWQiOiJDSEdHIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsImV4cCI6MTYzMzA1NjA1NSwiaWF0IjoxNjE3Mjg2MDU1LCJlbWFpbCI6Im1haG11dG1hbjhAZ21haWwuY29tIn0.VvYVj6nGKFDjxKqsuiiSoEtwD_UHH_i-vZTkS3pYpC1wwbqBkwDOOs9noIQmHBhObb_5gsiHWO2-uU7DKfEiWmnzCpFEw1_jDCiwv4QlTezo39OpVojcluO58-0QnOJksXwDTAw1Hm4RIuv7fn0N3aPNzdCOg72Lquw-p9Rv6ojSZoZgvzIXt9rqRAAN25w4wWxTugDgImokgZOCHY_MsFQd_v3o9svd1Oljy-zUbitG-b5keBqfsubxrq8IoA0kPuQbzerQ51RoVXOI-Uwh1p2ZPVs8toJBR_mgkvyPsgCLw7hRnFCp17XEMSMqDuuqWkGmBA7p0DEfRgyN7wgq2w'
    }

    response = requests.request("POST", url, headers=headers, data=payload).text
    rt = str(time.clock())
    mma = rt.split(".")[0]
    m = json.loads(response)
    for i in m['data']['search']['study']['responseContent']['docs']:
        nn = i['url']
        us = "https://www.chegg.com" + nn
        bot.reply_to(message, "Links 📍🌐 :\n\n"+us+"\n\n ⏱ Time : "+str(mma)+"\n\nBy Eng Mahmoud Fadhil 🛡 @eng2028\n\nGo to bot to get solution @Chegg_1 ✅✅\n\nBest Wishes")
bot.polling()
