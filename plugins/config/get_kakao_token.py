import requests

client_id = 'd14711abf81502b80df3ebb317d0797c'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'FWn9YFLnmj-RdToSjL1VnF6qJ5ouCwJa-zE7kYPfDMg54Lf_7YnRgAAAAAQKPCQgAAABkrnxdR4SmUam6ZdnFg'

token_url = 'https://kauth.kakao.com/oauth/token'
data = {
    'grant_type' : 'authorization_code',
    'client_id' : client_id,
    'redirect_uri' : redirect_uri,
    'code' : authorize_code
}

response = requests.post(token_url, data=data)
tokens = response.json()
print(tokens)