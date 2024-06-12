import requests
from bs4 import BeautifulSoup
import time
import random
import sys

def busca_telefone(busca):
    url = f"https://www.google.com/search?q={requests.utils.quote(busca)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Erro ao realizar a busca: {response.status_code}")
        return None

def random_delay():
    time.sleep(random.uniform(2, 5))  # Atraso aleatório entre 2 e 5 segundos

def main():
    if len(sys.argv) != 2:
        print("Comando inválido, utilize da seguinte maneira:")
        print(f"> python {sys.argv[0]} contas.txt")
        sys.exit(1)

    contas_file = sys.argv[1]

    with open(contas_file, 'r') as file:
        contas = file.readlines()

    total = len(contas)
    i = 0

    for linha in contas:
        linha = linha.strip()
        aConta = linha.split(";")
        cnpj = aConta[0].strip()
        razao = aConta[1].strip()

        print(f"[{i + 1} de {total}] Razão: {razao} ", end='')

        texto_busca = f"TELEFONE {razao}"

        html_busca_telefone = busca_telefone(texto_busca)
        
        if html_busca_telefone:
            soup = BeautifulSoup(html_busca_telefone, 'html.parser')
            telefone_span = soup.find('span', class_='LrzXr zdqRlf kno-fv')
            telefone = None
            if telefone_span:
                telefone = telefone_span.get_text()
            
            if telefone:
                print(f" => POSSUI TELEFONE: {telefone}")
                with open("INFOS.txt", "a") as out_file:
                    out_file.write(f"{cnpj};{razao};{telefone}\n")
            else:
                print(" => NÃO POSSUI TELEFONE!")
        else:
            print(" => ERRO NA BUSCA!")

        random_delay()
        i += 1

if __name__ == "__main__":
    main()
