- Como rodar o frontend ?
  - python user_api.py
  - Este comando começará o servidor do lado do frontend que serve para receber mensagens e requisições de confirmação, tudo feito por uma API REST.
  - E começará a interface gráfica. 
  

- Como se comunicar com o frontend ?
  - Por meio de requisições REST: (Por enquanto localmente)
    - Requisição para enviar mensagem: POST
    
      http://127.0.0.1:5000/api/messages
      
      data:
      
        {'id': "id da mensagem", 'sender': "username", 'content': "Conteúdo da mensagem", 'created_at': "Data de criação no formato do backend"}
        
      -Exemplo: data = {'id': 123,'sender': 'new_user', 'content': 'teste sucesso', 'created_at': 'data'}
      
                response = requests.post("http://127.0.0.1:5000/api/messages", data=data)
    
