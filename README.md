# Sistema de Cadastro de Listas de Tarefas
Aplicação desenvolvida para a empresa FATTO Consultoria e Sistemas.

# Guia de Instalação e Execução da Aplicação de Lista de Tarefas

Este guia fornece instruções para configurar e executar uma aplicação de lista de tarefas em Python, utilizando Flask e SQLite. Vamos passar pela instalação do Python 3.12.3 e do SQLite, configuração do ambiente virtual, e execução da aplicação no terminal.

## Antes de executar a aplicação, verifique se:

1. **O Python 3.12.3 está devidamente instalado e configurado**:
   - Acesse o site oficial do Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **O SQLite está baixado**:
   - No Windows, execute o instalador e selecione a opção "Add Python to PATH" durante a instalação.
   - No macOS e Linux, siga as instruções do instalador para instalar o Python.
  
3. **Flask e outras dependências necessárias para o projeto.**:
   - Execute o comando de python no terminal:
      ```bash
     pip install flask
     ```
4. ** O Configurar o Banco de Dados SQLite**:
   - Será necessário criar o banco de dados `tarefas.db` e a tabela.
   - Certifique-se de incluir os arquivos 

## Executando a Aplicação

Agora que o ambiente está configurado, podemos executar a aplicação.

1. **Iniciar a aplicação**:
   - Com o ambiente virtual ativado, execute o arquivo `app.py`:
     ```bash
     python app.py
     ```

2. **Acessar a aplicação**:
   - Abra o navegador e acesse a URL:
     ```
     http://127.0.0.1:5000
     ```

   A aplicação deve estar rodando e pronta para uso.

## Estrutura da Aplicação

- `app.py`: Código principal da aplicação.
- `tarefas.db`: Banco de dados SQLite.
- `templates/`: Contém os arquivos HTML da interface.
- `static/`: Contém arquivos CSS e JavaScript para estilização e funcionalidades.

## Funcionalidades

- **Adicionar Tarefa**: Criar novas tarefas com informações como nome, custo, data limite e ordem.
- **Editar Tarefa**: Atualizar informações das tarefas existentes.
- **Excluir Tarefa**: Remover tarefas da lista.
- **Ordenação de Tarefas**: Ajustar a ordem das tarefas para organização.

## Problemas Comuns

- **Erro de Banco de Dados**: Se houver algum erro relacionado ao banco de dados, tente apagar o arquivo `tarefas.db` e recriar a tabela usando o passo de configuração do banco de dados.
- **Dependências Faltando**: Certifique-se de que todas as bibliotecas foram instaladas corretamente.

## Créditos

Desenvolvido por [Yasmin Cibreiros Chagas](https://github.com/yasminccs).
