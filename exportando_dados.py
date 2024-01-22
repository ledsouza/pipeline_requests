from manipula_repos import ManipulaRepositorios

# instanciando um objeto
novo_repo = ManipulaRepositorios('ledsouza')

# Criando o repositório
nome_repo = 'linguagens-repositorios-empresas'
novo_repo.cria_repo(nome_repo)

# Adicionando arquivos salvos no repositório criado
novo_repo.add_arquivo(nome_repo, 'linguagens_amzn.csv', 'dados/linguagens_amzn.csv')
novo_repo.add_arquivo(nome_repo, 'linguagens_netflix.csv', 'dados/linguagens_netflix.csv')
novo_repo.add_arquivo(nome_repo, 'linguagens_spotify.csv', 'dados/linguagens_spotify.csv')