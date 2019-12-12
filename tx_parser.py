import requests

uri_tx = "https://blockchain.info/rawtx/"
tx_hash = "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16"
response_tx = requests.get(uri_tx + tx_hash, params={'format': 'hex'}, )
print(response_tx.text)


uri_block = "https://blockchain.info/rawblock/"
block_hash = "00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee"
response_block = requests.get(uri_block + block_hash, params={'format': 'hex'}, )
print(response_block.text)

print(response_tx.text in response_block.text)

print("wklfnakwenfkwaenfkajwenflkewnf" in "kqawnrk23lqnrkq32wklfnakwenfkwaenfkajwenflkewnf23eqkl23nkr23n")