import requests
import socket

def read_subdomains(file_path, limit=20):
    """Lê uma wordlist de subdomínios e retorna os primeiros 'limit' subdomínios."""
    try:
        with open(file_path, 'r') as file:
            subdomains = [line.strip() for line in file.readlines()]
        return subdomains[:limit]
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return []

def is_resolvable(subdomain, domain):
    """Verifica se o subdomínio pode ser resolvido via DNS."""
    try:
        socket.gethostbyname(f"{subdomain}.{domain}")
        return True
    except socket.error:
        return False

def check_subdomain(subdomain, domain, use_https=False):
    """Realiza uma requisição GET a um subdomínio e retorna o status code."""
    protocol = "https" if use_https else "http"
    full_url = f"{protocol}://{subdomain}.{domain}"
    try:
        response = requests.get(full_url, timeout=5)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return f"Erro: {e}"

def check_subdomains(domain, file_path='subdomains-top1million-5000.txt', limit=20):
    """Lê os subdomínios de uma wordlist e verifica os status codes dos primeiros 'limit' subdomínios."""
    subdomains = read_subdomains(file_path, limit)
    
    if not subdomains:
        return
    
    for subdomain in subdomains:
        if is_resolvable(subdomain, domain):
            status_code = check_subdomain(subdomain, domain)
            print(f"Subdomínio: {subdomain}.{domain} | Status Code: {status_code}")
        else:
            print(f"Subdomínio: {subdomain}.{domain} | Status Code: DNS não resolvido")

# Exemplo de uso
check_subdomains('example.com')
