import requests
import sys

def pegar_link():
    # URL da API secreta que gera o sinal
    api_url = "https://api.spalla.top/api/v1/public/video/play/8/0/0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.band.com.br/',
        'Origin': 'https://www.band.com.br'
    }

    try:
        print("Iniciando conexao direta com a API Spalla...")
        r = requests.get(api_url, headers=headers, timeout=15)
        dados = r.json()
        link = dados.get('data', {}).get('url')
        
        if link:
            # Força a qualidade para 1080p para melhor imagem
            return link.replace("playlist.m3u8", "playlist-1080p.m3u8")
        return None
    except Exception as e:
        print(f"Erro na conexao: {e}")
        return None

link_final = pegar_link()

if link_final:
    print(f"SUCESSO! Link obtido: {link_final}")
    with open("band.m3u", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, Band Ao Vivo\n{link_final}")
else:
    print("FALHA: O servidor nao entregou o link.")
    sys.exit(1)
