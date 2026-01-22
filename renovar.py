import requests
import re
import sys

def capturar_link():
    url_band = "https://www.band.com.br/ao-vivo"
    
    # Fingimos ser um navegador comum para o site não bloquear
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("Acessando o site da Band...")
        response = requests.get(url_band, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Procuramos o link que contém playlist-1080p.m3u8 e o token sjwt
        # O padrão busca algo como https://...playlist-1080p.m3u8?sjwt=...
        padrao = r'https://[a-zA-Z0-9./\-_]+\.m3u8\?sjwt=[a-zA-Z0-9.\-_]+'
        links_encontrados = re.findall(padrao, response.text)

        if links_encontrados:
            # Pegamos o primeiro link encontrado
            return links_encontrados[0]
        else:
            return None

    except Exception as e:
        print(f"Erro na requisição: {e}")
        return None

novo_link = capturar_link()

if novo_link:
    print(f"Sucesso! Link encontrado: {novo_link}")
    with open("band.m3u", "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1, Band Ao Vivo\n")
        f.write(novo_link)
else:
    print("Falha: O link com token não foi encontrado no código da página.")
    sys.exit(1)
