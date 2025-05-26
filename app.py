from flask import Flask, request, jsonify
from curl_cffi import requests as curl_requests
from seleniumbase import SB

app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello, Flaskie v2!'

@app.route('/curl_cffi/get_html')
def get_html_using_curl_cffi():
    is_raw = request.args.get('raw', 'false').lower() == 'true'
    url_param = request.args.get('url')
    if not url_param:
        return "No URL provided", 400
    
    try:
        r = curl_requests.get(url_param, impersonate="chrome")
        if is_raw:
            return r.text, 200, {'Content-Type': 'text/plain'}
        else:
            return jsonify({
                'url': r.url,
                'status_code': r.status_code,
                'headers': dict(r.headers),
                'content': r.text
            }), 200

    except Exception as e:
        return f"Error fetching URL: {str(e)}", 500
    

@app.route('/seleniumbase/get_html')
def get_html_using_seleniumbase():
    is_raw = request.args.get('raw', 'false').lower() == 'true'
    url_param = request.args.get('url')
    if not url_param:
        return "No URL provided", 400
    
    try:
        with SB() as sb:
            sb.open(url_param)
            html_content = sb.get_page_source()
            if is_raw:
                return html_content, 200, {'Content-Type': 'text/plain'}
            else:
                return jsonify({
                    'url': sb.get_current_url(),
                    'title': sb.get_title(),
                    'content': html_content
                }), 200

    except Exception as e:
        return f"Error fetching URL: {str(e)}", 500