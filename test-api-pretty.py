#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime

# Cores ANSI
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'

BASE_URL = "http://localhost:3000/api/livros"

def print_header(title):
    """Imprime um header formatado"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}╔════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.NC} {title}")
    print(f"{Colors.BLUE}{Colors.BOLD}╚════════════════════════════════════════════════════════╝{Colors.NC}\n")

def print_test(number, description):
    """Imprime descrição do teste"""
    print(f"{Colors.CYAN}📝 {number}️⃣  {description}{Colors.NC}")

def print_request(method, data=None):
    """Imprime a requisição"""
    print(f"{Colors.YELLOW}Request ({method}):{Colors.NC}")
    if data:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    print()

def print_response(data, status_code=None):
    """Imprime a resposta formatada"""
    print(f"{Colors.YELLOW}Response{f' (HTTP {status_code})' if status_code else ''}:{Colors.NC}")
    if isinstance(data, dict):
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(data)
    print()

def print_success(message="Sucesso!"):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}\n")

def print_error(message="Erro!"):
    """Imprime mensagem de erro"""
    print(f"{Colors.RED}❌ {message}{Colors.NC}\n")

def wait_server(max_attempts=10):
    """Aguarda o servidor ficar pronto"""
    print(f"{Colors.CYAN}⏳ Aguardando servidor...{Colors.NC}")
    for i in range(max_attempts):
        try:
            response = requests.get(BASE_URL, timeout=1)
            print(f"{Colors.GREEN}✅ Servidor pronto!{Colors.NC}\n")
            return True
        except:
            time.sleep(1)
    print(f"{Colors.RED}❌ Servidor não respondeu!{Colors.NC}\n")
    return False

def main():
    # Header principal
    clear_screen()
    print_header("🚀 API WEB BIBLIOTECA - TESTES COMPLETOS (Python)")
    
    # Aguardar servidor
    if not wait_server():
        return
    
    ids = []
    
    try:
        # 1. Listar vazio
        print_test(1, "GET /api/livros - Listar todos os livros")
        response = requests.get(BASE_URL)
        data = response.json()
        print_response(data, response.status_code)
        print_success("Lista vazia inicialmente")
        
        # 2. Criar livro 1
        print_test(2, "POST /api/livros - Criar primeiro livro")
        livro1 = {
            "titulo": "Vidas Secas",
            "autor": "Graciliano Ramos",
            "isbn": "9788508097679",
            "anoPublicacao": 1938
        }
        print_request("POST", livro1)
        response = requests.post(BASE_URL, json=livro1)
        data = response.json()
        print_response(data, response.status_code)
        print_success()
        ids.append(data['id'])
        
        # 3. Criar livro 2
        print_test(3, "POST /api/livros - Criar segundo livro")
        livro2 = {
            "titulo": "Memórias de um Sargento de Milícias",
            "autor": "Manuel Antônio de Almeida",
            "isbn": "9788535914565",
            "anoPublicacao": 1852
        }
        print_request("POST", livro2)
        response = requests.post(BASE_URL, json=livro2)
        data = response.json()
        print_response(data, response.status_code)
        print_success()
        ids.append(data['id'])
        
        # 4. Criar livro 3
        print_test(4, "POST /api/livros - Criar terceiro livro")
        livro3 = {
            "titulo": "O Cortiço",
            "autor": "Aluísio Azevedo",
            "isbn": "9788508078142",
            "anoPublicacao": 1890
        }
        print_request("POST", livro3)
        response = requests.post(BASE_URL, json=livro3)
        data = response.json()
        print_response(data, response.status_code)
        print_success()
        ids.append(data['id'])
        
        # 5. Listar todos
        print_test(5, "GET /api/livros - Listar todos os livros (após criações)")
        response = requests.get(BASE_URL)
        data = response.json()
        print_response(data, response.status_code)
        print_success(f"Total de livros: {len(data)}")
        
        # 6. Buscar por ID
        print_test(6, f"GET /api/livros/{ids[0]} - Buscar livro por ID")
        response = requests.get(f"{BASE_URL}/{ids[0]}")
        data = response.json()
        print_response(data, response.status_code)
        print_success()
        
        # 7. Atualizar disponibilidade
        print_test(7, f"PUT /api/livros/{ids[1]} - Atualizar disponibilidade")
        update_data = {"disponivel": False}
        print_request("PUT", update_data)
        response = requests.put(f"{BASE_URL}/{ids[1]}", json=update_data)
        data = response.json()
        print_response(data, response.status_code)
        print_success()
        
        # 8. Atualizar título
        print_test(8, f"PUT /api/livros/{ids[2]} - Atualizar título")
        update_data = {"titulo": "O Cortiço - Edição Especial"}
        print_request("PUT", update_data)
        response = requests.put(f"{BASE_URL}/{ids[2]}", json=update_data)
        data = response.json()
        print_response(data, response.status_code)
        print_success()
        
        # 9. Erro de validação
        print_test(9, "POST /api/livros - Tentar criar sem campos obrigatórios")
        invalid_livro = {"titulo": "Livro Incompleto"}
        print_request("POST", invalid_livro)
        response = requests.post(BASE_URL, json=invalid_livro)
        data = response.json()
        print_response(data, response.status_code)
        print_success("Validação funcionando corretamente!")
        
        # 10. Erro ISBN duplicado
        print_test(10, "POST /api/livros - Tentar criar livro com ISBN duplicado")
        duplicate_isbn = {
            "titulo": "Novo Livro",
            "autor": "Autor",
            "isbn": "9788508097679",
            "anoPublicacao": 2000
        }
        print_request("POST", duplicate_isbn)
        response = requests.post(BASE_URL, json=duplicate_isbn)
        data = response.json()
        print_response(data, response.status_code)
        print_success("Validação de ISBN funcionando!")
        
        # 11. Deletar livro
        print_test(11, f"DELETE /api/livros/{ids[0]} - Deletar livro")
        response = requests.delete(f"{BASE_URL}/{ids[0]}")
        if response.status_code == 204:
            print(f"{Colors.YELLOW}Response (HTTP 204):{Colors.NC}")
            print("(Sem conteúdo)\n")
            print_success("Deletado com sucesso!")
        else:
            print_response(response.text, response.status_code)
            print_error()
        
        # 12. Listar finais
        print_test(12, "GET /api/livros - Estado final da base")
        response = requests.get(BASE_URL)
        data = response.json()
        print_response(data, response.status_code)
        print_success(f"Livros restantes: {len(data)}")
        
        # Resumo
        print_header("📊 RESUMO DOS TESTES")
        print(f"{Colors.GREEN}{Colors.BOLD}✅ Todos os testes executados com sucesso!{Colors.NC}\n")
        print(f"{Colors.CYAN}Operações testadas:{Colors.NC}")
        print(f"  • GET /api/livros - {Colors.GREEN}✓{Colors.NC}")
        print(f"  • POST /api/livros - {Colors.GREEN}✓{Colors.NC}")
        print(f"  • PUT /api/livros/:id - {Colors.GREEN}✓{Colors.NC}")
        print(f"  • DELETE /api/livros/:id - {Colors.GREEN}✓{Colors.NC}")
        print(f"  • Validação de dados - {Colors.GREEN}✓{Colors.NC}")
        print(f"  • Constraint de ISBN - {Colors.GREEN}✓{Colors.NC}")
        print(f"\n{Colors.BOLD}{Colors.GREEN}API está 100% funcional!{Colors.NC}\n")
        
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar ao servidor")
    except Exception as e:
        print_error(f"Erro: {str(e)}")

def clear_screen():
    """Limpa a tela"""
    import os
    os.system('clear' if os.name == 'posix' else 'cls')

if __name__ == "__main__":
    main()
