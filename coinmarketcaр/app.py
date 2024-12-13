from flask import Flask, render_template, request, jsonify
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

app = Flask(__name__)

API_KEY = '1d7b4aaa-fa48-4ad8-9551-383cff16e77b'

def get_crypto_data(symbol, currency):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol.upper(),
        'convert': currency.upper()
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        if 'data' in data and symbol.upper() in data['data']:
            crypto_data = data['data'][symbol.upper()]
            quote_data = crypto_data['quote'][currency.upper()]

            price = quote_data['price']
            market_cap = quote_data['market_cap']
            volume_24h = quote_data['volume_24h']
            percent_change_1h = quote_data['percent_change_1h']
            percent_change_24h = quote_data['percent_change_24h']
            percent_change_7d = quote_data['percent_change_7d']
            circulating_supply = crypto_data['circulating_supply']
            total_supply = crypto_data['total_supply']
            max_supply = crypto_data['max_supply']

            result = {
                'symbol': symbol.upper(),
                'price': price,
                'market_cap': market_cap,
                'volume_24h': volume_24h,
                'percent_change_1h': percent_change_1h,
                'percent_change_24h': percent_change_24h,
                'percent_change_7d': percent_change_7d,
                'circulating_supply': circulating_supply,
                'total_supply': total_supply,
                'max_supply': max_supply,
            }

            return result
        else:
            return {'error': 'Криптовалюта не найдена'}

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_crypto', methods=['POST'])
def get_crypto():
    symbol = request.form.get('symbol')
    currency = request.form.get('currency')
    crypto_info = get_crypto_data(symbol, currency)

    if 'error' in crypto_info:
        return jsonify({'error': crypto_info['error']})
    else:
        return jsonify(crypto_info)

if __name__ == '__main__':
    app.run(debug=True)