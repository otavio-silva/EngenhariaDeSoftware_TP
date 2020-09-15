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
#def get_user_info_request(id, access_token):


#Mensagens

username = "gabrielll"
password = "senha"
req = create_user_request(username, password)
print(req.json())
req = authenticate_user_request(username, password)
print(req.json())
#response = requests.get("http://127.0.0.1:5000/api/messages")
#print(response.content)
#print(json.loads(response.content))
