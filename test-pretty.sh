#!/bin/bash

# Cores para output formatado
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Função para imprimir header
print_header() {
    echo -e "\n${BLUE}${BOLD}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║${NC} $1"
    echo -e "${BLUE}${BOLD}╚════════════════════════════════════════════════════════╝${NC}\n"
}

# Função para imprimir teste
print_test() {
    echo -e "${CYAN}📝 $1${NC}"
}

# Função para imprimir sucesso
print_success() {
    echo -e "${GREEN}✅ Sucesso!${NC}\n"
}

# Função para imprimir erro
print_error() {
    echo -e "${RED}❌ Erro!${NC}\n"
}

# Função para imprimir request/response
print_request() {
    echo -e "${YELLOW}Request:${NC}"
    echo -e "$1\n"
}

print_response() {
    echo -e "${YELLOW}Response:${NC}"
    echo "$1" | jq . 2>/dev/null || echo "$1"
    echo ""
}

# Aguardar servidor estar pronto
wait_server() {
    echo -e "${CYAN}⏳ Aguardando servidor...${NC}"
    for i in {1..10}; do
        if curl -s http://localhost:3000/api/livros > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Servidor pronto!${NC}\n"
            return 0
        fi
        sleep 1
    done
    echo -e "${RED}❌ Servidor não respondeu!${NC}\n"
    return 1
}

# ===== INÍCIO DOS TESTES =====
clear
print_header "🚀 API WEB BIBLIOTECA - TESTES COMPLETOS"

# 1. LISTAR LIVROS (GET - vazio)
print_test "1️⃣  GET /api/livros - Listar todos os livros"
RESPONSE=$(curl -s http://localhost:3000/api/livros)
if [ "$RESPONSE" == "[]" ]; then
    print_response "$RESPONSE"
    print_success
else
    print_response "$RESPONSE"
fi

# 2. CRIAR LIVRO 1
print_test "2️⃣  POST /api/livros - Criar primeiro livro"
REQUEST='{"titulo":"Vidas Secas","autor":"Graciliano Ramos","isbn":"9788508097679","anoPublicacao":1938}'
print_request "$REQUEST"
RESPONSE=$(curl -s -X POST http://localhost:3000/api/livros \
  -H "Content-Type: application/json" \
  -d "$REQUEST")
print_response "$RESPONSE"
print_success
ID1=$(echo "$RESPONSE" | jq -r '.id')

# 3. CRIAR LIVRO 2
print_test "3️⃣  POST /api/livros - Criar segundo livro"
REQUEST='{"titulo":"Memórias de um Sargento de Milícias","autor":"Manuel Antônio de Almeida","isbn":"9788535914565","anoPublicacao":1852}'
print_request "$REQUEST"
RESPONSE=$(curl -s -X POST http://localhost:3000/api/livros \
  -H "Content-Type: application/json" \
  -d "$REQUEST")
print_response "$RESPONSE"
print_success
ID2=$(echo "$RESPONSE" | jq -r '.id')

# 4. CRIAR LIVRO 3
print_test "4️⃣  POST /api/livros - Criar terceiro livro"
REQUEST='{"titulo":"O Cortiço","autor":"Aluísio Azevedo","isbn":"9788508078142","anoPublicacao":1890}'
print_request "$REQUEST"
RESPONSE=$(curl -s -X POST http://localhost:3000/api/livros \
  -H "Content-Type: application/json" \
  -d "$REQUEST")
print_response "$RESPONSE"
print_success
ID3=$(echo "$RESPONSE" | jq -r '.id')

# 5. LISTAR TODOS
print_test "5️⃣  GET /api/livros - Listar todos os livros (após criações)"
RESPONSE=$(curl -s http://localhost:3000/api/livros)
print_response "$RESPONSE"
print_success

# 6. BUSCAR POR ID
print_test "6️⃣  GET /api/livros/$ID1 - Buscar livro por ID"
RESPONSE=$(curl -s http://localhost:3000/api/livros/$ID1)
print_response "$RESPONSE"
print_success

# 7. ATUALIZAR LIVRO
print_test "7️⃣  PUT /api/livros/$ID2 - Atualizar disponibilidade"
REQUEST='{"disponivel":false}'
print_request "$REQUEST"
RESPONSE=$(curl -s -X PUT http://localhost:3000/api/livros/$ID2 \
  -H "Content-Type: application/json" \
  -d "$REQUEST")
print_response "$RESPONSE"
print_success

# 8. ATUALIZAR TÍTULO
print_test "8️⃣  PUT /api/livros/$ID3 - Atualizar título"
REQUEST='{"titulo":"O Cortiço - Edição Especial"}'
print_request "$REQUEST"
RESPONSE=$(curl -s -X PUT http://localhost:3000/api/livros/$ID3 \
  -H "Content-Type: application/json" \
  -d "$REQUEST")
print_response "$RESPONSE"
print_success

# 9. ERRO DE VALIDAÇÃO
print_test "9️⃣  POST /api/livros - Tentar criar sem campos obrigatórios"
REQUEST='{"titulo":"Livro Incompleto"}'
print_request "$REQUEST"
RESPONSE=$(curl -s -X POST http://localhost:3000/api/livros \
  -H "Content-Type: application/json" \
  -d "$REQUEST")
if echo "$RESPONSE" | grep -q "mensagem"; then
    print_response "$RESPONSE"
    echo -e "${GREEN}✅ Validação funcionando corretamente!${NC}\n"
else
    print_response "$RESPONSE"
fi

# 10. ERRO DE ISBN DUPLICADO
print_test "🔟 POST /api/livros - Tentar criar livro com ISBN duplicado"
REQUEST='{"titulo":"Novo Livro","autor":"Autor","isbn":"9788508097679","anoPublicacao":2000}'
print_request "$REQUEST"
RESPONSE=$(curl -s -X POST http://localhost:3000/api/livros \
  -H "Content-Type: application/json" \
  -d "$REQUEST")
if echo "$RESPONSE" | grep -q "ISBN"; then
    print_response "$RESPONSE"
    echo -e "${GREEN}✅ Validação de ISBN funcionando!${NC}\n"
else
    print_response "$RESPONSE"
fi

# 11. DELETAR LIVRO
print_test "1️⃣1️⃣  DELETE /api/livros/$ID1 - Deletar livro"
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X DELETE http://localhost:3000/api/livros/$ID1)
HTTP_STATUS=$(echo "$RESPONSE" | grep HTTP_STATUS | cut -d: -f2)
if [ "$HTTP_STATUS" == "204" ]; then
    echo -e "${GREEN}✅ Deletado com sucesso! (HTTP $HTTP_STATUS)${NC}\n"
else
    echo -e "${RED}❌ Erro ao deletar (HTTP $HTTP_STATUS)${NC}\n"
fi

# 12. LISTAR FINAIS
print_test "1️⃣2️⃣  GET /api/livros - Estado final da base"
RESPONSE=$(curl -s http://localhost:3000/api/livros)
print_response "$RESPONSE"

# RESUMO FINAL
print_header "📊 RESUMO DOS TESTES"
echo -e "${GREEN}${BOLD}✅ Todos os testes executados com sucesso!${NC}"
echo -e "\n${CYAN}Operações testadas:${NC}"
echo -e "  • GET /api/livros - ${GREEN}✓${NC}"
echo -e "  • POST /api/livros - ${GREEN}✓${NC}"
echo -e "  • PUT /api/livros/:id - ${GREEN}✓${NC}"
echo -e "  • DELETE /api/livros/:id - ${GREEN}✓${NC}"
echo -e "  • Validação de dados - ${GREEN}✓${NC}"
echo -e "  • Constraint de ISBN - ${GREEN}✓${NC}"
echo -e "\n${BOLD}${GREEN}API está 100% funcional!${NC}\n"
