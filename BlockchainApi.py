import requests


class BlockchainApi:
    def __init__(self, _uri):
        self.uri = _uri

    def get_latest_block(self):
        response = requests.get(self.uri)
        return response.json()

    def get_specific_block(self, block_hash):
        response = requests.get(self.uri, params={'block_hash': block_hash}, )
        return response.json()
