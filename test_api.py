import urllib.request, urllib.parse, json, time

base_url = 'http://127.0.0.1:8000/api'
username = f'test_user_{int(time.time())}'

# 1. Register
req = urllib.request.Request(f'{base_url}/auth/register', method='POST', 
                             data=json.dumps({'username':username,'email':f'{username}@test.com','password':'password123'}).encode('utf-8'), 
                             headers={'Content-Type': 'application/json'})
urllib.request.urlopen(req)

# 2. Login
data = urllib.parse.urlencode({'username': username, 'password': 'password123'}).encode('utf-8')
req = urllib.request.Request(f'{base_url}/auth/login', method='POST', data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
res = urllib.request.urlopen(req)
token = json.loads(res.read())['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def get_req(endpoint):
    req = urllib.request.Request(f'{base_url}/{endpoint}', method='GET', headers=headers)
    return json.loads(urllib.request.urlopen(req).read())

def post_req(endpoint, data):
    req = urllib.request.Request(f'{base_url}/{endpoint}', method='POST', data=json.dumps(data).encode('utf-8'), headers=headers)
    return json.loads(urllib.request.urlopen(req).read())

def del_req(endpoint):
    req = urllib.request.Request(f'{base_url}/{endpoint}', method='DELETE', headers=headers)
    return json.loads(urllib.request.urlopen(req).read())

# Scans
print('Scanning URLs...')
post_req('scan/url', {'url': 'https://www.google.com'})
url_phish = post_req('scan/url', {'url': 'http://paypal-login-security.example.com/verify-account'})
print('Phishing URL Risk:', url_phish['risk_level'], 'Indicators:', url_phish['indicators'])

print('Scanning Messages...')
post_req('scan/message', {'message': 'Hi, are we still meeting at 5 PM today?'})
msg_scam = post_req('scan/message', {'message': 'URGENT! Your bank account will be blocked today. Verify your account immediately using this link and enter your OTP.'})
print('Scam Message Risk:', msg_scam['risk_level'], 'Indicators:', msg_scam['indicators'])

# Verify History
history_urls = get_req('history/urls')
history_msgs = get_req('history/messages')
print('URL History Count:', history_urls['total'])
print('Msg History Count:', history_msgs['total'])
assert history_urls['total'] == 2
assert history_msgs['total'] == 2

# Delete One Record
print('Deleting one URL record...')
first_id = history_urls['items'][0]['id']
del_req(f'history/urls/{first_id}')
history_urls = get_req('history/urls')
assert history_urls['total'] == 1

# Delete All
print('Deleting all history...')
del_req('history/urls')
del_req('history/messages')
history_urls = get_req('history/urls')
history_msgs = get_req('history/messages')
assert history_urls['total'] == 0
assert history_msgs['total'] == 0

print('ALL TESTS PASSED')
