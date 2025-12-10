# API Web Biblioteca 📚

Uma API REST para gerenciamento de livros desenvolvida com **TypeScript**, **Express** e **TypeORM**.

## Características

- ✅ CRUD completo de livros
- ✅ Banco de dados SQLite
- ✅ Validação de dados
- ✅ Tratamento de erros robusto
- ✅ Estrutura em camadas (Controllers, Services, Repositories)
- ✅ TypeScript com tipagem forte

## Pré-requisitos

- Node.js 16+ 
- npm ou yarn

## Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/llooizaq13/API-Web-Biblioteca.git
cd API-Web-Biblioteca
```

2. **Instale as dependências:**
```bash
npm install
```

3. **Execute o servidor:**
```bash
npm run dev
```

O servidor iniciará em `http://localhost:3000`

## Scripts Disponíveis

| Comando | Descrição |
|---------|-----------|
| `npm run dev` | Inicia o servidor em modo desenvolvimento com hot-reload |
| `npm start` | Inicia o servidor em modo produção |
| `npm run typeorm` | Executa comandos do TypeORM |

## Estrutura do Projeto

```
src/
├── config/
│   └── database.ts           # Configuração do TypeORM e SQLite
├── entities/
│   └── Livro.ts              # Entidade/Modelo do Livro
├── repositories/
│   └── LivroRepository.ts     # Camada de acesso a dados
├── controllers/
│   └── LivroController.ts     # Controladores da API
├── routes/
│   └── livroRoutes.ts         # Definição das rotas
└── server.ts                  # Ponto de entrada da aplicação
```

## Endpoints da API

### Base URL
```
http://localhost:3000/api/livros
```

### 1. Criar um novo livro
**POST** `/api/livros`

**Request Body:**
```json
{
  "titulo": "Memórias de um Sargento de Milícias",
  "autor": "Manuel Antônio de Almeida",
  "isbn": "9788535914565",
  "anoPublicacao": 1852,
  "disponivel": true
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "titulo": "Memórias de um Sargento de Milícias",
  "autor": "Manuel Antônio de Almeida",
  "isbn": "9788535914565",
  "anoPublicacao": 1852,
  "disponivel": true
}
```

### 2. Listar todos os livros
**GET** `/api/livros`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "titulo": "Memórias de um Sargento de Milícias",
    "autor": "Manuel Antônio de Almeida",
    "isbn": "9788535914565",
    "anoPublicacao": 1852,
    "disponivel": true
  },
  {
    "id": 2,
    "titulo": "Vidas Secas",
    "autor": "Graciliano Ramos",
    "isbn": "9788508097679",
    "anoPublicacao": 1938,
    "disponivel": true
  }
]
```

### 3. Buscar livro por ID
**GET** `/api/livros/:id`

**Response (200 OK):**
```json
{
  "id": 1,
  "titulo": "Memórias de um Sargento de Milícias",
  "autor": "Manuel Antônio de Almeida",
  "isbn": "9788535914565",
  "anoPublicacao": 1852,
  "disponivel": true
}
```

### 4. Atualizar um livro
**PUT** `/api/livros/:id`

**Request Body:**
```json
{
  "disponivel": false
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "titulo": "Memórias de um Sargento de Milícias",
  "autor": "Manuel Antônio de Almeida",
  "isbn": "9788535914565",
  "anoPublicacao": 1852,
  "disponivel": false
}
```

### 5. Deletar um livro
**DELETE** `/api/livros/:id`

**Response (204 No Content)**

## Validações

- **Título**: Obrigatório, máximo 255 caracteres
- **Autor**: Obrigatório, máximo 150 caracteres
- **ISBN**: Obrigatório, máximo 20 caracteres, deve ser único
- **Ano de Publicação**: Obrigatório, deve ser um número inteiro
- **Disponível**: Opcional, padrão é `true`

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 201 | Livro criado com sucesso |
| 200 | Requisição bem-sucedida |
| 204 | Livro deletado com sucesso (sem conteúdo) |
| 400 | Erro de validação - dados inválidos |
| 404 | Livro não encontrado |
| 409 | Conflito - ISBN já cadastrado |
| 500 | Erro interno do servidor |

## Exemplos de Uso

### Usando cURL

**Criar um livro:**
```bash
curl -X POST http://localhost:3000/api/livros \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "O Cortiço",
    "autor": "Aluísio Azevedo",
    "isbn": "9788508078142",
    "anoPublicacao": 1890
  }'
```

**Listar todos:**
```bash
curl -X GET http://localhost:3000/api/livros
```

**Buscar por ID:**
```bash
curl -X GET http://localhost:3000/api/livros/1
```

**Atualizar:**
```bash
curl -X PUT http://localhost:3000/api/livros/1 \
  -H "Content-Type: application/json" \
  -d '{"disponivel": false}'
```

**Deletar:**
```bash
curl -X DELETE http://localhost:3000/api/livros/1
```

### Usando Postman ou Insomnia

1. Importe os endpoints acima como uma coleção
2. Configure as variáveis de ambiente:
   - `BASE_URL`: `http://localhost:3000/api/livros`
3. Execute as requisições

## Banco de Dados

A aplicação utiliza **SQLite** com o arquivo `biblioteca.sqlite` criado automaticamente na raiz do projeto.

### Estrutura da Tabela `livros`

| Coluna | Tipo | Restrições |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT |
| titulo | VARCHAR(255) | NOT NULL |
| autor | VARCHAR(150) | NOT NULL |
| isbn | VARCHAR(20) | NOT NULL, UNIQUE |
| anoPublicacao | INTEGER | NOT NULL |
| disponivel | BOOLEAN | DEFAULT TRUE |

## Tecnologias Utilizadas

- **TypeScript** - Linguagem tipada para JavaScript
- **Express** - Framework web minimalista
- **TypeORM** - ORM para TypeScript/JavaScript
- **SQLite** - Banco de dados leve e embutido
- **ts-node** - Executor de TypeScript para Node.js

## Desenvolvimento

### Instalação de dependências de desenvolvimento
```bash
npm install
```

### Compilar TypeScript
```bash
npx tsc
```

### Estrutura de erros

A aplicação retorna erros estruturados:

```json
{
  "mensagem": "Descrição do erro",
  "erro": "Detalhes técnicos (apenas em desenvolvimento)"
}
```

## Licença

ISC

## Autor

Desenvolvido por Maria Luiza Cavalcanti (llooizaq13)

## Suporte

Para reportar problemas ou sugerir melhorias, basta mandar uma mensagemzinha para papear.
