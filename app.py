from flask import Flask, request, render_template, jsonify
#from cryptos import *
from bs4 import BeautifulSoup

from ecc import PrivateKey
from helper import decode_base58, SIGHASH_ALL,hash256,hash160,encode_base58
from script import p2pkh_script, Script
from tx import TxIn, TxOut, Tx
from mytestnetaddress import mysecret

from cryptos import *
import json

import qrcode
import os
import shutil

app = Flask(__name__)

c = Bitcoin(testnet=True)
#@app.route('/')
#def hellow():
#    return 'Hellow, World'


@app.route('/')
def homepagehtml():
    return render_template("index.html")


@app.route('/request', methods=['POST'])
def CreatBitcoinWallet():
    data = request.get_json()
    print(data)
    a = str(data['email']).replace("@","").replace(".","")
    print(a)
    b = str(data['password'])
    brain =(a+' '+b)
    print(brain)

    priv = sha256(brain)
    pub = c.privtopub(priv)
    addr = c.pubtoaddr(pub)

    print(f'비트코인 라이브러리 테스트')
    print(f'입력값 : {brain}\n')
    print(f'비밀키 : {priv}\n')
    print(f'공개키 : {pub}\n')
    print(f'주  소 : {addr}\n')

    img = qrcode.make(addr) # 주 소 qr코드 이미지 생성
    img2 = qrcode.make(priv) # 비밀키 qr코드 이미지 생성

    filename = 'addr.png'
    filename2 = 'priv.png'

    #filename = addr+'.png'
    #filename2 = priv+'.png'
    #print(filename)
    img.save(filename)
    img2.save(filename2)

    if os.path.isfile("static/images/addr.png"):
        os.remove('static/images/addr.png')
    if os.path.isfile('static/images/priv.png'):
        os.remove('static/images/priv.png')


    shutil.move(filename,'static/images') #
    shutil.move(filename2,'static/images') #

    data['email'] = addr #data객체(딕셔너리)에 주소 담기
    data['password'] = priv #data 객체(딕셔너리)에 비밀키 담기

    return jsonify(result = "success", result2= data) #index의 $.ajax({})에 데이터 반환


@app.route('/detail', methods=['POST'])
def InfoWallet():

    data = request.get_json()
    print(data)
    addr = data['addr']
    inputs = c.unspent(addr)
    history = c.history(addr)

    balance = history['final_balance']
    total_received = history['total_received']
    total_sent = history['total_sent']
    tx_history = history['txs']

    list_key = []
    list_value = []

    f = open("info.txt", 'w')
    f.write('<!DOCTYPE html>\n')
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('<title>'+addr+'</title>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<pre>\n')
    f.write('address : '+addr+'\n')
    f.write('balance : '+balance+'\n')
    f.write('total_sent : '+total_sent+'\n')
    f.write('total_received : '+total_received+'\n')

    for i in range (len(tx_history)):
        print(f'트랜잭션 {len(tx_history) - i})')
        f.write('tx_num : '+str(len(tx_history) - i)+'\n')
        #print(tx_history[i].get('inputs'))
        for j in range (len(tx_history[i].get('inputs'))):
            #print(tx_history[i].get('inputs')[j])
            print('sequence')
            print(tx_history[i].get('inputs')[j].get('sequence'))
            f.write('sequence : '+str(tx_history[i].get('inputs')[j].get('sequence'))+'\n')

            print('witness')
            print(tx_history[i].get('inputs')[j].get('witness'))
            f.write('witness : '+str(tx_history[i].get('inputs')[j].get('witness'))+'\n')

            print('prev_out')
            print(tx_history[i].get('inputs')[j].get('prev_out'))
            f.write('prev_out : '+str(tx_history[i].get('inputs')[j].get('prev_out'))+'\n')

            print('script')
            print(tx_history[i].get('inputs')[j].get('script'))
            f.write('script : '+str(tx_history[i].get('inputs')[j].get('script'))+'\n')


        #for j in range (len(tx_history[i].get('out'))):
        #    print(tx_history[i].get('out')[j].keys())
        print('result')
        print(tx_history[i].get('result'))
        f.write('result : '+str(tx_history[i].get('result'))+'\n')
        print()
        f.write('\n\n')

    f.write('</pre>\n')
    f.write('</body>\n')
    f.write('</html>\n')
    f.close()

    old_filename = 'info.txt'
    new_filename = os.path.splitext(old_filename)[0] + '.html'
    os.rename(old_filename, new_filename)

    if os.path.isfile("templates/info.html"):
        os.remove('templates/info.html')
    print("시발")
    print(data)
    data['addr'] = addr
    data['balance'] = balance
    data['total_sent'] = total_sent
    data['total_received'] = total_received

    shutil.move('info.html','templates/')

    return jsonify(result = "success", result2= data)


@app.route('/page2.html')
def page2html():
    return render_template("page2.html")


@app.route('/plugin/plugin_home.html')
def plugin_homehtml():
    return render_template("plugin_home.html")


@app.route('/info')
def info_txt():
    return render_template("info.html")






if __name__ =='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
