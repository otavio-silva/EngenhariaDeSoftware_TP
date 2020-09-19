- Como rodar o frontend ?
  - python user_api.py
  - Este comando começará o servidor do lado do frontend que serve para receber mensagens e requisições de confirmação, tudo feito por uma API REST.
  - E começará a interface gráfica. 
  
- Como testar o frontend ?
  - É possível testar usando a interface, mas só se pode enviar mensagens para usuários cadastrados no back end. Ou seja, deve-se criar esses usuários.
  Essa criação pode ser feita pela interface ou pela API do back end.
    - Exemplo com requisições úteis (outras podem ser encontradas no arquivo rest_requests.py):
    ```
    username = "usr"
    password = "psw"
    req = create_user_request(username, password)
    print(req.json())
    req = authenticate_user_request(username, password)
    print(req.json())
    access_token = req.json()['token']
    req = get_user_info_request(username, access_token)
    ```
  - Usando a interface e as requisições é possível testar várias funcionalidades.
  - Outro caso de teste é o recebimento de mensagens. Para isso é necessário enviar uma requisição ao servidor Flask.
    -Note que é possível criar um novo contato (aba de conversa, não um contato mesmo) recebendo uma mensagem desse contato, como no WhatsApp.
      -Ou seja, se alguém te mandar uma mensagem, o contato dele aparecerá na sua aba.
    -Exemplo:
    ```
    import requests
    data = {'id': 123,'sender': 'buhbuh54', 'content': 'teste sucesso', 'created_at': 'data'}
    response = requests.post("http://127.0.0.1:5000/api/messages", data=data)
    print(response.json())
    ```

- Como se comunicar com o frontend ?
  - Por meio de requisições REST: (Por enquanto localmente)
    - Requisição para enviar mensagem: POST
    
      http://127.0.0.1:5000/api/messages
      
      data:
      
        {'id': "id da mensagem", 'sender': "username", 'content': "Conteúdo da mensagem", 'created_at': "Data de criação no formato do backend"}
        
      -Exemplo: 
              
                data = {'id': 123,'sender': 'new_user', 'content': 'teste sucesso', 'created_at': 'data'}
      
                response = requests.post("http://127.0.0.1:5000/api/messages", data=data)
    
