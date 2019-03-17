import pprint
import requests
from urllib.parse import urlencode
import itertools


TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
params = {
    'user_ids': 10799607,
    'access_token': TOKEN,
    'v': 5.92
}

response_get_id = requests.get('https://api.vk.com/method/users.get', params)
user = int(response_get_id.json()['response'][0]['id'])

print(user)

response_groups = requests.get('https://api.vk.com/method/groups.get', params)
response_friends = requests.get('https://api.vk.com/method/friends.get', params)

groups_user = response_groups.json()['response']['items']
friends_id = response_friends.json()['response']['items']

print(groups_user)

print(friends_id)
