import requests
import re
import sys

def capturar():
    url = "https://www.band.com.br/ao-vivo"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("Buscando link...")
        r = requests.get(url, headers=headers, timeout=20)
        # Tenta pegar o link dinâmico primeiro
        match = re.search(r'https://[a-zA-Z0-9./\-_]+\.m3u8\?sjwt=[a-zA-Z0-9.\-_]+', r.text)
        
        if match:
            return match.group(0).replace('\\/', '/')
        return "https://evp-singular-band.akamaized.net/out/v1/7888258e80714f33a824497e88949f57/playlist.m3u8"
    except:
        return "https://evp-singular-band.akamaized.net/out/v1/7888258e80714f33a824497e88949f57/playlist.m3u8"

link_final = capturar()

# A mágica para o VLC funcionar está aqui:
# Adicionamos o cabeçalho 'Referer' e 'User-Agent' direto no link da lista
vlc_config = '|Referer=https://www.band.com.br/&User-Agent=Mozilla/5.0'

if link_final:
    with open("band.m3u", "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1, Band Ao Vivo\n")
        # O link agora vai com as instruções para o player
        f.write(f"{link_final}{vlc_config}")
    print("Arquivo atualizado para VLC!")
