import BlockchainApi
import time


def main():
    start = time.time()
    uri = 'https://blockchain.info/latestblock'
    hash = '00000000000000000013db796853a933a792181f84d31dc0012a744b1e56879a'

    blockchain_api = BlockchainApi.BlockchainApi(uri)

    while True:
        end = time.time()
        if (end - start) > 30:
            latest_block = blockchain_api.get_latest_block()
            print(f'hash: {latest_block["hash"]}')
            print(f'time: {latest_block["time"]}')
            print(f'height: {latest_block["height"]}')
            print('')
            start = time.time()


if __name__ == "__main__":
    main()
