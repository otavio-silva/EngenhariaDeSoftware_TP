import requests
data = {'id': 123,'sender': 'buhbuh54', 'content': 'teste sucesso', 'created_at': 'data'}
response = requests.post("http://127.0.0.1:5000/api/messages", data=data)
print(response.json())