import requests
from urllib.parse import urlparse
import sys

def read_wordlist(wordlist_file, limit=None):
    """Lê a wordlist para subdomínios, paths ou arquivos."""
    try:
        with open(wordlist_file, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        return lines[:limit] if limit else lines
    except FileNotFoundError:
        print(f"Erro: Arquivo '{wordlist_file}' não encontrado.")
        return []

def check_url(url):
    """Verifica se a URL responde com status 200."""
    protocols = ['https', 'http']
    for protocol in protocols:
        full_url = f"{protocol}://{url}"
        try:
            response = requests.get(full_url, timeout=5)
            if response.status_code == 200:
                return full_url
        except requests.exceptions.RequestException:
            continue
    return None

def enumerate_subdomains(domain, subdomains):
    """Enumera subdomínios válidos."""
    valid_subdomains = []
    for subdomain in subdomains:
        url = f"{subdomain}.{domain}"
        full_url = check_url(url)
        if full_url:
            valid_subdomains.append(full_url)
    return valid_subdomains

def enumerate_paths_and_files(domain, paths, files):
    """Enumera paths e arquivos válidos."""
    valid_paths = []
    valid_files = []

    # Paths
    for path in paths:
        url = f"{domain}/{path}"
        full_url = check_url(url)
        if full_url:
            valid_paths.append(full_url)

    # Arquivos
    for file in files:
        url = f"{domain}/{file}"
        full_url = check_url(url)
        if full_url:
            valid_files.append(full_url)

    return valid_paths, valid_files

def main(domain):
    print("------------------------------------------------------------------------")
    print("1TDCPG -> Vinicius Lourenco")
    print(f"Alvo: {domain}")
    print("--------------------------------")

    # Subdomínios
    subdomains = read_wordlist('subdomains.txt')
    valid_subdomains = enumerate_subdomains(domain, subdomains)
    print("Subdomínios encontrados:")
    for subdomain in valid_subdomains:
        print(subdomain)
    print("--------------------------------")

    # Paths e Arquivos
    paths = read_wordlist('paths.txt')
    files = read_wordlist('files.txt')
    valid_paths, valid_files = enumerate_paths_and_files(domain, paths, files)

    print("Paths encontrados:")
    for path in valid_paths:
        print(path)
    print("--------------------------------")

    print("Arquivos encontrados:")
    for file in valid_files:
        print(file)
    print("--------------------------------")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python cp1.py <dominio>")
        sys.exit(1)

    target_domain = sys.argv[1]
    main(target_domain)
