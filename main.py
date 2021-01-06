import json
import logging
import gspread
import requests
import uuid

from datetime import date, datetime
from oauth2client.service_account import ServiceAccountCredentials

from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
access_token = ''
logging.basicConfig(level=logging.INFO)


@app.route('/pesankue', methods=['GET', 'POST'])
def webhook():
    userReq = request.get_json(force=True)
    outputContexts = userReq.get('queryResult').get('outputContexts')
    action = userReq.get('queryResult').get('action')
    fb_sender_id = '2919206894815271'

    id_pesanan = uuid.uuid4().hex[:8]
    # return "Pesanan Masuk"
    if action == 'menu.kue':
        logging.info(action)
        return menu_kue(fb_sender_id)
    elif action == 'order.confirm':
        logging.info(action)
        return order_kue(outputContexts, fb_sender_id, action, id_pesanan)
    elif action == 'cek.pesanan':
        return cek_pesanan(outputContexts, fb_sender_id, action)


def menu_kue(fb_sender_id):
    url = f"https://graph.facebook.com/v4.0/me/messages?access_token={access_token}"
    jsdata = {
        "recipient": {
            "id": fb_sender_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Nastar",
                            "image_url": "https://scontent-sin6-1.xx.fbcdn.net/v/t1.0-9/88273837_111698277114400_7187246720357498880_n.png?_nc_cat=104&_nc_sid=e007fa&_nc_eui2=AeEKptTnhbb4sEBhBGPLEnupcC54IwbTQytwLngjBtNDK4LXEaJp47Ed7csUlkBWuatN36TuaSB0fXnQnVwGdWp_&_nc_ohc=rNeUi5NHCGUAX8NdLaf&_nc_ht=scontent-sin6-1.xx&oh=a9b71431b1a25b1f58945c946af0b2a8&oe=5F1998D8",
                            "subtitle": "Rasanya nanas yang berlimpah"
                        },
                        {
                            "title": "Kaastengel Special",
                            "image_url": "https://scontent-sin6-1.xx.fbcdn.net/v/t1.0-9/89049677_111698237114404_7182026642875744256_n.png?_nc_cat=104&_nc_sid=e007fa&_nc_eui2=AeFXMJx03D5kN9GzJhQhFZgBw8RJtRKCJzXDxEm1EoInNeWncW9Uzy4ZfH5x_Ze7eVcWQ9qRx-xW_8_cYMKyvoIf&_nc_ohc=goUkzM_HPGsAX_rZExG&_nc_ht=scontent-sin6-1.xx&oh=dd6b6fb730c5bb4811513f28a0cc380b&oe=5F16CE02",
                            "subtitle": "Rasa keju yang renyah"
                        },
                        {
                            "title": "Choco Stick",
                            "image_url": "https://scontent-sin6-1.xx.fbcdn.net/v/t1.0-9/89855278_111697983781096_9056820734193565696_n.png?_nc_cat=104&_nc_sid=e007fa&_nc_eui2=AeF5lESxMRejP6jMD1Z2AsY5FiiEjAN8NGAWKISMA3w0YI9ELk-eXDGdSyvJN47gOaF4t3DFmOfZiEmdvvZiphUl&_nc_ohc=y-q6-KkpWI8AX9XzvsO&_nc_ht=scontent-sin6-1.xx&oh=f405861158f7fd25157c3ddd707c9ffd&oe=5F168024",
                            "subtitle": "Keju dengan coklat"
                        },
                        {
                            "title": "Putri Salju",
                            "image_url": "https://scontent-sin6-2.xx.fbcdn.net/v/t1.0-9/88984270_111698407114387_8597036444977987584_n.png?_nc_cat=108&_nc_sid=e007fa&_nc_eui2=AeGidBl-YfnLyzJ4qSGpUVdRm_dW4HsHP9Ob91bgewc_03Sgn1Mp65kcOalDbWJ-AKUXJEKI0P7wq7CU_TaANspp&_nc_ohc=J8yO5e0RnecAX9z89oL&_nc_ht=scontent-sin6-2.xx&oh=a597b06cc647fef655413e376fb3ec10&oe=5F18F546",
                            "subtitle": "Manis seputih salju"
                        },
                        {
                            "title": "Lidah Kucing",
                            "image_url": "https://scontent-sin6-1.xx.fbcdn.net/v/t1.0-9/89787400_111698253781069_86188062211571712_n.png?_nc_cat=104&_nc_sid=e007fa&_nc_eui2=AeH4SFe63_xH3IGDp4o7sGWrbpsopQ6T3S5umyilDpPdLqlM__LoY9B8VBLBXCFaTkNA4kdxhgcWa2m7mF-hCvsc&_nc_ohc=b_DiF_V9gzcAX9kXlc3&_nc_ht=scontent-sin6-1.xx&oh=ad0ce9c3bec7ffe2cf5acfd8178932ea&oe=5F187DD5",
                            "subtitle": "Kriuk"
                        },
                        {
                            "title": "Sagu Keju",
                            "image_url": "https://scontent-sin6-2.xx.fbcdn.net/v/t1.0-9/89034626_111698533781041_772264656310894592_n.png?_nc_cat=102&_nc_sid=e007fa&_nc_eui2=AeE9A6JRKexipw2Fwvv0miuJTZ0wr-onjAlNnTCv6ieMCXuIhj37bOYbGWpFIp8HQztl1m6rT8obRJo37bosMQJz&_nc_ohc=G4-HN1reZwkAX_Y-Uw3&_nc_ht=scontent-sin6-2.xx&oh=8a5e0d4671065f8b1fa835f2854f57c9&oe=5F172920",
                            "subtitle": "Keju yang renyah"
                        },
                        {
                            "title": "Red Velvet",
                            "image_url": "https://scontent-sin6-1.xx.fbcdn.net/v/t1.0-9/89394973_111698500447711_4877520309088944128_n.png?_nc_cat=111&_nc_sid=e007fa&_nc_eui2=AeFqlZrtpq8wDK39c2KKt4W9_WZWQaUHZWD9ZlZBpQdlYKycVdlYMdVX9fDGn3sRh3cICjG4D8lr-dR9xQzZLLrs&_nc_ohc=afjg4T9S5yAAX8TMVoF&_nc_ht=scontent-sin6-1.xx&oh=5c215f6d94d0ff65aa2cd50b7cafdf31&oe=5F1A2167",
                            "subtitle": "Renyah"
                        }
                    ]
                }
            }
        }
    }
    resp = requests.request("POST", url, json=jsdata, timeout=600)

    jsdata2 = {
        "recipient": {
            "id": fb_sender_id
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": "Mau melakukan pemesanan?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Ya!",
                    "payload": "Pesan Kue Kering"
                }, {
                    "content_type": "text",
                    "title": "Tidak",
                    "payload": "Cancel order"
                }
            ]
        }
    }
    resp2 = requests.request("POST", url, json=jsdata2, timeout=600)
    logging.info(resp2.content)
    return "Success"


def order_kue(outputContexts, fb_sender_id, action, id_pesanan):
    list_pesanan = []
    # logging.info("JSON Pesanan")
    # logging.info(json.dumps(outputContexts))

    client = gspread.authorize(creds)
    for eachContext in outputContexts:
        # fb_sender_id = eachContext.get('parameters', {}).get(
        #     'facebook_sender_id') if fb_sender_id is None else fb_sender_id

        if 'contexts/generic' in eachContext['name']:
            dfinput = eachContext
            nama_pemesan = dfinput.get('parameters').get('name.original')
            nomor_telp = dfinput.get('parameters').get('phone.original')
            alamat_pemesan = dfinput.get('parameters').get('address.original')
            pesanan = dfinput.get('parameters').get('kue.original')

            # opening Sheets
            list_pesanan.append(
                {'nama': nama_pemesan.lower(), 'nomor': nomor_telp, 'alamat': alamat_pemesan, 'kue': pesanan})
            # Konversi variabel jenis kue type list menjadi str
            str_kue = ', '.join(list_pesanan[0]['kue'])
            # tanggal pemesanan dilakukan
            tanggal_format = datetime.now()
            tanggal_pesan = tanggal_format.strftime('%m/%d/%Y')
            # id_pesanan = uuid.uuid4().hex[:8]
            sheet = client.open('Pesanan Kue').sheet1
            sheet.append_row([list_pesanan[0]['nama'], list_pesanan[0]
                              ['nomor'], list_pesanan[0]['alamat'], str_kue, tanggal_pesan, id_pesanan])

    url = f"https://graph.facebook.com/v4.0/me/messages?access_token={access_token}"
    jsdata = {
        "recipient": {
            "id": fb_sender_id
        },
        "message": {
            "text": f'Berikut adalah order_ID: {id_pesanan} pesanan anda.\nSimpan Order_ID dengan baik untuk melakukan \"Cek Pesanan\"'
        }
    }
    resp = requests.request("POST", url, json=jsdata, timeout=600)
    logging.info(resp)
    return "ok"


def cek_pesanan(outputContexts, fb_sender_id, action):
    logging.info(action)
    logging.info(outputContexts)
    list_name = []
    client = gspread.authorize(creds)

    for eachContext in outputContexts:
        if 'contexts/cekpesanan-followup' in eachContext['name']:
            dfinput = eachContext
            get_nama = dfinput.get('parameters').get('name')
            list_name.append({'nama': get_nama.lower()})

            sheet = client.open('Pesanan Kue').sheet1
            try:
                search_name = sheet.find(list_name[0]['nama'])
                str_cell = str(search_name)
                number_row = str_cell[7:8]
                data_pencarian = sheet.row_values(number_row)
                print("string cell")
                print(str_cell)
                print(data_pencarian)

                url = f"https://graph.facebook.com/v4.0/me/messages?access_token={access_token}"
                jsdata = {
                    "recipient": {
                        "id": fb_sender_id
                    },
                    "message": {
                        "text": f'Berikut pesanan anda\n\nNama: {data_pencarian[0]}\nNomor HP: {data_pencarian[1]}\nAlamat: {data_pencarian[2]}\nOrder: {data_pencarian[3]}\nTanggal: {data_pencarian[4]}'
                    }
                }
                resp = requests.request("POST", url, json=jsdata, timeout=600)
                logging.info(resp)

            except gspread.exceptions.CellNotFound:
                url = f"https://graph.facebook.com/v4.0/me/messages?access_token={access_token}"
                jsdata = {
                    "recipient": {
                        "id": fb_sender_id
                    },
                    "message": {
                        "text": "Data pemesanan tidak ditemukan"
                    }
                }
                resp = requests.request("POST", url, json=jsdata, timeout=600)

    return "Ok"


if __name__ == '__main__':
    app.run()
