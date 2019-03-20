import requests
from urllib.parse import urlencode
import itertools
import json
import time

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

user_input = input('Введите id или имя пользователя: ')

try:
    int(user_input)
    try:
        params = {
            'user_ids': user_input,
            'access_token': TOKEN,
            'v': 5.92
        }
        response_get_id = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        user_id = int(response_get_id.json()['response'][0]['id'])
    except KeyError:
        print('Пользователя с таким id не существует!')
        exit(0)
except ValueError:
    try:
        params = {
            'user_ids': user_input,
            'access_token': TOKEN,
            'v': 5.92
        }
        response_get_id = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        user_id = int(response_get_id.json()['response'][0]['id'])
    except KeyError:
        print('Пользователя с таким именем не существует!')
        exit(0)
print('id пользователя: ', user_id)

params = {
    'user_id': user_id,
    'access_token': TOKEN,
    'v': 5.92
}

try:
    response_groups = requests.get('https://api.vk.com/method/groups.get', params)
    response_friends = requests.get('https://api.vk.com/method/friends.get', params)
    groups_user = response_groups.json()['response']['items']
    friends_id = response_friends.json()['response']['items']
except KeyError:
    print('Пользователь ограничил доступ к своей странице, '
          'либо страница заблокирована администрацией ВК,'
          'получение данных не возможно!!!')
    exit(0)

print('Группы пользователя: ', groups_user)

print('id друзей пользователя', friends_id)

friend_group_list = []
for friend in friends_id:
    params = {
        'access_token': TOKEN,
        'user_id': friend,
        'v': 5.92
    }
    try:
        friend_groups = requests.get('https://api.vk.com/method/groups.get', params)
        friend_group_list.append(friend_groups.json()['response']['items'])
        print('.')
        time.sleep(1,5)
    except Exception as e:
        print(friend_groups.json())
general_groups_friend = list(itertools.chain.from_iterable(friend_group_list))
print(general_groups_friend)

set_list_of_unique_groups = set(groups_user).difference(set(general_groups_friend))
list_of_unique_groups = list(set_list_of_unique_groups)
print(list_of_unique_groups)

output_list = []
for individual_user_groups in list_of_unique_groups:
    params_out = {
        'group_id': individual_user_groups,
        'fields': 'members_count',
        'access_token': TOKEN,
        'v': 5.92
    }

    try:
        out_list_of_unique_groups = requests.get('https://api.vk.com/method/groups.getById', params_out)
        finish_list = out_list_of_unique_groups.json()['response'][0]
        output_finish_group = {'name': finish_list['name'],
                       'gid': finish_list['id'],
                       'members_count': finish_list['members_count']}
        output_list.append(output_finish_group)
    except KeyError:
        print(out_list_of_unique_groups.json())

print(output_list)

with open('groups.json', 'w', encoding='utf-8') as file:
    json.dump(output_list, file, ensure_ascii=False)
