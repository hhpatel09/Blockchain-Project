import requests
import json


# hex: 0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c0101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000
def main():
    # first tx_hash = f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16
    # genesis_block hash = 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
    url = 'https://blockchain.info/block-height/170?format=json'
    response = requests.get(url)
    y = json.loads(response.text)
    block_hash = y["blocks"][0]['hash']
    print("hash: " + block_hash)
    url = 'https://blockchain.info/rawblock/' + block_hash
    response = requests.get(url, params={'format': 'hex'}, )
    # response = requests.get(url)
    return response.text


def parse_block(string):
    block = {}
    # block header stuff
    start = 0
    end = 8
    block["block_version"] = string[start:end]

    start = end
    end += 64
    block["pre_block_hash"] = string[start:end]

    start = end
    end += 64
    block["merkle_root"] = string[start:end]

    start = end
    end += 8
    block["time"] = string[start:end]

    start = end
    end += 8
    block["bits"] = string[start:end]

    start = end
    end += 8
    block["nonce"] = string[start:end]

    # transactions
    start = end
    end += 2
    block["num_trans"] = string[start:end]

    # TODO: put the rule checking in here. Everything after this will change***
    x = int('0x' + block["num_trans"], 0)
    for i in range(x):
        start = end
        end += 8
        block["trans_version"] = string[start:end]

        # transaction input data
        start = end
        end += 2
        block["num_inputs"] = string[start:end]
        # TODO: put the rule checking in here. Everything after this will change again***

        start = end
        end += 64
        block["pre_tx_hash"] = string[start:end]

        start = end
        end += 8
        block["pre_tx_out_index"] = string[start:end]

        start = end
        end += 2
        block["input_script_length"] = int('0x' + string[start:end], 0)

        start = end
        end += block["input_script_length"] * 2
        block["input_script"] = string[start:end]

        start = end
        end += 8
        block["sequence"] = string[start:end]

        # transaction outputs
        start = end
        end += 2
        block["num_outputs"] = string[start:end]
        # TODO: put the rule checking in here. Everything after this will change again***

        start = end
        end += 16
        block["value"] = string[start:end]

        start = end
        end += 2
        block["output_script_length"] = int('0x' + string[start:end], 0) * 2

        start = end
        end += block["output_script_length"]
        block["output_script"] = string[start:end]

        start = end
        end += 8
        block["lock_time"] = string[start:end]

    return block


if __name__ == "__main__":
    # hex_str = '0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768' \
    #           'f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c010100000001000000000000000000000000000000' \
    #           '0000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f3230303' \
    #           '9204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffff' \
    #           'ffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4' \
    #           'cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000'

    hex_str = main()
    block_data = parse_block(hex_str)

