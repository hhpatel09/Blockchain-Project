import codecs
import hashlib
import requests


# switch the endianness of a given string
def revEndian(str):
    return ''.join(reversed([str[i:i + 2] for i in range(0, len(str), 2)]))


# convert a bytebuffer into a string
def hashStr(bytebuffer):
    return str(codecs.encode(bytebuffer, 'hex'))[2:-1]


# find the double sha256 hash for a given hex string
def hasher(hex):
    bin = codecs.decode(hex, 'hex')
    hash = hashlib.sha256(bin).digest()
    hash2 = hashlib.sha256(hash).digest()
    return revEndian(hashStr(hash2))


# uri = 'https://blockchain.info/rawtx/'
# tx_id = 'f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16'
# response = requests.get(uri + tx_id, params={'format': 'hex'}, )
# print(response.text)
# print(hasher('0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c'))
#
# # https://bitcoin.stackexchange.com/questions/2177/how-to-calculate-a-hash-of-a-tx
