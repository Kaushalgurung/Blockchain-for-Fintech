
import json
import requests

# Target address
address = '1Dorian4RoXcnBv9hnQ4Y2C1an6NJ4UrjX'

resp = requests.get('https://blockchain.info/unspent?active=%s' % address)
utxo_set = json.loads(resp.text)["unspent_outputs"]

for utxo in utxo_set:
    print("{tx_hash}:{tx_output_n} - {value} Satoshis".format(**utxo))
