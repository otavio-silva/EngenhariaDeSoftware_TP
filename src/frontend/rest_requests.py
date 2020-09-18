import json, requests

#Usuários
'''
Faz requisição para criar usuário
Requisição tipo POST
TODO: campos opcionais 
'''
def create_user_request(username, password):
    data = {"username": username, "password": password}
    req = requests.post('http://localhost:8000/api/users/register', data=data)
    return req

'''
Faz requisição de autenticação de usuário
Requisição tipo POST
'''
def authenticate_user_request(username, password):
    data = {"username": username, "password": password}
    req = requests.post('http://localhost:8000/api/auth', data=data)
    return req

'''
Faz requisição que recupera informações de um usuário
Requisição tipo GET
'''
def get_user_info_request(username, access_token):
    headers = {'Authorization': f'Token {access_token}'}
    req = requests.get('http://localhost:8000/api/users/' + str(username), headers=headers)
    return req


#Mensagens
'''
Faz requisição que envia uma mensagem a um usuário
Requisição tipo POST
'''
def send_message_request(receiver_username, message, access_token):
    headers = {'Authorization': f'Token {access_token}'}
    data = {"username": receiver_username, "message": message}
    req = requests.post('http://localhost:8000/api/messages', data=data, headers=headers)
    return req

'''
Faz requisição que recupera informações sobre uma mensagem
Requisição tipo GET
'''
def get_message_info_request(message_id, access_token):
    headers = {'Authorization': f'Token {access_token}'}
    req = requests.get('http://localhost:8000/api/messages/' + str(message_id), headers=headers)
    return req

'''
Faz requisição que atualiza o estado de uma mensagem para lida ou recebida
Requisição tipo PUT
'''
def update_message_state_request(received, read, message_id, access_token):
    headers = {'Authorization': f'Token {access_token}'}
    data = {'received' : received, 'read': read}
    req = requests.put('http://localhost:8000/api/messages/' + str(message_id), headers=headers, data=data)
    return req




'''
username = "usr"
password = "psw"
req = create_user_request(username, password)
print(req.json())
req = authenticate_user_request(username, password)
print(req.json())
access_token = req.json()['token']
req = get_user_info_request(username, access_token)
print(req.json())
req = send_message_request("usr2", "Mensagem sendo enviada", access_token)
print(req.json())
message_id = req.json()['created_id']
req = get_message_info_request(message_id, access_token)
print(req.json())
req = update_message_state_request(True, False, message_id, access_token)
print(req.json())
#response = requests.get("http://127.0.0.1:5000/api/messages")
#print(response.content)
#print(json.loads(response.content))
'''