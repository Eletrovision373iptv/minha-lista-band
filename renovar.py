import requests
import re
import sys

def capturar_link():
    # URL da Band
    url_alvo = "https://www.band.com.br/ao-vivo"
    
    # Headers para simular um navegador comum
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("Acessando o código fonte da Band...")
        response = requests.get(url_alvo, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Esta é a parte que 'caça' o link m3u8 com o token no meio do texto
        # Procuramos o padrão da Spalla (singularcdn)
        padrao = r'https://[a-zA-Z0-9./\-_]+\.m3u8\?sjwt=[a-zA-Z0-9.\-_]+'
        links = re.findall(padrao, response.text)

        if links:
            print("Link com token encontrado!")
            return links[0]
        else:
            # Tenta um padrão secundário caso o primeiro mude
            padrao_reserva = r'https://[a-zA-Z0-9./\-_]+playlist.m3u8\?sjwt=[a-zA-Z0-9.\-_]+'
            links_reserva = re.findall(padrao_reserva, response.text)
            return links_reserva[0] if links_reserva else None

    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

# Execução
link_atualizado = capturar_link()

if link_atualizado:
    with open("band.m3u", "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1, Band Ao Vivo\n")
        f.write(link_atualizado)
    print(f"Sucesso: {link_atualizado}")
else:
    print("Falha: O link não estava no HTML. O site pode ter mudado a proteção.")
    sys.exit(1)
