import requests
from bs4 import BeautifulSoup
import pandas as pd

# request URL
def get_page_content(request_url):
    # Get page content
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(request_url,headers=headers,timeout=10)
    content = html.text
    # Create BeautifulSoup object with content
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup


def analysis(soup):
    temp = soup.find('div', class_= 'tslb_b')
    # Create DataFrame
    df = pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])
    tr_list = temp.find_all('tr')
    for tr in tr_list:
        temp = {}
        td_list = tr.find_all('td')
        # first tr has no td, rest are have td
        if len(td_list) > 0:
            id, brand, car_model, type, desc, problem, datetime, status = td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            # put text into DataFrame
            temp['id'], temp['brand'], temp['car_model'], temp['type'], temp['desc'], temp['problem'],temp['datatime'], temp['status'] = id, brand, car_model, type, desc, problem, datetime, status
            df = df.append(temp, ignore_index = True)
    return df


page_num = 20
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'

result = pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])
for i in range(page_num):
    request_url = base_url + str(i+1) + '.shtml'
    soup = get_page_content(request_url)
    df = analysis(soup)
    print(request_url)
    print(df)
    result = result.append(df)

result.to_csv('result.csv', index=False, encoding='GBK')