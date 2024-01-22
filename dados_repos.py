import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Carregue as variáveis de ambiente do arquivo .env.
load_dotenv()

class DadosRepositorios:

    def __init__(self, owner):
        self.owner=owner
        self.api_base_url='https://api.github.com'
        self.access_token=os.getenv('ACCESS_TOKEN')
        self.headers={'Authorization': 'Bearer ' + self.access_token,
                      'X-GitHub-Api-Version': '2022-11-28'}
        
    def lista_repositorios(self):
        repos_list = []
        page_num = 1
        next_page_url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'

        with requests.Session() as session:
            session.headers.update(self.headers)

            while next_page_url:
                try:
                    response = session.get(next_page_url)
                    response.raise_for_status()
                    repos_list.append(response.json())

                    links = requests.utils.parse_header_links(response.headers.get('Link', ''))
                    next_link = next((link['url'] for link in links if link['rel'] == 'next'), None)
                    next_page_url = next_link
                    page_num += 1
                except requests.exceptions.RequestException:
                    next_page_url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                    repos_list.append(None)

        return repos_list
    
    def nomes_repos (self, repos_list): 
        repo_names=[] 
        for page in repos_list:
            for repo in page:
                try:
                    repo_names.append(repo['name'])
                except: 
                    pass

        return repo_names
    
    def nomes_linguagens (self, repos_list):
        repo_languages=[]
        for page in repos_list:
            for repo in page:
                try:
                    repo_languages.append(repo['language'])
                except:
                    pass

        return repo_languages
    
    def cria_df_linguagens (self):

        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos(repositorios)
        linguagens = self.nomes_linguagens(repositorios)

        dados = pd.DataFrame()
        dados['repository_name'] = nomes
        dados['language'] = linguagens

        return dados

# Extraindo dados dos repositórios

amazon_rep = DadosRepositorios('amzn')
ling_mais_usadas_amzn = amazon_rep.cria_df_linguagens()

netflix_rep = DadosRepositorios('netflix')
ling_mais_usadas_netflix = netflix_rep.cria_df_linguagens()

spotify_rep = DadosRepositorios('spotify')
ling_mais_usadas_spotify = spotify_rep.cria_df_linguagens()

# Salvando os dados 
ling_mais_usadas_amzn.to_csv('dados/linguagens_amzn.csv')
ling_mais_usadas_netflix.to_csv('dados/linguagens_netflix.csv')
ling_mais_usadas_spotify.to_csv('dados/linguagens_spotify.csv')