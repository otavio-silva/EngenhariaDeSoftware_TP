# Backend em Django

## Instalações

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

## Uso

Faça as migrações necessários para o banco de dados:

```bash
python manage.py makemigrations chat 
python manage.py makemigrations message
python manage.py migrate
```

Crie um superusuário:

```bash
python manage.py createsuperuser
```

Inicie o servidor:

```bash
python manage.py runserver
```

Acesse a página de administração e crie alguns objetos, em http://localhost:8000/admin

## Endpoints (temporários)

Mensagens:
- Listar todas: http://localhost:8000/api/messages/


