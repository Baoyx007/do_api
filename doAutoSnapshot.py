#!/usr/bin/env python
import requests
import time
from datetime import datetime

__author__ = 'haven'

api_token = 'c7e3803303bcd37b9859234bc910169b7cef7fa477d85fb3912ecf8fdaef7a76'
baseUrl = 'https://api.digitalocean.com/v2/'
headers = {'content_type': 'application/json', 'Authorization': 'Bearer ' + api_token}
droplet_id = '7914548'


def is_droplet_on():
    url = baseUrl + 'droplets/' + droplet_id
    r = requests.get(url, headers=headers)
    return r.json()['droplet']['status'] == 'active'


def power_off():
    url = baseUrl + "droplets/" + droplet_id + "/actions"
    params = {'type': 'power_off'}
    return post(params, url)


def power_on():
    url = baseUrl + "droplets/" + droplet_id + "/actions"
    params = {'type': 'power_on'}
    return post(params, url)


def post(params, url):
    r = requests.post(url, params=params, headers=headers)
    # print(r.status_code)
    if r.status_code != 201:
        r.raise_for_status()
    else:
        print(params['type'] + '\'operation start')
        return r.json()['action']['id']


def snapshot():
    url = baseUrl + "droplets/" + droplet_id + "/actions"
    params = {'type': 'snapshot', 'name': 'havenSFO :' + datetime.now().strftime('%a, %b %d %Y, %H:%M')}
    return post(params, url)


def check_action_status(action_id):
    url = baseUrl + 'actions/' + str(action_id)
    r = requests.get(url, headers=headers)
    completed = r.json()['action']['status'] == 'completed';
    print('action %d completed %s' % (action_id, completed))
    return r.json()['action']['status'] == 'completed'


def main():
    if is_droplet_on():
        action_id = power_off()
        while not check_action_status(action_id):
            time.sleep(5)
    print('success power_off')
    action_id = snapshot()
    while not check_action_status(action_id):
        time.sleep(25)
    print('success snapshot')
    power_on()


main()
