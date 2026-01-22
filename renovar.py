import requests
import re
import sys

def capturar():
    url = "https://www.band.com.br/ao-vivo"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        print("Buscando link no site...")
        r = requests.get(url, headers=headers, timeout=15)
        # Procura o link m3u8 com token sjwt
        match = re.search(r'https://[a-zA-Z0-9./\-_]+\.m3u8\?sjwt=[a-zA-Z0-9.\-_]+', r.text)
        if match:
            return match.group(0)
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
    print("Link nao encontrado no código da página.")
    sys.exit(1)
