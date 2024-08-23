import requests
from urllib.parse import urlparse

def read_subdomains(file_path, limit=100):
    """Lê os primeiros 'limit' subdomínios de um arquivo."""
    try:
        with open(file_path, 'r') as file:
            subdomains = [line.strip() for line in file.readlines()[:limit]]
        return subdomains
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return []

def check_subdomain(url):
    """Verifica se a URL responde com status 200."""
    protocols = ['https', 'http']
    for protocol in protocols:
        full_url = f"{protocol}://{url}"
        try:
            response = requests.get(full_url, timeout=5)
            if response.status_code == 200:
                return response.status_code, full_url
        except requests.exceptions.RequestException:
            continue
    return None, None

def extract_paths_and_files(url):
    """Extrai os caminhos e arquivos da URL."""
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/')

    # Lista de paths
    paths = []
    path_accum = ''
    path_parts = path.split('/')
    
    for i, part in enumerate(path_parts):
        path_accum += f'/{part}'
        if i < len(path_parts) - 1 or '.' not in part:
            full_path = f"{parsed_url.scheme}://{parsed_url.netloc}{path_accum}/"
            paths.append(full_path)

    # Verifica se o último segmento é um arquivo
    file_url = None
    if '.' in path_parts[-1]:
        file_url = f"{parsed_url.scheme}://{parsed_url.netloc}{path_accum}"

    return paths, file_url

def check_subdomains(file_path='subdomains-top1million-5000.txt', limit=100):
    """Processa os subdomínios completos e exibe aqueles que retornam status 200."""
    subdomains = read_subdomains(file_path, limit)
    
    if not subdomains:
        print("Nenhum subdomínio para processar.")
        return
    
    for subdomain in subdomains:
        status_code, url = check_subdomain(subdomain)
        if status_code == 200:
            print(f"status {status_code} ({url})")
            paths, file_url = extract_paths_and_files(url)
            if paths:
                print("paths:")
                for path in paths:
                    print(f"- {path}")
            if file_url:
                print("arquivos:")
                print(f"- {file_url}")
            print("-" * 50)

# Exemplo de uso
if __name__ == "__main__":
    file_path = 'subdomains-top1million-5000.txt'
    
    # Verificando subdomínios do arquivo
    check_subdomains(file_path=file_path, limit=100)
