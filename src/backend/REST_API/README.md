# Backend em Django

## Instalações

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

## Uso

Faça as iniciações necessárias do banco de dados:

```bash
python manage.py makemigrations chat 
python manage.py makemigrations message
python manage.py makemigrations user
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver
```

## Endpoints (temporários)

### Autenticação

(Criar usuário antes)

O mecanismo de autenticação é via `token` único de cada usuário, assim, toda requisição ao servidor que é necessário login, o `token` deve ser passado no cabeçalho.

#### Obtenção de token de acesso

É necessário que o usuário informe sua senha e username, se a autenticação ocorrer sem problemas, um `token` de acesso será retornado.

- [POST] http://localhost:8000/api/auth/ com o seguinte corpo json:
    ```json
        {
            "username": "your_username",
            "password": "your_password"
        }
    ```
    - Resultado esperado:
        - Se autenticação ocorreu corretamente, um json com o `token` de acesso, exemplo:
            ```json
            {
                "token": "617745842d028b2b9cd36c7d189ff876d192b3f2"
            }
            ```
        - Se a autenticação falhou:
            ```json
            {
                "non_field_errors": [
                    "Unable to log in with provided credentials."
                ]
            }
            ```

Exemplo em python:

```python
import requests

credentials = {
	"username": "your_username",
	"password": "your_password"
}

req = requests.post('http://localhost:8000/api/auth/', data=credentials)

access_token = req.json()['token']
```

> Obs.: O token de acesso é necessário em toda requisição que precisa autenticação.

### Usuários

- Criação: [POST] http://localhost:8000/api/users/register  com o seguinte corpo json obrigatório:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

    - Outros campos opcionais:
        - first_name: Primeiro nome do usuário
        - last_name: Sobrenome do usuário
        - ip_address: IP público do usuário
    
    - Resposta esperada: 
        - Json representando o usuário criado
        - Erros de criação do usuário

    - Exemplo de uso em python:
    ```python
    import requests

    #criação de usuário apenas com username e senha
    data = {'username': 'your_username', 'password': 'your_password'}
    req = requests.post('http://localhost:8000/api/users/register', data=data)

    print(req.json())
    ``` 
- Recuperar informação de um usuário (**requer token de acesso**):
    - [GET] http://localhost:8000/api/users/{user_id}
    - Saída esperada:
        - Json com a informação do usuário ou de erro.
    - Exemplo:
        ```python
        import requests

        #caso não tenha o token de acesso armazenado em algum lugar
        credentials = {'username': 'your_username', 'password': 'your_password'}
        req = requests.post('http://localhost:8000/api/auth/', data=credentials)
        access_token = req.json()['token']

        #envie o token de acesso no cabeçalho da requisição
        headers = {'Authorization': f'Token {access_token}'}

        #recuperar info. do usuário de ID 1
        req = requests.get('http://localhost:8000/api/users/1', headers=headers)
        user_info = req.json()
        
        print(user_info)
        ```

