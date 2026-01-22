import requests
import sys

def capturar_link_direto():
    # Esta é a URL da API que gera o sinal da Band
    api_url = "https://api.spalla.top/api/v1/public/video/play/8/0/0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.band.com.br/',
        'Origin': 'https://www.band.com.br'
    }

    try:
        print("Solicitando sinal à API da Spalla...")
        response = requests.get(api_url, headers=headers, timeout=15)
        data = response.json()
        
        # O link m3u8 fica escondido dentro da resposta JSON
        link_m3u8 = data.get('data', {}).get('url')
        
        if link_m3u8:
            # Forçamos a qualidade máxima (1080p) se disponível
            if "playlist.m3u8" in link_m3u8:
                link_m3u8 = link_m3u8.replace("playlist.m3u8", "playlist-1080p.m3u8")
            return link_m3u8
        return None
    except Exception as e:
        print(f"Erro na API: {e}")
        return None

novo_link = capturar_link_direto()

if novo_link:
    print(f"Sucesso! Link da API: {novo_link}")
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{novo_link}")
else:
    print("A API da Spalla não retornou um link válido.")
    sys.exit(1)
