import requests
import sys

def capturar_sinal_real():
    # Esta é a API que gera o link com sjwt que você viu no detector
    api_url = "https://api.spalla.top/api/v1/public/video/play/8/0/0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.band.com.br/',
        'Origin': 'https://www.band.com.br'
    }

    try:
        print("Solicitando link com token à API Spalla...")
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Extrai a URL que contém o sjwt
        link_token = data.get('data', {}).get('url')
        
        if link_token:
            # Força a qualidade 1080p se necessário
            if "playlist.m3u8" in link_token and "playlist-1080p" not in link_token:
                link_token = link_token.replace("playlist.m3u8", "playlist-1080p.m3u8")
            return link_token
        return None
    except Exception as e:
        print(f"Erro na API: {e}")
        return None

link_final = capturar_sinal_real()

# Configuração para o VLC aceitar o sinal
vlc_config = '|Referer=https://www.band.com.br/&Origin=https://www.band.com.br&User-Agent=Mozilla/5.0'

if link_final:
    print(f"Sucesso! Link com token capturado.")
    with open("band.m3u", "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1, Band Ao Vivo\n")
        f.write(f"{link_final}{vlc_config}")
else:
    print("Não foi possível capturar o link dinâmico.")
    sys.exit(1)
