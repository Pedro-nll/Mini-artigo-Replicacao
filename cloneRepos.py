import os
import requests
from datetime import datetime
from git import Repo
from git.remote import RemoteProgress

class Progress(RemoteProgress):
    def update(self, *args):
        print(self._cur_line)

# Lista de repos escolhida para o mini-artigo
repos = {
    "public-apis/public-apis": "https://github.com/public-apis/public-apis",
    "AUTOMATIC1111/stable-diffusion-webui": "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
    "ytdl-org/youtube-dl": "https://github.com/ytdl-org/youtube-dl",
    "huggingface/transformers": "https://github.com/huggingface/transformers",
    "langchain-ai/langchain": "https://github.com/langchain-ai/langchain",
    "pytorch/pytorch": "https://github.com/pytorch/pytorch"
}

GITHUB_TOKEN = ""

def get_commits(repo_name, per_page=30):
    url = f"https://api.github.com/repos/{repo_name}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers, params={"per_page": per_page})
    response.raise_for_status()
    return response.json()

def clone_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        return False
    print(f"Cloning from {repo_url} into {clone_dir}")
    Repo.clone_from(repo_url, clone_dir, progress=Progress())
    return True

def checkout_version(repo_dir, commit_sha):
    repo = Repo(repo_dir)
    repo.git.checkout(commit_sha)

def main():
    # repos.items são todos os repositorios selecionados a partir do script pythonRepos.py
    # repo_name é o dono/nome do repo e url é a url de acesso
    for repo_name, repo_url in repos.items():
        print(f"Processing: {repo_name}")
        # get_commits pega os ultimos 30 commits de um dos repo
        # 30 é a paginação do github
        commits = get_commits(repo_name)
        
        if not commits:
            print(f"No commits found for {repo_name}")
            continue

        # primeiro comit (numero 29) da lista de commits e o ultimo commit feito (0) 
        first_commit_sha = commits[-1]['sha']
        latest_commit_sha = commits[0]['sha']
        
        # Definindo o nome dos arquivos pra cada versão
        base_clone_dir = f"./repos/{repo_name}"
        latest_dir = f"{base_clone_dir}_latest"
        first_dir = f"{base_clone_dir}_first"
        
        # Clona o repo e dá checkout pra ultima versão dele
        if latest_commit_sha and not os.path.exists(latest_dir):
            clone_repo(repo_url, base_clone_dir)
            if not os.path.exists(latest_dir):
                os.mkdir(latest_dir)
            checkout_version(base_clone_dir, latest_commit_sha)
            os.rename(base_clone_dir, latest_dir)
            print(f"ULTIMA VERSÃO SALVA NO PATH {latest_dir}")

        # Clona o repo e dá checkout pra versão mais antiga pega na paginação dele
        if first_commit_sha and not os.path.exists(first_dir):
            clone_repo(repo_url, base_clone_dir)
            if not os.path.exists(first_dir):
                os.mkdir(first_dir)
            checkout_version(base_clone_dir, first_commit_sha)
            os.rename(base_clone_dir, first_dir)
            print(f"PRIMEIRA VERSAO SALVA NO PATH {first_dir}")

if __name__ == "__main__":
    main()