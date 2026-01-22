import requests
import sys

# Este script nao lê o site da Band, ele fala direto com o servidor de sinal
def pegar_link():
    api_url = "https://api.spalla.top/api/v1/public/video/play/8/0/0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.band.com.br/',
        'Origin': 'https://www.band.com.br'
    }

    try:
        print("Conectando diretamente ao servidor de sinal (Spalla API)...")
        r = requests.get(api_url, headers=headers, timeout=10)
        dados = r.json()
        link = dados.get('data', {}).get('url')
        
        if link:
            # Força a qualidade para 1080p
            return link.replace("playlist.m3u8", "playlist-1080p.m3u8")
        return None
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

link_final = pegar_link()

if link_final:
    print(f"SUCESSO! Link obtido: {link_final}")
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{link_final}")
else:
    print("FALHA: O servidor de sinal não respondeu com um link.")
    sys.exit(1)
