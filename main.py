import BlockchainApi
import time
import requests


def main():
    # start = time.time()
    # uri = 'https://blockchain.info/latestblock'
    # hash = '00000000000000000013db796853a933a792181f84d31dc0012a744b1e56879a'

    # uri = "https://blockchain.info/rawtx/"
    # block_hash = "8a6c6c5d27d18cc525307711f3463f3d97957a356ed39e641316f6aa890f342e"
    # response = requests.get(uri + block_hash, params={'format': "hex"}, )
    # print(response.text)
    print(int("b'4869206d79206e616d65206973206861727368", 10))

    # blockchain_api = BlockchainApi.BlockchainApi(uri)
    #
    # while True:
    #     end = time.time()
    #     if (end - start) > 30:
    #         latest_block = blockchain_api.get_latest_block()
    #         print(f'hash: {latest_block["hash"]}')
    #         print(f'time: {latest_block["time"]}')
    #         print(f'height: {latest_block["height"]}')
    #         print('')
    #         start = time.time()
    #


if __name__ == "__main__":
    main()
