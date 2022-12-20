import requests
import time
from pprint import pprint
import json
from tqdm import tqdm


class Yandex:
    base_url = 'https://cloud-api.yandex.net:443'
    jsons = {}
    json_list = []
    vk_url = 'https://api.vk.com/method/photos.get'
    url_vk_list = []
    likes = []

    def __init__(self, yandex_token, token, id):
        self.yandex_token = yandex_token
        self.token = token
        self.id = id

    def get_url_list(self):
        params = {'owner_id': self.id,
                 'access_token': token,
                 'v': '5.131',
                 'album_id': 'profile',
                 'extended': '1',
                 'count': 5}

        response = requests.get(self.vk_url, params=params).json()['response']['items']
        for res in response:
            like = res['likes']['count']
            url = res['sizes'][-1]['url']
            type = res['sizes'][-1]['type']
            date = res['date']
            if like in self.likes:
                like = str(like) + '_date_' + str(date)
                kort = (url, like)
                self.url_vk_list.append(kort)
                self.jsons['file_name'] = f'{like}.jpg'
                self.jsons['size'] = type
                self.json_list.append(dict.copy(self.jsons))
            else:
                kort = (url, like)
                self.url_vk_list.append(kort)
                self.jsons['file_name'] = f'{like}.jpg'
                self.jsons['size'] = type
                self.json_list.append(dict.copy(self.jsons))  
            self.likes.append(like)

        with open('inf.json', 'w', encoding= 'utf-8') as document:        
            json.dump(self.json_list, document, indent=4)    

        return self.url_vk_list
        
    def upload_from_internet(self):
        headers = {'Authorization': f'OAuth {yandex_token}'}
        upload_from_internet_url = self.base_url + '/v1/disk/resources/upload'
        self.create_path(self.id)

        for uri, name in tqdm(self.get_url_list()):
            time.sleep(0)
            params = {'url': uri, 'path': f'/{self.id}/{name}.jpg'}
            requests.post(upload_from_internet_url, params=params, headers=headers)

    def create_path(self,id):
        url_create_file = self.base_url + '/v1/disk/resources'
        headers = {'Authorization': f'OAuth {yandex_token}'}
        params = {'path': f'/{id}'}
        requests.put(url_create_file, headers=headers, params=params)


token = 
yandex_token = 


ya = Yandex(yandex_token, token, 13083588)
ya.upload_from_internet()