
import time
import requests


def main():
    # Getting the block height of the
    uri_tx = "https://blockchain.info/rawtx/"
    tx_hash = "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16"
    response_tx = requests.get(uri_tx + tx_hash, params={'format': 'json'}, )
    res = response_tx.json()
    print(res['block_height'])

    # uri_block_height = "https://blockchain.info/block-height/"
    # block_height_hash = "12321"
    # response = requests.get(uri_block_height + block_height_hash, params={'format': "json"}, )
    # print(response.json())




if __name__ == "__main__":
    main()
