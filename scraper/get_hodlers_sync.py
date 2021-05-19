import os
import json
import requests

from heapq import heappush, heappop

headers = {
    'authority': 'bitclout.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'content-type': 'application/json',
    'origin': 'https://bitclout.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-GB,en;q=0.9,hr-HR;q=0.8,hr;q=0.7,en-US;q=0.6,de;q=0.5,bs;q=0.4',
    # IMPORTANT: CHANGE THE `cookie` HEADER TO YOUR OWN COOKIE
    'cookie': 'amplitude_id_YOUR_OWN_BITCLOUT_COOKIE',
    'sec-gpc': '1',
}


def get_hodlers(user):
    data = f'{{"PublicKeyBase58Check":"","Username":"{user}","LastPublicKeyBase58Check":"","NumToFetch":100,"FetchHodlings":false,"FetchAll":true}}'

    response = requests.post('https://bitclout.com/api/v0/get-hodlers-for-public-key', headers=headers, data=data)

    hodlers = response.text
    with open(f'hodlers/{user}.json', 'w') as f:
        print(hodlers, file=f)

    return json.loads(hodlers)


if __name__ == '__main__':
    users = []
    seen = set()
    directory = os.path.dirname(__file__) + '/hodlers'
    for f in os.listdir(directory):
        seen.add(f[:-5])

    for f in os.listdir(directory):
        hodlers = json.load(directory + '/' + f)
        for hodler in hodlers['Hodlers']:
            try:
                n = hodler['ProfileEntryResponse']['CoinEntry']['NumberOfHolders']
                user = hodler['ProfileEntryResponse']['Username']
                if user not in seen:
                    heappush(users, (-n, user))
            except Exception:
                continue

    while users:
        _, user = heappop(users)
        seen.add(user)
        try:
            hodlers = get_hodlers(user)
        except Exception:
            continue
        for hodler in hodlers['Hodlers']:
            try:
                n = hodler['ProfileEntryResponse']['CoinEntry']['NumberOfHolders']
                user = hodler['ProfileEntryResponse']['Username']
                if user not in seen:
                    heappush(users, (-n, user))
            except Exception:
                continue
