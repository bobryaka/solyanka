import requests
import json
import random
import time
import re


def defender(id, token, api):
    try:
        temp = (re.findall(r'(?<=https://vk.com/id)\d+', id) if re.findall(r'(?<=https://vk.com/id)\d+', id) else
                re.findall(r'(?<=https://vk.com/)\S+', id))
        id = temp[0] if temp else id
        user = requests.get("https://api.vk.com/method/users.get?user_ids=%s&fields=photo_200&access_token=%s&v=%s" % (
            id, token, api)).json()['response'][0]
        if not user['is_closed']:
            return 'ok', user
        elif user['is_closed']:
            return "closed"
    except (KeyError, IndexError):
        return "deactivated"


class Contact:

    api = '5.131'

    def __init__(self, user1_id, user2_id, keys):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.service_key = keys[0]
        self.user_token = keys[1]
        self.app_token = keys[2]
        self.app_token2 = keys[3]
        self.drugi_1chela = self.friends_get(self.user1_id)
        self.drugi_2chela = self.friends_get(self.user2_id)

    def friends_get(self, user_id):
        all_fr = requests.get("https://api.vk.com/method/friends.get?user_id=%s&fields=1&access_token=%s&v=%s" % (
            user_id, self.service_key, Contact.api)).json()['response']['items']
        norm_fr = list()
        for fr in all_fr:
            try:
                fr['deactivated']
            except KeyError:
                norm_fr.append(fr['id'])
        return norm_fr

    @staticmethod
    def parts(lst, sz):
        # Делит список на части, чтобы кормить ими execute и getMutual
        return [lst[i:i + sz] for i in range(0, len(lst), sz)]

    @staticmethod
    def get_fr_of_fr(lst, token):
        big_lst = list()
        uniq_fr = set()
        # Отправляет по кускам вк, принимает назад и складывает в новый список
        for part in Contact.parts(lst, 25):
            code = 'return [' + ', '.join(
                ('API.friends.get({"v": "5.131", "count":"500", "order": "hints", "user_id":"' + str(x) + '"})') for x
                in part) + '];'
            vk_exec = requests.get("https://api.vk.com/method/execute?code=%s&access_token=%s&v=%s" % (code, token, Contact.api)).json()
            big_lst.append(vk_exec)
            time.sleep(0.34)
        # Собирает уникальный пул из друзей друзей
        for i in big_lst:
            for k in i['response']:
                if isinstance(k, dict):
                    uniq_fr.update(k['items'])
        return uniq_fr

    def handshake(self):
        # Если один чел просто есть в друзьях у другого чела возвращает их самих
        #
        if int(self.user1_id) in self.drugi_2chela:
            return self.user1_id, self.user2_id
        return self.handshake_2()

    def handshake_2(self):
        #  Смотрим есть ли общий знакомый у 2 челов
        check = set(self.drugi_1chela).intersection(set(self.drugi_2chela))
        # Если есть, то дергаем рандомного первого и рисуем типа 2 рукопожатия
        if check:
            return self.user1_id, random.choice(tuple(check)), self.user2_id
        return self.handshake_3()

    def handshake_3(self):
        for part in self.parts(self.drugi_1chela, 100):
            kek = requests.get("https://api.vk.com/method/friends.getMutual?source_uid=%s&target_uids=%s,%s&access_token=%s&v=%s"
                               % (self.user2_id, part[0], part, self.user_token, Contact.api)).json()['response']
            for lel in kek:
               if lel['common_count'] > 0:
                   return self.user1_id, lel['id'], lel['common_friends'][0], self.user2_id
            time.sleep(0.34)
        return self.handshake_4()

    def handshake_4(self):
        dd_1ch = Contact.get_fr_of_fr(self.drugi_1chela, self.app_token)
        dd_2ch = Contact.get_fr_of_fr(self.drugi_2chela, self.app_token2)
        check = tuple(dd_1ch.intersection(dd_2ch))
        if check:
            for candidate in check:
                if defender(candidate, self.service_key, Contact.api)[0] == 'ok':
                    m3_friend = candidate
                    m2_1friend = requests.get(
                        "https://api.vk.com/method/friends.getMutual?source_uid=%s&target_uid=%s&access_token=%s&v=%s" % (
                        self.user1_id, m3_friend, self.user_token, Contact.api)).json()['response'][0]
                    m2_2friend = requests.get(
                        "https://api.vk.com/method/friends.getMutual?source_uid=%s&target_uid=%s&access_token=%s&v=%s" % (
                        self.user2_id, m3_friend, self.user_token, Contact.api)).json()['response'][0]
                    return self.user1_id, m2_1friend, m3_friend, m2_2friend, self.user2_id

        return "not found"
