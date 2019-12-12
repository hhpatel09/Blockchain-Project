import requests
import json
import hash_maker


def main(tx_hash):
    # first tx_hash = f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16
    # first tx block hash = 00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee
    # genesis_block hash = 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f

    # get block height from transaction data
    uri_tx = "https://blockchain.info/rawtx/"
    response_tx = requests.get(uri_tx + tx_hash, params={'format': 'json'}, )
    res = response_tx.json()
    url = 'https://blockchain.info/block-height/'
    block_height = str(res['block_height'])

    # get block from block height
    response = requests.get(url + block_height, params={'format': 'json'}, )
    y = json.loads(response.text)
    block_hash = y["blocks"][0]['hash']
    print("hash: " + block_hash)

    # get block raw data from block hash
    url = 'https://blockchain.info/rawblock/' + block_hash
    response = requests.get(url, params={'format': 'hex'}, )
    # response = requests.get(url)
    return response.text


# parse out block into usable components
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
    block["txs"] = []
    for i in range(x):
        block["txs"].append({})
        start = end
        end += 8
        block["txs"][i]["trans_version"] = string[start:end]

        # transaction input data
        start = end
        end += 2
        block["txs"][i]["num_inputs"] = string[start:end]
        # TODO: put the rule checking in here. Everything after this will change again***
        num_inputs = int('0x' + block["txs"][i]["num_inputs"], 0)
        block["txs"][i]["tx_inputs"] = []
        for k in range(num_inputs):
            block["txs"][i]["tx_inputs"].append({})

            start = end
            end += 64
            block["txs"][i]["tx_inputs"][k]["pre_tx_hash"] = string[start:end]

            start = end
            end += 8
            block["txs"][i]["tx_inputs"][k]["pre_tx_out_index"] = string[start:end]

            start = end
            end += 2
            block["txs"][i]["tx_inputs"][k]["input_script_length"] = string[start:end]
            input_script_length = int('0x' + string[start:end], 0)

            start = end
            end += input_script_length * 2
            block["txs"][i]["tx_inputs"][k]["input_script"] = string[start:end]

            start = end
            end += 8
            block["txs"][i]["tx_inputs"][k]["sequence"] = string[start:end]

        # transaction outputs
        start = end
        end += 2
        block["txs"][i]["num_outputs"] = string[start:end]
        # TODO: put the rule checking in here. Everything after this will change again***
        num_outputs = int('0x' + block["txs"][i]["num_outputs"], 0)
        block["txs"][i]["tx_outputs"] = []
        for k in range(num_outputs):
            block["txs"][i]["tx_outputs"].append({})

            start = end
            end += 16
            block["txs"][i]["tx_outputs"][k]["value"] = string[start:end]

            start = end
            end += 2
            block["txs"][i]["tx_outputs"][k]["output_script_length"] = string[start:end]
            output_script_length = int('0x' + string[start:end], 0) * 2

            start = end
            end += output_script_length
            block["txs"][i]["tx_outputs"][k]["output_script"] = string[start:end]

        start = end
        end += 8
        block["txs"][i]["lock_time"] = string[start:end]

    return block


# get first transaction data
def get_transaction_data(block, index):
    trans_data = ''
    trans_data += block["txs"][index]["trans_version"]

    # get all inputs
    trans_data += block["txs"][index]["num_inputs"]
    for i in range(int('0x' + block["txs"][index]["num_inputs"], 0)):
        trans_data += block["txs"][index]["tx_inputs"][i]["pre_tx_hash"]
        trans_data += block["txs"][index]["tx_inputs"][i]["pre_tx_out_index"]
        trans_data += block["txs"][index]["tx_inputs"][i]["input_script_length"]
        trans_data += block["txs"][index]["tx_inputs"][i]["input_script"]
        trans_data += block["txs"][index]["tx_inputs"][i]["sequence"]

    # get all outputs
    trans_data += block["txs"][index]["num_outputs"]
    for i in range(int('0x' + block["txs"][index]["num_outputs"], 0)):
        trans_data += block["txs"][index]["tx_outputs"][i]["value"]
        trans_data += block["txs"][index]["tx_outputs"][i]["output_script_length"]
        trans_data += block["txs"][index]["tx_outputs"][i]["output_script"]

    trans_data += block["txs"][index]["lock_time"]

    return trans_data


if __name__ == "__main__":
    tx_hash = 'f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16'
    hex_str = main(tx_hash)
    block_data = parse_block(hex_str)
    trans_data_str = get_transaction_data(block_data, 1)
    print(hash_maker.hasher(trans_data_str))
