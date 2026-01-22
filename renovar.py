import requests
import sys

def capturar_sinal_direto():
    # Esta URL é a "fonte" oficial que gera o link do streaming
    api_url = "https://api.spalla.top/api/v1/public/video/play/8/0/0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.band.com.br/',
        'Origin': 'https://www.band.com.br'
    }

    try:
        print("Solicitando link direto ao servidor de sinal...")
        response = requests.get(api_url, headers=headers, timeout=10)
        data = response.json()
        
        # O link m3u8 real vem dentro da resposta da API
        link_bruto = data.get('data', {}).get('url')
        
        if link_bruto:
            # Forçamos a qualidade máxima (1080p)
            link_final = link_bruto.replace("playlist.m3u8", "playlist-1080p.m3u8")
            return link_final
        return None
    except Exception as e:
        print(f"Erro na API: {e}")
        return None

novo_link = capturar_sinal_direto()

if novo_link:
    print(f"Sucesso! Link capturado: {novo_link}")
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{novo_link}")
else:
    print("A API da Band não retornou o sinal. Verificando bloqueios...")
    sys.exit(1)
