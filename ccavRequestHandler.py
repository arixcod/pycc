#!/usr/bin/python

from flask import request, redirect, Flask, render_template, jsonify
from ccavutil import encrypt, decrypt
from ccavResponseHandler import res
from string import Template

app = Flask('ccavRequestHandler')

'''
Please put in the 32-bit alphanumeric key and Access Code provided by CCAvenue.
'''

accessCode = 'AVIP10LH97AS04PISA'
workingKey = '79B8D8AA336EDF95D51C1FA98272E119'






@app.route('/')
def webprint():
    return render_template('dataFrom.htm')



@app.route('/success')
def success():
    return render_template('suc.html')

@app.route('/cancel')
def cancel():
    return render_template('can.html')



@app.route('/ccavResponseHandler', methods=['GET', 'POST'])
def ccavResponseHandler():
    plainText = res(request.form['encResp'])
    return plainText

@app.route('/ccavRequestHandler', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        p_merchant_id = "3751076"
        p_order_id = data['order_id']
        p_currency = "INR"
        p_amount = data['amount']
        p_redirect_url = "http://arixpower.com/ccavResponseHandler"  # Updated URL
        p_cancel_url = "http://arixpower.com/ccavResponseHandler"    # Updated URL

        p_language = 'EN'
        p_billing_name = data.get('billing_name', "")
        p_billing_address = data.get('billing_address', "")
        p_billing_city = data.get('billing_city', "")
        p_billing_state = data.get('billing_state', "")
        p_billing_zip = data.get('billing_zip', "")
        p_billing_country = data.get('billing_country', "")
        p_billing_tel = data.get('billing_tel', "")
        p_billing_email = data.get('billing_email', "")
        p_delivery_name = data.get('delivery_name', "")
        p_delivery_address = data.get('delivery_address', "")
        p_delivery_city = data.get('delivery_city', "")
        p_delivery_state = data.get('delivery_state', "")
        p_delivery_zip = data.get('delivery_zip', "")
        p_delivery_country = data.get('delivery_country', "")
        p_delivery_tel = data.get('delivery_tel', "")
        p_merchant_param1 = data.get('merchant_param1', "")
        p_merchant_param2 = data.get('merchant_param2', "")
        p_merchant_param3 = data.get('merchant_param3', "")
        p_merchant_param4 = data.get('merchant_param4', "")
        p_merchant_param5 = data.get('merchant_param5', "")
        p_promo_code = data.get('promo_code', "")
        p_customer_identifier = data.get('customer_identifier', "")

        merchant_data = (
            'merchant_id=' + p_merchant_id + '&' +
            'order_id=' + p_order_id + '&' +
            'currency=' + p_currency + '&' +
            'amount=' + p_amount + '&' +
            'redirect_url=' + p_redirect_url + '&' +
            'cancel_url=' + p_cancel_url + '&' +
            'language=' + p_language + '&' +
            'billing_name=' + p_billing_name + '&' +
            'billing_address=' + p_billing_address + '&' +
            'billing_city=' + p_billing_city + '&' +
            'billing_state=' + p_billing_state + '&' +
            'billing_zip=' + p_billing_zip + '&' +
            'billing_country=' + p_billing_country + '&' +
            'billing_tel=' + p_billing_tel + '&' +
            'billing_email=' + p_billing_email + '&' +
            'delivery_name=' + p_delivery_name + '&' +
            'delivery_address=' + p_delivery_address + '&' +
            'delivery_city=' + p_delivery_city + '&' +
            'delivery_state=' + p_delivery_state + '&' +
            'delivery_zip=' + p_delivery_zip + '&' +
            'delivery_country=' + p_delivery_country + '&' +
            'delivery_tel=' + p_delivery_tel + '&' +
            'merchant_param1=' + p_merchant_param1 + '&' +
            'merchant_param2=' + p_merchant_param2 + '&' +
            'merchant_param3=' + p_merchant_param3 + '&' +
            'merchant_param4=' + p_merchant_param4 + '&' +
            'merchant_param5=' + p_merchant_param5 + '&' +
            'promo_code=' + p_promo_code + '&' +
            'customer_identifier=' + p_customer_identifier
        )

        encryption = encrypt(merchant_data, workingKey)

        html = '''\
        <html>
        <head>
            <title>Sub-merchant checkout page</title>
            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        </head>
        <body>
        <form id="nonseamless" method="post" name="redirect" action="https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction">
            <input type="hidden" id="encRequest" name="encRequest" value=$encReq>
            <input type="hidden" name="access_code" id="access_code" value=$xscode>
            <script language='javascript'>document.redirect.submit();</script>
        </form>    
        </body>
        </html>
        '''
        fin = Template(html).safe_substitute(encReq=encryption, xscode=accessCode)
        return fin

    return jsonify({'error': 'Invalid input format, JSON expected'}), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=30001)
