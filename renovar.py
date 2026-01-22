import requests
import re
import sys

def capturar_link():
    url = "https://www.band.com.br/ao-vivo"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("Buscando novo link no site da Band...")
        r = requests.get(url, headers=headers, timeout=20)
        
        # Esta linha procura o link m3u8 com o token dentro do código da página
        links = re.findall(r'https://[a-zA-Z0-9./\-_]+\.m3u8\?sjwt=[a-zA-Z0-9.\-_]+', r.text)
        
        if links:
            return links[0]
        return None
    except Exception as e:
        print(f"Erro na captura: {e}")
        return None

link_novo = capturar_link()

if link_novo:
    print(f"Sucesso! Link encontrado: {link_novo}")
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{link_novo}")
else:
    print("Nao foi possivel encontrar o link no codigo da pagina.")
    sys.exit(1)
