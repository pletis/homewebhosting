from ecc import PrivateKey
from helper import decode_base58, SIGHASH_ALL,hash256,hash160,encode_base58
from script import p2pkh_script, Script
from tx import TxIn, TxOut, Tx
from mytestnetaddress import mysecret

mvop3gM6C7P3JwQpPsixUffDgSN1P5hch8

#보낼 주소
input_target_address = 'my7adnDoe9pt3hP3m9Qfc8qSMyTx5ynYK3'

#받을 주소
#민혁이 공개키 : mue5XYkgFJWGvvfyAg6gomoNvxwYAKqngC
input_change_address = 'mue5XYkgFJWGvvfyAg6gomoNvxwYAKqngC'

#28d2dc5ba74d9e4a9aa8da2cf47b3c738f03a560ed6bb92b5bd24d02a984ea74
#28d2dc5ba74d9e4a9aa8da2cf47b3c738f03a560ed6bb92b5bd24d02a984ea74
prev_tx = bytes.fromhex('28d2dc5ba74d9e4a9aa8da2cf47b3c738f03a560ed6bb92b5bd24d02a984ea74')

mysecret = 'c4e7fa90a3c9fce935b6b21cdb8966194634e59844872c4c8f79e02230a2cbb5'

prev_index = 1

target_address = input_target_address
target_amount =
change_address = input_change_address
change_amount = 0.013
secret = mysecret

print(mysecret)
print(PrivateKey(secret=secret))
priv = PrivateKey(secret=secret)
tx_ins = []
tx_ins.append(TxIn(prev_tx, prev_index))
tx_outs = []
h160 = decode_base58(target_address)
script_pubkey = p2pkh_script(h160)
target_satoshis = int(target_amount*100000000)
tx_outs.append(TxOut(target_satoshis, script_pubkey))
h160 = decode_base58(change_address)
script_pubkey = p2pkh_script(h160)
change_satoshis = int(change_amount*100000000)
tx_outs.append(TxOut(change_satoshis, script_pubkey))
tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)

#print(tx_obj.sign_input(0, priv))
print(tx_obj.serialize().hex())
#print(tx_obj.id())
print('그래서 트랜잭션은?')
print(tx_obj)
