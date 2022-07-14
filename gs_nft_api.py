import requests
import csv
import logging
from datetime import datetime
from time import sleep


logging.basicConfig(filename='/root/gamestop-nft-data/gs_nft_api.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 

logging.info(f"\n\n***** starting gs_nft_api.py *****\n")

# Get the number of collections (we could just use a really big limit instead, but this helps future proofing)
Collections_count = requests.get("https://api.nft.gamestop.com/nft-svc-marketplace/getCollectionsPaginated?&limit=0").json()['totalNum']

# Get all collections overview data
Collections_overview_data = requests.get(f"https://api.nft.gamestop.com/nft-svc-marketplace/getCollectionsPaginated?&limit={Collections_count}").json()

# Get backup data from stats page (only shows top 50 collections)
Collections_backup_data = requests.get(f"https://api.nft.gamestop.com/nft-svc-marketplace/getStats?timePeriod=0&type=collection").json()


# go through each individual collection from Collections_data
Collections_individual_data = {}
for index, collection in enumerate(Collections_overview_data['data']):
    try:
        # For each collectionID, try to get the individual collection data
        Collections_individual_data[collection['collectionId']] = requests.get(f"https://api.nft.gamestop.com/nft-svc-marketplace/getCollectionStats?collectionId={collection['collectionId']}").json()
        logging.info(f"gathering data on collection {index+1} of {Collections_count} - {collection['slug']} {Collections_individual_data[collection['collectionId']]}")
        sleep(.25)
    except Exception as e:
        # If there's an error...
        logging.error(f"{collection['collectionId']} ({collection['slug']}) {e}")
        fixed = False

        # Attempt to get the individual collection data from the backup data
        for i in Collections_backup_data:
            if i['collectionId'] == collection['collectionId']:
                Collections_individual_data[collection['collectionId']] = {'itemCount': i['items'], 'floorPrice':0, 'totalVolume': i['volume'], 'forSale': 0}
                fixed = True
                break

        if fixed:    
            logging.error(f"{collection['collectionId']} ({collection['slug']}) Data successfully extracted from backup data")
        else:
            logging.error(f"{collection['collectionId']} ({collection['slug']}) Unable to find data in backup data")

# sum up the values we want from the individual collections
wei = sum([int(i['totalVolume']) for i in Collections_individual_data.values()])
items = sum([int(i['itemCount']) for i in Collections_individual_data.values()])
forsale = sum([int(i['forSale']) for i in Collections_individual_data.values()])

#write to csv file
with open('/root/gamestop-nft-data/gamestop_nft_data.csv', mode='a') as f:
    w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerow([datetime.now(), wei, items, forsale])
