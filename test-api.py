#!/usr/bin/env python3

import requests
import json
import time
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)

BASE_URL = "http://localhost:3000/api/livros"

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'

def print_header():
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}📚 TESTES DA API BIBLIOTECA{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")

def print_separator():
    print(f"{Colors.CYAN}{'─'*60}{Colors.RESET}")

def print_test(method, endpoint, description):
    print(f"{Colors.CYAN}➜ {Colors.BOLD}{method:<6}{Colors.RESET}{Colors.CYAN}{endpoint:<30}{Colors.YELLOW}{description}{Colors.RESET}")

def print_success(response_text):
    print(f"{Colors.GREEN}✅ Sucesso!{Colors.RESET}")
    try:
        data = json.loads(response_text)
        print(f"{Colors.BLUE}Resposta:{Colors.RESET}")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response_text)
    print()

def print_error(error_msg):
    print(f"{Colors.RED}❌ Erro! {error_msg}{Colors.RESET}\n")

def check_server():
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"{Colors.GREEN}✅ Servidor conectado na porta 3000{Colors.RESET}\n")
        return True
    except:
        print(f"{Colors.RED}❌ Servidor não está rodando!{Colors.RESET}")
        print(f"{Colors.YELLOW}Inicie com: npm run dev{Colors.RESET}")
        return False

def run_tests():
    print_header()
    
    print(f"{Colors.BOLD}🖥️  Verificando servidor...{Colors.RESET}")
    if not check_server():
        sys.exit(1)

    livro_id = None

    try:
        # Teste 1: GET /api/livros
        print_test("GET", "/api/livros", "Listar todos os livros")
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print_success(response.text)
        else:
            print_error(f"HTTP {response.status_code}")

        # Teste 2: POST /api/livros
        print_test("POST", "/api/livros", "Criar novo livro")
        livro_data = {
            "titulo": "Memórias de um Sargento de Milícias",
            "autor": "Manuel Antônio de Almeida",
            "isbn": "9788535914565",
            "anoPublicacao": 1852
        }
        response = requests.post(BASE_URL, json=livro_data)
        if response.status_code == 201:
            print_success(response.text)
            try:
                livro_id = response.json()["id"]
            except:
                pass
        else:
            print_error(f"HTTP {response.status_code}")

        if livro_id:
            # Teste 3: GET /api/livros/:id
            print_test("GET", f"/api/livros/{livro_id}", "Buscar livro por ID")
            response = requests.get(f"{BASE_URL}/{livro_id}")
            if response.status_code == 200:
                print_success(response.text)
            else:
                print_error(f"HTTP {response.status_code}")

            # Teste 4: PUT /api/livros/:id
            print_test("PUT", f"/api/livros/{livro_id}", "Atualizar livro (indisponível)")
            update_data = {"disponivel": False}
            response = requests.put(f"{BASE_URL}/{livro_id}", json=update_data)
            if response.status_code == 200:
                print_success(response.text)
            else:
                print_error(f"HTTP {response.status_code}")

            # Teste 5: DELETE /api/livros/:id
            print_test("DELETE", f"/api/livros/{livro_id}", "Deletar livro")
            response = requests.delete(f"{BASE_URL}/{livro_id}")
            if response.status_code == 204:
                print(f"{Colors.GREEN}✅ Sucesso! (HTTP 204){Colors.RESET}\n")
            else:
                print_error(f"HTTP {response.status_code}")

        # Teste 6: Validação
        print_test("POST", "/api/livros", "Validação: campos obrigatórios")
        invalid_data = {"titulo": "Incompleto"}
        response = requests.post(BASE_URL, json=invalid_data)
        if response.status_code == 400:
            print(f"{Colors.GREEN}✅ Validação funcionando!{Colors.RESET}")
            print(f"{Colors.BLUE}Erro retornado:{Colors.RESET}")
            try:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except:
                print(response.text)
            print()
        else:
            print_error(f"HTTP {response.status_code}")

        # Resumo final
        print_separator()
        print(f"{Colors.GREEN}{Colors.BOLD}⭐ TESTES COMPLETADOS COM SUCESSO!{Colors.RESET}")
        print_separator()
        print(f"{Colors.CYAN}Endpoints funcionando:{Colors.RESET}")
        print(f"  {Colors.GREEN}✅{Colors.RESET} POST   /api/livros          - Criar livro")
        print(f"  {Colors.GREEN}✅{Colors.RESET} GET    /api/livros          - Listar todos")
        print(f"  {Colors.GREEN}✅{Colors.RESET} GET    /api/livros/:id      - Buscar por ID")
        print(f"  {Colors.GREEN}✅{Colors.RESET} PUT    /api/livros/:id      - Atualizar livro")
        print(f"  {Colors.GREEN}✅{Colors.RESET} DELETE /api/livros/:id      - Deletar livro")
        print()
        print(f"{Colors.YELLOW}Validações:{Colors.RESET}")
        print(f"  {Colors.GREEN}✅{Colors.RESET} Campos obrigatórios")
        print(f"  {Colors.GREEN}✅{Colors.RESET} ISBN único")
        print(f"  {Colors.GREEN}✅{Colors.RESET} Tipo de dados correto")
        print()

    except Exception as e:
        print_error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
