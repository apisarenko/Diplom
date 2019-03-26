import requests
from urllib.parse import urlencode
import itertools
import json
import time

with open("token.json", 'r') as file:
    data = json.load(file)
    TOKEN = data[0]['token']

params = {
    'access_token': TOKEN,
    'v': 5.92
}

def check_user(user_input):
    try:
        int(user_input)
        try:
            params['user_ids'] = user_input
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
            params['user_ids'] = user_input
            response_get_id = requests.get(
                'https://api.vk.com/method/users.get',
                params
            )
            user_id = int(response_get_id.json()['response'][0]['id'])
        except KeyError:
            print('Пользователя с таким именем не существует!')
            exit(0)
    return user_id

def friend_list(person_id):
    params['user_id'] = person_id
    list_friends_id = []
    try:
        response_friends = requests.get('https://api.vk.com/method/friends.get', params)
        list_friends_id = response_friends.json()['response']['items']
    except KeyError:
        print('Пользователь ограничил доступ к своей странице, '
              'либо страница заблокирована администрацией ВК,'
              'получение данных не возможно!!!')
        exit(0)
    return list_friends_id

def group_list_user(person_id):
    params['user_id'] = person_id
    list_groups_person = []
    try:
        response_groups = requests.get('https://api.vk.com/method/groups.get', params)
        list_groups_person = response_groups.json()['response']['items']
    except Exception as e:
        if list_groups_person.json()['error']['error_code'] == 7:
            print('Нет прав для выполнения данного действия')
        if list_groups_person.json()['error']['error_code'] == 18:
            print('Страница удалена или заблокирована')
        if list_groups_person.json()['error']['error_code'] == 30:
            print('Профиль является приватным')
        if list_groups_person.json()['error']['error_code'] == 260:
            print('Доступ к списку групп ограничен настройками приватности')
        exit(0)
    return list_groups_person

def list_groups_friend(friends):
    list_friends_user = friends
    friend_group_list = []
    x = 0
    while x < len(list_friends_user):
        params['user_id'] = list_friends_user[x]
        count = 0
        x += 1
        try:
            friend_groups = requests.get('https://api.vk.com/method/groups.get', params)
            friend_group_list.append(friend_groups.json()['response']['items'])
            print('.')
            count += 1
        except Exception as e:
            if friend_groups.json()['error']['error_code'] == 6:
                time.sleep(0.33)
            else:
                print(friend_groups.json())
                count += 1
    return friend_group_list

def unique_groups(group_list, group_user):
    unique_list = group_list
    groups_user = group_user
    general_groups_friend = list(itertools.chain.from_iterable(unique_list))
    set_list_of_unique_groups = set(groups_user).difference(set(general_groups_friend))
    list_of_unique_groups = list(set_list_of_unique_groups)
    return list_of_unique_groups

def json_output(unique_groups):
    list_of_unique_groups = unique_groups
    output_list = []
    x = 0
    while x < len(list_of_unique_groups):
        params_out = {
            'group_id': list_of_unique_groups[x],
            'fields': 'members_count'
        }
        params.update(params_out)
        count = 0
        x += 1
        try:
            out_list = requests.get('https://api.vk.com/method/groups.getById', params)
            finish_list = out_list.json()['response'][0]
            output_finish_group = {'name': finish_list['name'],
                                     'gid': finish_list['id'],
                                     'members_count': finish_list['members_count']}
            output_list.append(output_finish_group)
            count += 1
        except Exception as e:
            if out_list.json()['error']['error_code'] == 6:
                time.sleep(0.33)
    return output_list

def main():
    user = input('Введите id или имя пользователя: ')
    user_id = check_user(user)
    print('id пользователя: ', user_id)
    list_friends_user = friend_list(user_id)
    print('Список друзей пользователя: ', list_friends_user)
    list_groups_user = group_list_user(user_id)
    print('Список групп пользователя: ', list_groups_user)
    friend_group_list = list_groups_friend(list_friends_user)
    print(friend_group_list)
    list_of_unique_groups = unique_groups(friend_group_list, list_groups_user)
    print(list_of_unique_groups)
    output_list = json_output(list_of_unique_groups)
    print(output_list)

    with open('groups.json', 'w', encoding='utf-8') as json_file:
        json.dump(output_list, json_file, ensure_ascii=False)


main()
