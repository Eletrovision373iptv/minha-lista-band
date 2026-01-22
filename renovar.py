import requests
import sys

def capturar_sinal():
    # Esta é a URL da API da Spalla que fornece o sinal para a Band
    # O ID '8' geralmente corresponde ao sinal nacional ao vivo
    api_url = "https://api.spalla.top/api/v1/public/video/play/8/0/0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.band.com.br/',
        'Origin': 'https://www.band.com.br'
    }

    try:
        print("Solicitando link de streaming à API Spalla...")
        response = requests.get(api_url, headers=headers, timeout=10)
        data = response.json()
        
        # Extrai a URL do campo 'url' dentro do JSON de resposta
        link_m3u8 = data.get('data', {}).get('url')
        
        if link_m3u8:
            # Força a qualidade 1080p se estiver no formato padrão
            if "playlist.m3u8" in link_m3u8:
                link_m3u8 = link_m3u8.replace("playlist.m3u8", "playlist-1080p.m3u8")
            return link_m3u8
        return None
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return None

link_final = capturar_sinal()

if link_final:
    print(f"Link capturado com sucesso: {link_final}")
    with open("band.m3u", "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1, Band Ao Vivo\n")
        f.write(link_final)
else:
    print("Não foi possível obter o link da API.")
    sys.exit(1)
