import requests
from rest_requests import *
#data = {'id': 123,'sender': 'pop', 'content': 'teste sucesso', 'created_at': 'data'}
#response = requests.post("http://127.0.0.1:5000/api/messages", data=data)
#print(response.json())

username = "pop"
password = "pop"
#req = create_user_request(username, password)
#print(req.json())
req = authenticate_user_request(username, password)
print(req.json())
access_token = req.json()['token']
#req = keep_active_request(5000, access_token)
#print(req)
#req = get_user_info_request(username, access_token)
#print(req.json())
req = send_message_request("usr", "Mensagem sendo enviada", access_token)
print(req.json())
"""
message_id = req.json()['created_id']
req = get_message_info_request(message_id, access_token)
print(req.json())
req = update_message_state_request(True, False, message_id, access_token)
print(req.json())
req = keep_active_request(5000, access_token)
print(req)
#response = requests.get("http://127.0.0.1:5000/api/messages")
#print(response.content)
#print(json.loads(response.content))
"""