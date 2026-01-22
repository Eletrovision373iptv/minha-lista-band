import requests
import sys

def pegar_link_seguro():
    # API Spalla que gera o token sjwt
    api_url = "https://api.spalla.top/api/v1/public/video/play/8/0/0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.band.com.br/',
        'Origin': 'https://www.band.com.br'
    }

    try:
        # Timeout de 10 segundos para nao travar o GitHub
        print("Conectando a API (Limite de 10s)...")
        r = requests.get(api_url, headers=headers, timeout=10)
        r.raise_for_status()
        
        link = r.json().get('data', {}).get('url')
        if link:
            # Força 1080p se disponível
            return link.replace("playlist.m3u8", "playlist-1080p.m3u8")
        return None
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

link_final = pegar_link_seguro()

# Headers para o VLC nao dar erro 403
vlc_headers = '|Referer=https://www.band.com.br/&Origin=https://www.band.com.br&User-Agent=Mozilla/5.0'

if link_final:
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{link_final}{vlc_headers}")
    print("Sucesso! Arquivo band.m3u atualizado.")
else:
    print("Falha total. Gerando link de emergencia para nao travar.")
    # Link de emergencia caso a API esteja fora
    emergencia = "https://evp-singular-band.akamaized.net/out/v1/7888258e80714f33a824497e88949f57/playlist.m3u8"
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{emergencia}{vlc_headers}")
