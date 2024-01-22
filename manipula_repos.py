import requests
import base64
from dotenv import load_dotenv
import os

# Carregue as variáveis de ambiente do arquivo .env.
load_dotenv()

class ManipulaRepositorios:

    def __init__(self, username):
        self.username = username
        self.api_base_url='https://api.github.com'
        self.access_token=os.getenv('ACCESS_TOKEN')
        self.headers = {'Authorization':"Bearer " + self.access_token,
                        'X-GitHub-Api-Version': '2022-11-28'}

    def cria_repo(self, nome_repo):
        data = {
            "name": nome_repo,
            "description": "Dados dos repositórios de algumas empresas",
            "private": False
        }
        response = requests.post(f"{self.api_base_url}/user/repos", 
                                 json=data, headers=self.headers)

        print(f'status_code criação do repositório: {response.status_code}')

    def add_arquivo(self, nome_repo, nome_arquivo, caminho_arquivo):
        nome_arquivo = caminho_arquivo.split('/')[-1]

        # Codificando o arquivo
        with open(caminho_arquivo, "rb") as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content)

        # Realizando o upload
        url = f"{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{nome_arquivo}"
        data = {
                "message": "Adicionando um novo arquivo",
                "content": encoded_content.decode("utf-8")
        }

        response = requests.put(url, json=data, headers=self.headers)
        print(f'status_code upload do arquivo {nome_arquivo}: {response.status_code}')