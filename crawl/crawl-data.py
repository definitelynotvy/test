import requests
import pandas as pd
import time
import random
from tqdm import tqdm

cookies = {
    'SPC_F':'6g4tsyNnAOVZrdkEothirX2vqOAKYKvG',
    'REC_T_ID':'1b90a284-60d7-11ee-9fac-347379167e6a',
    '_fbp':'fb.1.1696218749922.845714687',
    '_hjSessionUser_868286':'eyJpZCI6IjM4MDc4Mzk3LTkyYjktNWI5OC04ZTU5LTA5MTkwNDIzMjA2OCIsImNyZWF0ZWQiOjE2OTYyMTg3NTE3ODQsImV4aXN0aW5nIjp0cnVlfQ==',
    'SPC_CLIENTID':'Nmc0dHN5Tm5BT1Zakkvipnlfiezqpjbc',
    '_fbc':'fb.1.1696492052115.IwAR3s_t5R4-Eo_PkMsWA23tmIQDeOW5bBwvuO_HOdubaAe8_SnfMHKpCGk5I',
    'SPC_U':'-',
    'SPC_EC':'-',
    'SPC_R_T_ID':'aMpQVEaogeEgzC2REyIqgNf7HtAfXTZnpg/Na8ETLYtdN+zfyJVZmwkscsgLiaLubPk4wOZz2hiD/7WnGGPITLiSYjJQa7mrT1bjyaiL7dug9IU8hMEZeGmzlji2TQAnAABmEplJXni1v0TTuEElpSAcsxbTVdqiPg0HRgG1tzg=',
    'SPC_R_T_IV':'cDhScmF4ZHdmUTJEV3Nreg==',
    'SPC_T_ID':'aMpQVEaogeEgzC2REyIqgNf7HtAfXTZnpg/Na8ETLYtdN+zfyJVZmwkscsgLiaLubPk4wOZz2hiD/7WnGGPITLiSYjJQa7mrT1bjyaiL7dug9IU8hMEZeGmzlji2TQAnAABmEplJXni1v0TTuEElpSAcsxbTVdqiPg0HRgG1tzg=',
    'SPC_T_IV':'cDhScmF4ZHdmUTJEV3Nreg==',
    '_ga_M32T05RVZT':'GS1.1.1702584482.8.0.1702584482.60.0.0',
    '_gcl_au':'1.1.132621638.1704285163',
    'SPC_SEC_SI':'v1-Q0doV2lrOFBvRXR0c0tWUzqSIPnPlp6/s6X1lEQ6DmKult9Xnpyqiml+aAZ4WFrGQffJjLIlh/Q4Pfhzck2AF+XKvuVVoMsC17uQmkH/ukE=',
    'SPC_SI':'QQKdZQAAAAA4U21UOWc2cUgzIwAAAAAAUVg4ZjE0Y28=',
    '__LOCALE__null':'VN',
    'csrftoken':'HjkIff4F9AQvoVi8PQtF5REcH6U2DCWX',
    '_sapid':'4ca77247a7f4e72281a35b07b63eded22d2b34d5ddb91a83eab792c7',
    '_ga_4GPP1ZXG63':'GS1.1.1704943368.5.0.1704943368.0.0.0',
    '_QPWSDCXHZQA':'785dab59-3459-49bd-e656-dff710e22f59',
    'REC7iLP4Q':'81046d04-828d-428f-b5bf-41fd10567732',
    'shopee_webUnique_ccd':'8qu2xejEBqwAS28CkMddQA%3D%3D%7C6jucaHmWIlDbdL77vaMDskUuw4sN2oC6efijlAdrZZISf3l0wmtt5zPIFmFbyEIKP%2BfCr%2BojiZWQPQ%3D%3D%7CEbX67z8zoaWMskfm%7C08%7C3',
    'ds':'11970091b5c5d10f73297635039af2e2',
    'AMP_TOKEN':'%24NOT_FOUND',
    '_ga':'GA1.2.1754520024.1696218751',
    '_gid':'GA1.2.1338439444.1704943371',
    '_dc_gtm_UA-61914164-6':'1'

}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Accept': 'application/json',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://shopee.vn/G%C4%83ng-Tay-%C4%91i-ph%C6%B0%E1%BB%A3t-511-Ng%C3%B3n-C%E1%BB%A5t-(Lo%E1%BA%A1i-X%E1%BB%8Bn)-T%E1%BA%ADp-Gym-L%C3%A1i-xe-%C4%90i-ph%C6%B0%E1%BB%A3t-i.163364638.9746994645?sp_atk=2fd4383f-0ce1-4acd-9f96-0c57fad2eb3c&xptdk=2fd4383f-0ce1-4acd-9f96-0c57fad2eb3c',
    'X-Csrftoken': 'HjkIff4F9AQvoVi8PQtF5REcH6U2DCWX',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = {
    'exclude_filter': '1',
    'filter': '0',
   ' filter_size': '0',
    'flag': '1',
    'fold_filter': '0',
    'itemid': '9746994645',
    'limit': '6',
    'offset': '0',
    'relevant_reviews': 'false',
    'request_source': '2',
    'shopid': '163364638',
    'tag_filter': '',
    'type': '0',
    'variation_filters': ''

}

def comment_parser(file_json, star):
    d = dict()
    d['itemid'] = file_json.get('ratings')[star].get('itemid')
    d['name'] = file_json.get('ratings')[star].get('product_items')[0].get('name')
    d['shopid']  = file_json.get('ratings')[star].get('shopid')
    d['userid'] = file_json.get('ratings')[star].get('userid')
    d['rating_star'] = file_json.get('ratings')[star].get('rating_star')
    d['comment'] = file_json.get('ratings')[star].get('comment')

    return d

BASE_URL = 'https://shopee.vn/api/v2/item/get_ratings'

def crawl_comments(item_id, shop_id):
    result = []
    lst_offset = [0, 6, 12]

    response = make_request(item_id, shop_id)

    if response and response.status_code == 200:
        json_data = response.json().get('data')
        for i in range(0,6):
            result.append(comment_parser(json_data, i))
    time.sleep(1)

    return result

def make_request(item_id, shop_id):
    params['itemid'] = item_id
    params['shopid'] = shop_id
    params['offset'] = 0
    response = requests.get(BASE_URL, headers=headers, params=params, cookies=cookies)
    response.raise_for_status()
    return response

# # Main script
# df_id = pd.read_csv('shopee_product_id.csv')
# p_ids = df_id.itemid.tolist()
# s_ids = df_id.shopid.tolist()
# result = []

# for pid, sid in tqdm(zip(p_ids, s_ids), total=len(p_ids), desc='Crawling comments'):
#     print(f'Crawling comments for product {pid}')
#     comments = crawl_comments(pid, sid)
#     result.extend(comments)

# df_comment = pd.DataFrame(result)
# df_comment.to_csv('shopee_comments_data.csv', index=False)
# df_comment
# 308461157.26711038214
comments = crawl_comments(26711038214, 308461157)
print(comments)