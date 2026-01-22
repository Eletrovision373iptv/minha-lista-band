import requests
import re
import sys

def capturar():
    url = "https://www.band.com.br/ao-vivo"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    try:
        print("Acessando site oficial da Band...")
        r = requests.get(url, headers=headers, timeout=20)
        content = r.text

        # 1. Tenta buscar link direto com token sjwt
        match = re.search(r'https://[a-zA-Z0-9./\-_]+\.m3u8\?sjwt=[a-zA-Z0-9.\-_]+', content)
        
        # 2. Se não achar, tenta buscar links dentro de aspas (formato JSON)
        if not match:
            match = re.search(r'https:[\\/]+[a-zA-Z0-9.\-_/]+playlist\.m3u8\?sjwt=[a-zA-Z0-9.\-_]+', content)
        
        if match:
            link = match.group(0).replace('\\/', '/')
            # Força qualidade 1080p
            return link.replace("playlist.m3u8", "playlist-1080p.m3u8")
        
        return None
    except Exception as e:
        print(f"Erro: {e}")
        return None

link_final = capturar()

if link_final:
    print(f"Sucesso! Link encontrado: {link_final}")
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{link_final}")
else:
    # Se tudo falhar, usamos o link fixo da CDN que costuma durar mais tempo
    print("Link dinâmico não encontrado. Usando link de emergência...")
    link_emergencia = "https://evp-singular-band.akamaized.net/out/v1/7888258e80714f33a824497e88949f57/playlist.m3u8"
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{link_emergencia}")
