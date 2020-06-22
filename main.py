import json
import logging
import gspread
import requests
import uuid

from datetime import date, datetime
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials

from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
access_token = 'EAAkc0ZCgiBl8BAAfzpD3IHVJr624w7aTb76rhptu1x5zEZC4EOnifQMjoXsgMm3RsTGT068A4bY38sDOVL05xFZCgyYwZBf75R6xW6UaWid5MH5H2XWYB1mQD5x0QUgzak4LfYXDgOl8V5CNzNZBCvQywDZAQVg0W8NR77AMDlaxgbJ0wBwRX6'
logging.basicConfig(level=logging.INFO)


@app.route('/pesankue', methods=['GET', 'POST'])
def webhook():
    userReq = request.get_json(force=True)
    outputContexts = userReq.get('queryResult').get('outputContexts')
    action = userReq.get('queryResult').get('action')
    fb_sender_id = '2919206894815271'
    # return "Pesanan Masuk"
    if action == 'menu.kue':
        logging.info(action)
        return menu_kue(fb_sender_id)
    elif action == 'order.confirm':
        logging.info(action)
        return order_kue(outputContexts, fb_sender_id, action)


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
                            "image_url": "https://scontent.fsub8-1.fna.fbcdn.net/v/t1.0-9/88273837_111698277114400_7187246720357498880_n.png?_nc_cat=104&_nc_sid=e007fa&_nc_eui2=AeEKptTnhbb4sEBhBGPLEnupcC54IwbTQytwLngjBtNDK4LXEaJp47Ed7csUlkBWuatN36TuaSB0fXnQnVwGdWp_&_nc_ohc=a_Jom8ai0V4AX-PyZoI&_nc_ht=scontent.fsub8-1.fna&oh=4ae1cd556449ef030c6e3923c2b7b058&oe=5EE62E58",
                            "subtitle": "Rasanya kaya nastar"
                        },
                        {
                            "title": "Kaastengel Special",
                            "image_url": "https://scontent.fsub8-1.fna.fbcdn.net/v/t1.0-9/89049677_111698237114404_7182026642875744256_n.png?_nc_cat=104&_nc_sid=e007fa&_nc_eui2=AeFXMJx03D5kN9GzJhQhFZgBw8RJtRKCJzXDxEm1EoInNeWncW9Uzy4ZfH5x_Ze7eVcWQ9qRx-xW_8_cYMKyvoIf&_nc_ohc=GoxQhx4WDq4AX-a9ZW1&_nc_ht=scontent.fsub8-1.fna&oh=54a4b00981c77cc467cd352404f6819b&oe=5EE36382",
                            "subtitle": "Rasa keju yang renyah"
                        },
                        {
                            "title": "Choco Stick",
                            "image_url": "https://scontent.fsub8-1.fna.fbcdn.net/v/t1.0-9/89855278_111697983781096_9056820734193565696_n.png?_nc_cat=104&_nc_sid=e007fa&_nc_eui2=AeF5lESxMRejP6jMD1Z2AsY5FiiEjAN8NGAWKISMA3w0YI9ELk-eXDGdSyvJN47gOaF4t3DFmOfZiEmdvvZiphUl&_nc_ohc=peUG1Sdbp1cAX8Qbbe_&_nc_ht=scontent.fsub8-1.fna&oh=3456967afe02e2a6edb9e11e9dbc77b7&oe=5EE315A4",
                            "subtitle": "Keju dengan coklat"
                        },
                        {
                            "title": "Putri Salju",
                            "image_url": "https://scontent.fsub8-1.fna.fbcdn.net/v/t1.0-9/88984270_111698407114387_8597036444977987584_n.png?_nc_cat=108&_nc_sid=e007fa&_nc_eui2=AeGidBl-YfnLyzJ4qSGpUVdRm_dW4HsHP9Ob91bgewc_03Sgn1Mp65kcOalDbWJ-AKUXJEKI0P7wq7CU_TaANspp&_nc_ohc=47YXMVM8xpIAX92rbFU&_nc_ht=scontent.fsub8-1.fna&oh=2310a99dbade6151234639049e459210&oe=5EE58AC6",
                            "subtitle": "Manis"
                        },
                        {
                            "title": "Lidah Kucing",
                            "image_url": "https://scontent.fsub8-1.fna.fbcdn.net/v/t1.0-9/89787400_111698253781069_86188062211571712_n.png?_nc_cat=104&_nc_sid=e007fa&_nc_eui2=AeH4SFe63_xH3IGDp4o7sGWrbpsopQ6T3S5umyilDpPdLqlM__LoY9B8VBLBXCFaTkNA4kdxhgcWa2m7mF-hCvsc&_nc_ohc=t60hAnu_y_8AX9LSq0z&_nc_ht=scontent.fsub8-1.fna&oh=5b1bf0cb72bf40c3fc649221c9d4bc1f&oe=5EE51355",
                            "subtitle": "Kriuk"
                        },
                        {
                            "title": "Sagu Keju",
                            "image_url": "https://scontent.fsub8-1.fna.fbcdn.net/v/t1.0-9/89034626_111698533781041_772264656310894592_n.png?_nc_cat=102&_nc_sid=e007fa&_nc_eui2=AeE9A6JRKexipw2Fwvv0miuJTZ0wr-onjAlNnTCv6ieMCXuIhj37bOYbGWpFIp8HQztl1m6rT8obRJo37bosMQJz&_nc_ohc=-6oiiiqDEJEAX9r4zj-&_nc_ht=scontent.fsub8-1.fna&oh=7ef41787ea49b9f2dd6c7486950e792e&oe=5EE3BEA0",
                            "subtitle": "Enak"
                        },
                        {
                            "title": "Red Velvet",
                            "image_url": "https://scontent.fsub8-1.fna.fbcdn.net/v/t1.0-9/89394973_111698500447711_4877520309088944128_n.png?_nc_cat=111&_nc_sid=e007fa&_nc_eui2=AeFqlZrtpq8wDK39c2KKt4W9_WZWQaUHZWD9ZlZBpQdlYKycVdlYMdVX9fDGn3sRh3cICjG4D8lr-dR9xQzZLLrs&_nc_ohc=VrZ9nN8WcbcAX934pkd&_nc_ht=scontent.fsub8-1.fna&oh=5780a3112d5fd1fbeaa1266644240f13&oe=5EE6B6E7",
                            "subtitle": "Renyah"
                        }
                    ]
                }
            }
        }
    }
    resp = requests.request("POST", url, json=jsdata, timeout=600)
    logging.info(resp.content)
    return "Success"


def order_kue(outputContexts, fb_sender_id, action):
    list_pesanan = []
    tanggal = datetime.now
    logging.info("JSON Pesanan")
    logging.info(json.dumps(outputContexts))

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
                {'nama': nama_pemesan, 'nomor': nomor_telp, 'alamat': alamat_pemesan, 'kue': pesanan})
            # Konversi variabel jenis kue type list menjadi str
            str_kue = ', '.join(list_pesanan[0]['kue'])
            # tanggal pemesanan dilakukan
            tanggal_format = datetime.now()
            tanggal_pesan = tanggal_format.strftime('%m/%d/%Y')
            id_pesanan = uuid.uuid4().hex[:8]
            sheet = client.open('Pesanan Kue').sheet1
            sheet.append_row([list_pesanan[0]['nama'], list_pesanan[0]
                              ['nomor'], list_pesanan[0]['alamat'], str_kue, tanggal_pesan, id_pesanan])

    return "ok"


def cek_pesanan(outputContexts):

    return "ok"


if __name__ == '__main__':
    app.run()
