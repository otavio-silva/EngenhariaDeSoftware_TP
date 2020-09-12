# Engenharia De Software - Trabalho Prático
Repositório para o trabalho prático da disciplina Engenharia De Software (DCC603).

## Spring Planing

### Histórias de Usuário

- História 1 : "Eu como usuário desejo fazer um login com usuário e senha."
- História 2 : "Eu como usuário desejo adicionar um contato."
- História 3 : "Eu como usuário desejo enviar e receber mensagens."
- História 4 : "Eu como usuário quero que minhas mensagens sejam salvas."
- História 5 : "O usuário admin deve ser capaz de excluir usuários."
- História 6 : "Eu como usuário desejo receber a confirmação de leitura. "
- História 7 (bônus): "Eu como usuário desejo criar um grupo e enviar mensagens à vários usuários. "

### Tasks 

- (Inicial) Montar um sistema que envia/consome Rest Requests para o frontend. Sistema: (.NET Core) 
    - Responsáveis: Otávio, Luiz, Elves
    - Meta: 21/08
- (Inicial) Montar um sistema que envia/consome Rest Requests para o backend. Sistema: (Python) 
    - Responsáveis: Evandro, Gabriel
    - Meta: 21/08
- (Inicial) Montar as telas iniciais do aplicativo
    - Responsáveis: Evandro, Gabriel
    - Meta: 21/08
    - Concluído : 27/08 (Evandro)

- (História 1) Montar uma tela de Login que produza o Request para login. O mesmo para o cadastro. 
    - Responsáveis: Evandro, Gabriel
- (História 1) Montar a API Rest para login e cadastro. 
    - Responsáveis: Otávio, Luiz, Elves
- (História 2) Montar a tela para adicionar o contato
    - Responsáveis: Evandro, Gabriel
- (História 3) Montar uma tela para escrever uma mensagem e um botão para enviá-la.
    - Responsáveis: Evandro, Gabriel
    - Concluído : 01/08 (Evandro)
- (História 3) Montar uma tela para ler as mensagens anteriores logo acima do painel de envio.
    - Responsáveis: Evandro, Gabriel
    - Concluído : 11/09 (Evandro)
- (História 3 e 6) Montar a API Rest para guardar e enviar as mensagens assim que o destinatário responder à um ping e confirmar o recebimento. 
    - Responsáveis: Otávio, Luiz, Elves
- (História 4) Garantir que as mensagens sejam salvas localmente (cache das N últimas)
    - Responsáveis: Evandro, Gabriel
    - Em progresso : 11/09 (Evandro)
- (História 4) Garantir que as mensagens sejam salvas no banco de dados
    - Responsáveis: Otávio, Luiz, Elves
- (História 5) Adicionar botão de excluir usuário do sistema
    - Responsáveis: Evandro, Gabriel
- (História 5) Filtrar requisição "DELETE" e permitir apenas usuários do tipo admin.  
    - Responsáveis: Otávio, Luiz, Elves
- (História 6) Mudar o ícone da mensagem para o "double-tick" indicando confirmação de envio.
    - Responsáveis: Evandro, Gabriel
- (História 7) Criar uma tela de mensagens que mostre o nome de quem enviou cada mensagem
    - Responsáveis: Evandro, Gabriel
    - Concluído : 11/09 (Evandro)
- (História 7) Reaproveitar as tabelas de conversa e adaptá-las para um grupo. 
    - Responsáveis: Otávio, Luiz, Elves
