import requests
import time

start = time.time()
uri = 'https://blockchain.info/latestblock'

while True:
    end = time.time()
    if (end - start) > 30:
        response = requests.get(uri)
        latest_block = response.json()
        print(f'hash: {latest_block["hash"]}')
        print(f'time: {latest_block["time"]}')
        print(f'height: {latest_block["height"]}')
        print('')
        start = time.time()
