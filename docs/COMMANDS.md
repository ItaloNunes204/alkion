# Alkion — Guia de Comandos

> Referência completa de comandos para desenvolvimento, execução e versionamento do projeto.

---

## Sumário

- [Backend](#backend)
- [Frontend Web](#frontend-web)
- [Frontend App](#frontend-app)
- [Frontend Desktop](#frontend-desktop)
- [Docker](#docker)
- [Banco de Dados / Migrations](#banco-de-dados--migrations)
- [Git — Regras e Comandos](#git--regras-e-comandos)

---

## Backend

> Terminal: **Backend (Flask)** — já abre com `.venv` ativo em `C:\projetos\alkion\backend`

### Ambiente Virtual

```cmd
# Ativar o ambiente virtual (necessário sempre que abrir um CMD comum)
.venv\Scripts\activate.bat

# Desativar o ambiente virtual
deactivate

# Instalar todas as dependências do requirements.txt
pip install -r requirements.txt

# Adicionar nova biblioteca e atualizar o requirements.txt
pip install nome-da-biblioteca
pip freeze > requirements.txt
```

### Rodando o servidor

```cmd
# Iniciar o servidor em modo desenvolvimento
python run.py

# O servidor sobe em:
# http://localhost:5000
# Documentação Swagger: http://localhost:5000/docs
```

### Testes

```cmd
# Rodar todos os testes
pytest

# Rodar testes com detalhes
pytest -v

# Rodar testes com cobertura de código
pytest --cov=app

# Rodar um arquivo de teste específico
pytest tests/unit/test_auth.py
```

---

## Banco de Dados / Migrations

> As migrations controlam as alterações no banco de dados ao longo do tempo.
> Sempre que você alterar ou criar um Model, precisa gerar e aplicar uma migration.

```cmd
# 1. Inicializar o sistema de migrations (apenas uma vez no projeto)
flask --app run:app db init

# 2. Gerar uma nova migration baseada nas mudanças dos Models
# Substitua "descricao" por algo que descreva o que mudou
flask --app run:app db migrate -m "create users table"
flask --app run:app db migrate -m "add email to companies"
flask --app run:app db migrate -m "create plans table"

# 3. Aplicar as migrations pendentes ao banco de dados
flask --app run:app db upgrade

# 4. Reverter a última migration aplicada
flask --app run:app db downgrade

# 5. Ver o histórico de migrations
flask --app run:app db history

# 6. Ver a migration atual aplicada
flask --app run:app db current
```

### Fluxo correto ao criar/alterar um Model

```
1. Edite ou crie o arquivo models.py do módulo
2. flask --app run:app db migrate -m "descricao da mudanca"
3. Revise o arquivo gerado em migrations/versions/
4. flask --app run:app db upgrade
```

---

## Docker

> Gerencia os containers do PostgreSQL e Redis.
> O Docker Desktop precisa estar aberto para os comandos funcionarem.

```cmd
# Subir todos os containers em background
docker compose up -d

# Parar todos os containers (mantém os dados)
docker compose stop

# Parar e remover os containers (mantém os dados nos volumes)
docker compose down

# Parar, remover containers E apagar todos os dados (cuidado!)
docker compose down -v

# Ver status dos containers
docker compose ps

# Ver logs do PostgreSQL
docker logs alkion_postgres

# Ver logs do Redis
docker logs alkion_redis

# Acessar o banco de dados pelo terminal
docker exec -it alkion_postgres psql -U alkion -d alkion_dev

# Comandos úteis dentro do psql:
# \dt          — listar todas as tabelas
# \du          — listar usuários
# \dx          — listar extensões instaladas
# \q           — sair do psql
# SELECT * FROM plans;  — exemplo de query
```

---

## Frontend Web

> Terminal: **Frontend Web** — abre em `C:\projetos\alkion\frontend-web`

```cmd
# Instalar dependências (apenas na primeira vez ou após mudanças no package.json)
npm install

# Iniciar servidor de desenvolvimento
npm run dev

# O servidor sobe em:
# http://localhost:5173

# Build para produção
npm run build

# Visualizar o build de produção localmente
npm run preview

# Verificar erros de código (lint)
npm run lint
```

---

## Frontend App

> Terminal: **Frontend App** — abre em `C:\projetos\alkion\frontend-app`

```cmd
# Instalar dependências
npm install

# Iniciar o servidor de desenvolvimento Expo
npx expo start

# Rodar no Android
npx expo run:android

# Rodar no iOS (apenas macOS)
npx expo run:ios

# Rodar no navegador
npx expo start --web

# Limpar cache do Expo
npx expo start --clear
```

---

## Frontend Desktop

> Terminal: **Frontend Desktop** — abre em `C:\projetos\alkion\frontend-desktop`

```cmd
# Instalar dependências
npm install

# Iniciar em modo desenvolvimento
npm run dev

# Build para Windows
npm run build:win

# Build para macOS
npm run build:mac

# Build para Linux
npm run build:linux
```

---

## Git — Regras e Comandos

> Terminal: **Git** — abre em `C:\projetos\alkion`

### Padrão de Commits (Conventional Commits)

Todo commit deve seguir o formato:
```
tipo(escopo): descricao em letras minusculas
```

**Tipos disponíveis:**

| Tipo | Quando usar | Exemplo |
|---|---|---|
| `feat` | Nova funcionalidade | `feat(auth): adiciona endpoint de login` |
| `fix` | Correção de bug | `fix(plans): corrige calculo de preco anual` |
| `docs` | Documentação | `docs: atualiza guia de comandos` |
| `style` | Formatação, sem lógica | `style(home): ajusta espacamento dos botoes` |
| `refactor` | Refatoração sem nova feature | `refactor(auth): simplifica verificacao de token` |
| `test` | Adicionando testes | `test(plans): adiciona testes de listagem` |
| `chore` | Configs, dependências | `chore: atualiza dependencias do backend` |
| `perf` | Melhoria de performance | `perf(inventory): otimiza query de estoque` |

> Commits fora deste padrão serão **bloqueados automaticamente** pelo Husky.

### Comandos do dia a dia

```cmd
# Ver status dos arquivos modificados
git status

# Adicionar todos os arquivos modificados para o commit
git add .

# Adicionar um arquivo específico
git add backend/app/modules/plans/routes.py

# Fazer um commit
git commit -m "feat(plans): adiciona listagem de planos"

# Enviar commits para o GitHub
git push

# Buscar atualizações do GitHub sem aplicar
git fetch

# Buscar e aplicar atualizações do GitHub
git pull

# Ver histórico de commits (resumido)
git log --oneline

# Ver histórico com gráfico de branches
git log --oneline --graph --all
```

### Trabalhando com Branches

```cmd
# Criar uma nova branch e já entrar nela
git checkout -b feat/modulo-auth

# Trocar de branch
git checkout main

# Ver todas as branches
git branch

# Enviar uma nova branch para o GitHub
git push -u origin feat/modulo-auth

# Fazer merge da branch atual na main
git checkout main
git merge feat/modulo-auth

# Deletar uma branch local após o merge
git branch -d feat/modulo-auth
```

### Desfazendo coisas

```cmd
# Descartar mudanças em um arquivo (volta ao último commit)
git checkout -- nome-do-arquivo.py

# Descartar TODAS as mudanças locais (cuidado!)
git checkout .

# Remover arquivos novos não rastreados
git clean -fd

# Desfazer o último commit (mantém as mudanças)
git reset --soft HEAD~1

# Ver diferença entre arquivos modificados
git diff
```

### Convenção de nomes de branches

```
feat/nome-da-funcionalidade     — nova funcionalidade
fix/descricao-do-bug            — correção de bug
docs/o-que-foi-documentado      — documentação
refactor/o-que-foi-refatorado   — refatoração
chore/o-que-foi-configurado     — configurações
```

**Exemplos:**
```
feat/modulo-auth
feat/tela-de-planos
fix/conexao-banco
docs/guia-de-comandos
chore/configuracao-docker
```

---

## Ordem de inicialização do ambiente

Siga esta ordem toda vez que for trabalhar no projeto:

```
1. Abrir o Docker Desktop e aguardar o engine iniciar
2. Abrir o VS Code na pasta C:\projetos\alkion
3. Abrir terminal Git → docker compose up -d
4. Abrir terminal Backend → python run.py
5. Abrir terminal Frontend Web → npm run dev
6. Acessar http://localhost:5173 no navegador
7. Acessar http://localhost:5000/docs para ver a API
```

---

*Documento mantido pela equipe Alkion.*
