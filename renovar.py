import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def capturar_link():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Ativa a captura de logs de performance
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("Acessando a Band...")
        driver.get("https://www.band.com.br/ao-vivo")
        
        # Espera o player carregar (pode levar um tempo na Band)
        print("Aguardando carregamento do streaming...")
        time.sleep(20) 
        
        # Pega os logs de rede
        logs = driver.get_log("performance")
        link_m3u8 = None
        
        for entry in logs:
            if "playlist-1080p.m3u8" in entry["message"]:
                # Limpa a mensagem do log para extrair a URL pura
                import json
                log_data = json.loads(entry["message"])
                url = log_data["message"]["params"].get("request", {}).get("url")
                if url and "playlist-1080p.m3u8" in url:
                    link_m3u8 = url
                    break
        
        return link_m3u8
    except Exception as e:
        print(f"Erro durante a captura: {e}")
        return None
    finally:
        driver.quit()

novo_link = capturar_link()

if novo_link:
    print(f"Sucesso! Link encontrado: {novo_link}")
    with open("band.m3u", "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1, Band Ao Vivo\n")
        f.write(novo_link)
else:
    print("Falha: O link não foi encontrado nos logs de rede.")
    exit(1) # Força o erro no GitHub se não achar o link
