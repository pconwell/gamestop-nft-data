# import necessary libraries
import requests
import csv
from datetime import datetime
from time import sleep


# Get the number of collections (we could just use a really big limit instead, but this helps future proofing)
Collections_count = requests.get("https://api.nft.gamestop.com/nft-svc-marketplace/getCollectionsPaginated?&limit=0").json()['totalNum']

# Get all collections overview data
Collections_overview_data = requests.get(f"https://api.nft.gamestop.com/nft-svc-marketplace/getCollectionsPaginated?&limit={Collections_count}").json()

# go through each individual collection from Collections_data
Collections_individual_data = {}
for index, collection in enumerate(Collections_overview_data['data']):
    try:
        Collections_individual_data[collection['collectionId']] = requests.get(f"https://api.nft.gamestop.com/nft-svc-marketplace/getCollectionStats?collectionId={collection['collectionId']}").json()
        print(f"gathering data on collection {index+1} of {Collections_count} - {collection['slug']} {Collections_individual_data[collection['collectionId']]}")
        sleep(.25)
    except:
        print(f"skipping error on collection collection['collectionId'] ******************************************************************************************")
        pass

# sum up the values we want from the individual collections
wei = sum([int(i['totalVolume']) for i in Collections_individual_data.values()])
items = sum([int(i['itemCount']) for i in Collections_individual_data.values()])
forsale = sum([int(i['forSale']) for i in Collections_individual_data.values()])

# print(f"Total eth: {wei * 10 ** -18} Total Items: {items} For Sale: {forsale}")

#write to csv file
with open('/root/gamestop-nft-data/gamestop_nft_data.csv', mode='a') as f:
    w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerow([datetime.now(), wei, items, forsale])
