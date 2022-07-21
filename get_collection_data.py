import requests
import asyncio
from aiohttp import ClientSession


async def fetch_collection_data(id, session):
    """ Try to fetch individual collection data. If not, return backup data (top 50 collections). """

    url = "https://api.nft.gamestop.com/nft-svc-marketplace/getCollectionStats"

    try:
        resp = await session.get(url, params={"collectionId": id})
        return await resp.json()
    except:
        resp = await session.get("https://api.nft.gamestop.com/nft-svc-marketplace/getStats?timePeriod=0&type=collection")
        return await resp.json()


async def collections_temp_file(id, session, collection_data):
    """ Clean up data depending on what was passed (collection data or backup data). """
    res = await fetch_collection_data(id, session)

    if type(res) == dict:
        # If theres a dict, it's collection data
        res['collectionId'] = id
        del res['itemCount']
        del res['forSale']
        del res['floorPrice']

        collection_data[id] = res

    elif type(res) == list:
        # If theres a list, it's backup data

        try:
            # if the collection id was found in the backup data:
            backup_data = {i['collectionId']: [i['collectionId'], i['volume']] for i in res}[id]
            res = {'collectionId':backup_data[0], 'totalVolume':backup_data[1]}

            collection_data[id] = res

        except KeyError:
            # if the collection id was not found in the backup data:
            print("unable to restore backup data - Skipping... ", id)
            pass

    else:
        print(" ********* Error ********* ")


async def main():

    collection_data = {}
    collection_ids = [i['collectionId'] for i in requests.get("https://api.nft.gamestop.com/nft-svc-marketplace/getCollections").json()]

    async with ClientSession() as session:
        await asyncio.gather(*[collections_temp_file(id, session, collection_data) for id in collection_ids])

    return collection_data


def run_main():

    return asyncio.run(main())

if __name__ == "__main__":

    # t = asyncio.run(main())
    t = run_main()

    print(t)
    print(len(t))
    print(type(t))
    print(t['36fab6f7-1e51-49d9-a0be-39343abafd0f'])
