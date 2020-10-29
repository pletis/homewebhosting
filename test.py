from cryptos import *
import json

#
#my7adnDoe9pt3hP3m9Qfc8qSMyTx5ynYK3
#박동현
#mvop3gM6C7P3JwQpPsixUffDgSN1P5hch8

#test
c = Bitcoin(testnet=True)
#c = Bitcoin(testnet=False)
#brain = 'a big long brainwallet password'
#brain = 'kk5339navercom Claudiana1040*'
brain = 'chlrhalsgurnaver.com choi2044'
#brain = 'KBU_201601071_PARKDONGHYUNE' #b'~'값이랑 출력이 똑같음.
priv = sha256(brain)
pub = c.privtopub(priv)
addr = c.pubtoaddr(pub)
inputs = c.unspent(addr)
history = c.history(addr)

print(f'비트코인 라이브러리 테스트')
#print(f'send 테스트 : {test}\n')
print(f'입력값 : {brain}\n')
print(f'비밀키 : {priv}\n')
print(f'공개키 : {pub}\n')
print(f'주  소 : {addr}\n')
