import requests
import json
import hash_maker

SATOSHI_TO_BTC = 0.00000001


def main(tx_hash):
    # first tx_hash = f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16
    # first tx block hash = 00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee
    # genesis_block hash = 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f

    # get block height from transaction data
    uri_tx = "https://blockchain.info/rawtx/"
    response_tx = requests.get(uri_tx + tx_hash, params={'format': 'json'}, )
    if response_tx.status_code != 200:
        return -1
    res = response_tx.json()
    url = 'https://blockchain.info/block-height/'
    block_height = str(res['block_height'])
    print("Block Height: %s" % block_height)

    # get block from block height
    response = requests.get(url + block_height, params={'format': 'json'}, )
    y = json.loads(response.text)
    block_hash = y["blocks"][0]['hash']
    print("block hash: " + block_hash)

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
    tmp = hex_to_uint32(string[start:end])
    if tmp == 253:
        start = end
        end += 4
    block["num_trans"] = string[start:end]

    # TODO: put the rule checking in here. Everything after this will change***
    x = hex_to_uint32(block["num_trans"])
    block["txs"] = []
    for i in range(x):
        block["txs"].append({})
        start = end
        end += 8
        block["txs"][i]["trans_version"] = string[start:end]

        # transaction input data
        start = end
        end += 2
        # TODO: == 253 rule checking in, add more
        block["txs"][i]["input_identifier"] = ''
        tmp = hex_to_uint32(string[start:end])
        if tmp == 253:
            block["txs"][i]["input_identifier"] = string[start:end]
            start = end
            end += 4
        block["txs"][i]["num_inputs"] = string[start:end]
        num_inputs = hex_to_uint32(block["txs"][i]["num_inputs"])
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


# get transaction data at a certain index
def get_transaction_data(block, index):
    trans_data = ''
    trans_data += block["txs"][index]["trans_version"]

    # get all inputs
    trans_data += block["txs"][index]["input_identifier"]
    trans_data += block["txs"][index]["num_inputs"]
    for i in range(hex_to_uint32(block["txs"][index]["num_inputs"])):
        trans_data += block["txs"][index]["tx_inputs"][i]["pre_tx_hash"]
        trans_data += block["txs"][index]["tx_inputs"][i]["pre_tx_out_index"]
        trans_data += block["txs"][index]["tx_inputs"][i]["input_script_length"]
        trans_data += block["txs"][index]["tx_inputs"][i]["input_script"]
        trans_data += block["txs"][index]["tx_inputs"][i]["sequence"]

    # get all outputs
    trans_data += block["txs"][index]["num_outputs"]
    for i in range(hex_to_uint32(block["txs"][index]["num_outputs"])):
        trans_data += block["txs"][index]["tx_outputs"][i]["value"]
        trans_data += block["txs"][index]["tx_outputs"][i]["output_script_length"]
        trans_data += block["txs"][index]["tx_outputs"][i]["output_script"]

    trans_data += block["txs"][index]["lock_time"]

    return trans_data


# loop through transactions, hash it, find the one that matches the given hash
def find_transaction(block):
    for j in range(hex_to_uint32(block["num_trans"])):
        trans_data_str = get_transaction_data(block, j)
        calculated_hash = hash_maker.hasher(trans_data_str)
        if tx_hash == calculated_hash:
            return j

    return -1


# print all the data from the specified transaction
def print_transaction_data(block, index, tx_hash):
    print("------------- TRANSACTION DATA ----------------")
    print("Transaction number: %d" % index)
    print("Transaction Hash: %s" % tx_hash)
    print("Version: %d" % hex_to_uint32(block["txs"][index]["trans_version"]))

    # Display TX inputs
    print("Number of inputs: %d" % hex_to_uint32(block["txs"][index]["num_inputs"]))
    for i in range(hex_to_uint32(block["txs"][index]["num_inputs"])):
        print("Transaction Input %d" % i)
        print("\tPrevious TX Hash: %d" % hex_to_uint32(block["txs"][index]["tx_inputs"][i]["pre_tx_hash"]))
        print("\tPrevious TX Output Index: %d" % hex_to_uint32(block["txs"][index]["tx_inputs"][i]["pre_tx_out_index"]))
        print("\tInput Script Length: %d" % hex_to_uint32(block["txs"][index]["tx_inputs"][i]["input_script_length"]))
        print("\tInput Script: %s" % block["txs"][index]["tx_inputs"][i]["input_script"])
        print("\tSequence: %d" % hex_to_uint32(block["txs"][index]["tx_inputs"][i]["sequence"]))

    # Display TX Outputs
    print("Number of outputs: %d" % hex_to_uint32(block["txs"][index]["num_outputs"]))
    for i in range(hex_to_uint32(block["txs"][index]["num_outputs"])):
        print("Transaction Output %d" % i)
        print("\tValue: %fBTC" % float(hex_to_uint32(block["txs"][index]["tx_outputs"][i]["value"]) * SATOSHI_TO_BTC))
        print("\tOutput Script Length: %d" % hex_to_uint32(block["txs"][index]["tx_outputs"][i]["output_script_length"]))
        print("\tOutput Script: %s" % block["txs"][index]["tx_outputs"][i]["output_script"])

    print("Lock Time: %d" % hex_to_uint32(block["txs"][index]["lock_time"]))


# Converts a hex string to a unsigned 32 bit integer based on its endianness
def hex_to_uint32(string, endianness='little-endian'):
    if endianness == 'big-endian':
        return int('0x' + string, 0)
    elif endianness == 'little-endian':
        return hex_to_uint32(hash_maker.revEndian(string), 'big-endian')


if __name__ == "__main__":
    # tx_hash = 'f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16'  # first TX, blk height 170
    # tx_hash = 'b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082'  # first TX, blk height 170
    # tx_hash = 'fe28050b93faea61fa88c4c630f0e1f0a1c24d0082dd0e10d369e13212128f33'  # block height 1,000
    # tx_hash = '6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4'  # block height 100,000
    # tx_hash = 'b5f6e3b217fa7f6d58081b5d2a9a6607eebd889ed2c470191b2a45e0dcb98eb0'  # block height 150,000
    # tx_hash = 'ee475443f1fbfff84ffba43ba092a70d291df233bd1428f3d09f7bd1a6054a1f'  # blk height 200,000, 388 TX's
    tx_hash = 'bcb887acb2c01b6c5c8b92c22a368135d207f07a26eff170fe730b1cd40d2547'  # blk height 200,000, TX 440 inputs
    hex_str = main(tx_hash)

    # if api returned something other than OK
    if hex_str == -1:
        print("Could not find transaction with the given hash")
        exit(0)

    block_data = parse_block(hex_str)
    tx_index = find_transaction(block_data)
    if tx_index == -1:
        print("Couldn't find tx")
        exit(0)

    print("Found TX at index: %d" % tx_index)
    print_transaction_data(block_data, tx_index, tx_hash)

