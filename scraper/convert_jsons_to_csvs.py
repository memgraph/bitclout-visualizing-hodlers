import os
import csv
import json


directory = os.path.dirname(__file__)
users = {}
hodls = []
for filename in os.listdir(directory + '/hodlers'):
    path = directory + '/hodlers/' + filename
    with open(path) as f:
        hodlers = json.load(f).get('Hodlers', [])
        for hodler in hodlers:
            hodls.append({
                'from': hodler['HODLerPublicKeyBase58Check'],
                'to': hodler['CreatorPublicKeyBase58Check'],
                'nanos': hodler.get('BalanceNanos', 0),
            })
            user = {
                'id': hodler['HODLerPublicKeyBase58Check'],
            }
            profile = hodler.get('ProfileEntryResponse')
            if profile is not None:
                coin = profile.get('CoinEntry')
                user.update({
                    'name': profile.get('Username'),
                    'description': profile.get('Description'),
                    'image': profile.get('ProfilePic'),
                    'isHidden': profile.get('IsHidden'),
                    'isReserved': profile.get('IsReserved'),
                    'isVerified': profile.get('IsVerified'),
                    'coinPrice': profile.get('CoinPriceBitCloutNanos'),
                    'creatorBasisPoints': coin.get("CreatorBasisPoints"),
                    'lockedNanos': coin.get("BitCloutLockedNanos"),
                    'nanosInCirculation': coin.get("CoinsInCirculationNanos"),
                    'watermarkNanos': coin.get("CoinWatermarkNanos"),
                })
            users[user['id']] = user

profile_columns = [
    'id',
    'name',
    'description',
    'image',
    'isHidden',
    'isReserved',
    'isVerified',
    'coinPrice',
    'creatorBasisPoints',
    'lockedNanos',
    'nanosInCirculation',
    'watermarkNanos',
]
names = set()
for user in users:
    name = users[user].get('name', None)
    if name is not None and name in names:
        print(name)
    names.add(name)

with open('profiles.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=profile_columns, lineterminator='\n')
    writer.writeheader()
    for user in users.values():
        writer.writerow(user)

hodl_columns = ['from', 'to', 'nanos']
with open('hodls.csv', 'w') as f:
    print(','.join(hodl_columns), file=f)
    for hodl in hodls:
        print(','.join(str(hodl[c]) for c in hodl_columns), file=f)
