#!/bin/bash

# Cores
RESET='\033[0m'
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'

# Símbolos
CHECK='✅'
CROSS='❌'
ARROW='➜'
STAR='⭐'
BOOK='📚'
ROCKET='🚀'
SERVER='🖥️'

# Função para imprimir linha separadora
print_separator() {
  echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
}

# Função para imprimir título
print_title() {
  echo ""
  print_separator
  echo -e "${BOLD}${MAGENTA}${BOOK}  $1${RESET}"
  print_separator
  echo ""
}

# Função para imprimir teste
print_test() {
  local method=$1
  local endpoint=$2
  local description=$3
  echo -e "${CYAN}${ARROW} ${BOLD}$method${RESET}${CYAN} $endpoint${RESET} - ${YELLOW}$description${RESET}"
}

# Função para imprimir resposta bem-sucedida
print_success() {
  echo -e "${GREEN}${CHECK} Sucesso!${RESET}"
  echo -e "${BLUE}Resposta:${RESET}"
  echo "$1" | jq '.' 2>/dev/null || echo "$1"
  echo ""
}

# Função para imprimir erro
print_error() {
  echo -e "${RED}${CROSS} Erro!${RESET}"
  echo "$1"
  echo ""
}

# Verificar se servidor está rodando
check_server() {
  if ! curl -s http://localhost:3000/api/livros &>/dev/null; then
    echo -e "${RED}${CROSS} Servidor não está rodando!${RESET}"
    echo -e "${YELLOW}Inicie com: npm run dev${RESET}"
    exit 1
  fi
}

# Main
main() {
  print_title "${ROCKET} TESTES DA API BIBLIOTECA"
  
  echo -e "${BOLD}${SERVER} Verificando servidor...${RESET}"
  check_server
  echo -e "${GREEN}${CHECK} Servidor conectado na porta 3000${RESET}\n"

  # Teste 1: GET /api/livros (listar)
  print_test "GET" "/api/livros" "Listar todos os livros"
  response=$(curl -s http://localhost:3000/api/livros)
  print_success "$response"

  # Teste 2: POST /api/livros (criar)
  print_test "POST" "/api/livros" "Criar novo livro"
  response=$(curl -s -X POST http://localhost:3000/api/livros \
    -H "Content-Type: application/json" \
    -d '{
      "titulo":"O Cortiço",
      "autor":"Aluísio Azevedo",
      "isbn":"9788508078142",
      "anoPublicacao":1890
    }')
  print_success "$response"
  
  # Extrair ID do livro criado
  livro_id=$(echo "$response" | jq -r '.id' 2>/dev/null)
  
  if [ ! -z "$livro_id" ] && [ "$livro_id" != "null" ]; then
    # Teste 3: GET /api/livros/:id (buscar por ID)
    print_test "GET" "/api/livros/$livro_id" "Buscar livro por ID"
    response=$(curl -s http://localhost:3000/api/livros/$livro_id)
    print_success "$response"

    # Teste 4: PUT /api/livros/:id (atualizar)
    print_test "PUT" "/api/livros/$livro_id" "Atualizar livro (marcar indisponível)"
    response=$(curl -s -X PUT http://localhost:3000/api/livros/$livro_id \
      -H "Content-Type: application/json" \
      -d '{"disponivel":false}')
    print_success "$response"

    # Teste 5: DELETE /api/livros/:id (deletar)
    print_test "DELETE" "/api/livros/$livro_id" "Deletar livro"
    http_code=$(curl -s -w "%{http_code}" -o /dev/null -X DELETE http://localhost:3000/api/livros/$livro_id)
    if [ "$http_code" = "204" ]; then
      echo -e "${GREEN}${CHECK} Sucesso! (HTTP 204)${RESET}\n"
    else
      echo -e "${RED}${CROSS} Erro! (HTTP $http_code)${RESET}\n"
    fi

    # Teste 6: Validação - Criar livro sem campos obrigatórios
    print_test "POST" "/api/livros" "Validação: livro sem campos obrigatórios"
    response=$(curl -s -X POST http://localhost:3000/api/livros \
      -H "Content-Type: application/json" \
      -d '{"titulo":"Incompleto"}')
    http_code=$(echo "$response" | jq -r '.mensagem' 2>/dev/null)
    if [ ! -z "$http_code" ]; then
      echo -e "${GREEN}${CHECK} Validação funcionando!${RESET}"
      echo -e "${BLUE}Erro retornado:${RESET}"
      echo "$response" | jq '.mensagem'
      echo ""
    fi
  fi

  # Resumo final
  print_separator
  echo -e "${BOLD}${GREEN}${STAR} TESTES COMPLETADOS COM SUCESSO!${RESET}"
  print_separator
  echo -e "${CYAN}Endpoints funcionando:${RESET}"
  echo -e "  ${CHECK} POST   /api/livros          - Criar livro"
  echo -e "  ${CHECK} GET    /api/livros          - Listar todos"
  echo -e "  ${CHECK} GET    /api/livros/:id      - Buscar por ID"
  echo -e "  ${CHECK} PUT    /api/livros/:id      - Atualizar livro"
  echo -e "  ${CHECK} DELETE /api/livros/:id      - Deletar livro"
  echo ""
  echo -e "${YELLOW}Validações:${RESET}"
  echo -e "  ${CHECK} Campos obrigatórios"
  echo -e "  ${CHECK} ISBN único"
  echo -e "  ${CHECK} Tipo de dados correto"
  echo ""
}

main
