import csv
import os
import requests
from os.path import exists
from datetime import datetime

import get_collection_data



collection_data = get_collection_data.run_main()
collection_slugs = {i['collectionId']: i['slug'] for i in requests.get("https://api.nft.gamestop.com/nft-svc-marketplace/getCollections").json()}
existing_collection_ids = [i['UUID'] for i in csv.DictReader(open("/root/gamestop-nft-data/indivdual_data.csv"))]
incoming_collection_ids = [i for i in collection_data.keys()]
existing_columns = next(csv.reader(open("/root/gamestop-nft-data/indivdual_data.csv")))

added = set(incoming_collection_ids).difference(existing_collection_ids)

collection_data['total'] = {"collectionId": "total", "totalVolume": sum([int(i['totalVolume']) for i in collection_data.values()])}


if exists("/root/gamestop-nft-data/indivdual_data.csv"):

    with open("/root/gamestop-nft-data/indivdual_data.csv", mode='r') as f:
        csv_reader = csv.DictReader(f)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        csv_reader.fieldnames.append(now)

        with open("/root/gamestop-nft-data/temp.csv", mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_reader.fieldnames)
            writer.writeheader()
            for i in csv_reader:
                try:
                    i[now] = collection_data[i['UUID']]['totalVolume']
                except KeyError:
                    i[now] = 0
                writer.writerow(i)

            for a in added:
                writer.writerow({'UUID': collection_data[a]['collectionId'], 'slug': collection_slugs[a], now: collection_data[a]['totalVolume']})

    os.remove("/root/gamestop-nft-data/indivdual_data.csv")
    os.rename("/root/gamestop-nft-data/temp.csv", "/root/gamestop-nft-data/indivdual_data.csv")

else:

    with open('/root/gamestop-nft-data/indivdual_data.csv', mode='w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['UUID', 'slug', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow(['total','total',sum([int(i['totalVolume']) for i in collection_data.values()])])
        
        for k,v in collection_data.items():
            writer.writerow([k, collection_slugs[k], v['totalVolume']])
