import requests
import sys

def capturar_direto():
    # Esta é a URL da API secreta que gera o link de sinal da Band
    api_url = "https://api.spalla.top/api/v1/public/video/play/8/0/0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.band.com.br/',
        'Origin': 'https://www.band.com.br'
    }

    try:
        print("Solicitando link de streaming diretamente à API...")
        response = requests.get(api_url, headers=headers, timeout=10)
        data = response.json()
        
        # Extrai a URL do vídeo de dentro dos dados da API
        link = data.get('data', {}).get('url')
        
        if link:
            # Garante que pegamos a melhor qualidade (1080p)
            return link.replace("playlist.m3u8", "playlist-1080p.m3u8")
        return None
    except Exception as e:
        print(f"Erro na API: {e}")
        return None

link_final = capturar_direto()

if link_final:
    print(f"Sucesso! Link capturado: {link_final}")
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{link_final}")
else:
    print("Falha ao obter sinal da API.")
    sys.exit(1)
