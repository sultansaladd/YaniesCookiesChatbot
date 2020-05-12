import json
import logging
import gspread

from oauth2client.service_account import ServiceAccountCredentials


from flask import Flask, request

app = Flask(__name__)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

client = gspread.authorize(creds)

access_token = 'EAAkc0ZCgiBl8BAAfzpD3IHVJr624w7aTb76rhptu1x5zEZC4EOnifQMjoXsgMm3RsTGT068A4bY38sDOVL05xFZCgyYwZBf75R6xW6UaWid5MH5H2XWYB1mQD5x0QUgzak4LfYXDgOl8V5CNzNZBCvQywDZAQVg0W8NR77AMDlaxgbJ0wBwRX6 '

logging.basicConfig(level=logging.INFO)


@app.route('/pesankue', methods=['GET', 'POST'])
def pesankue():
    userReq = request.get_json(force=True)
    outputContexts = userReq.get('queryResult').get('outputContexts')
    action = userReq.get('queryResult').get('action')

    fb_sender_id = '2919206894815271'
    for eachContext in outputContexts:
        # fb_sender_id = eachContext.get('parameters', {}).get(
        #     'facebook_sender_id') if fb_sender_id is None else fb_sender_id

        if 'contexts/input-phone' in eachContext['name']:
            dfinput = eachContext
            nama_pemesan = dfinput.get('parameters').get('name.original')
            nomor_telp = dfinput.get('parameters').get('phone.original')
            alamat_pemesan = dfinput.get('parameters').get('address.original')

    logging.info(json.dumps(outputContexts))
    logging.info(action)
    logging.info(nama_pemesan)
    logging.info(nomor_telp)
    logging.info(alamat_pemesan)
    logging.info(fb_sender_id)

    return "Pesanan Masuk"

    # if action == 'order.confirm':
    # logging.info(action)
    # return konfirmasi_pesanan(fb_sender_id)


# def konfirmasi_pesanan(fb_sender_id):
#     sheet = client.open('Pesanan Kue').sheet1
#     data = sheet.get_all_records()
#     print(json.dumps(data))


if __name__ == '__main__':
    app.run()
