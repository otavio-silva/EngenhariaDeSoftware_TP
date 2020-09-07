# Backend: Rest Api

## Instalações

É necessário adicionar as seguintes bibliotecas para que seja possível manipulação do banco de dados, embora atualmente use a opção `InMemory`, ou seja, sem persistência:

```bash
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.InMemory
```

## Uso

O seguinte comando executa a api rest:

```bash
dotnet run
```

A api deve executar no endereço `https://localhost:5001/api/{modelo}`. Onde modelo é aquele que se deseja realizar operações CRUD.




