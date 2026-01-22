import requests
import re
import sys

def capturar():
    # URL principal da Band
    url_site = "https://www.band.com.br/ao-vivo"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("Acessando o site da Band para buscar o ID do vídeo...")
        r = requests.get(url_site, headers=headers, timeout=15)
        
        # Tenta encontrar o link do manifesto que a Spalla (CDN da Band) usa
        # Buscamos o padrão de URL que contém o playlist.m3u8
        padrao = r'https://[a-zA-Z0-9./\-_]+playlist\.m3u8\?sjwt=[a-zA-Z0-9.\-_]+'
        match = re.search(padrao, r.text)
        
        if not match:
            # Se não achou direto, vamos buscar pelo ID do vídeo no código
            print("Link não está no HTML. Buscando por padrões alternativos...")
            # Padrão comum para o player da Band
            video_id_match = re.search(r'"videoID":"(\d+)"', r.text)
            if video_id_match:
                v_id = video_id_match.group(1)
                print(f"ID do vídeo encontrado: {v_id}")
                # Aqui você pode adicionar lógica para bater na API da Spalla se necessário
            
        if match:
            return match.group(0)
        
        # Caso o link esteja "escapado" com barras invertidas (comum em JSON)
        match_escaped = re.search(r'https:[\\/]+[a-zA-Z0-9.\-_/]+playlist\.m3u8\?sjwt=[a-zA-Z0-9.\-_]+', r.text)
        if match_escaped:
            return match_escaped.group(0).replace('\\/', '/')

        return None
    except Exception as e:
        print(f"Erro: {e}")
        return None

link = capturar()
if link:
    print(f"Sucesso! Link: {link}")
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{link}")
else:
    print("Link ainda não encontrado. O site usa carregamento dinâmico pesado.")
    sys.exit(1)
