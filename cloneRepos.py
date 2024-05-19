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

def get_commits(repo_name, per_page=12):
    url = f"https://api.github.com/repos/{repo_name}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    params = {"per_page": per_page}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def clone_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        return False
    print(f"Clonando {repo_url} em {clone_dir}")
    Repo.clone_from(repo_url, clone_dir, progress=Progress())
    return True

def checkout_version(repo_dir, commit_sha):
    repo = Repo(repo_dir)
    repo.git.checkout(commit_sha)

def main():
    # repos.items são todos os repositorios selecionados a partir do script pythonRepos.py
    # repo_name é o dono/nome do repo e url é a url de acesso
    for repo_name, repo_url in repos.items():
        print(f"ATUAL {repo_name}")
        # get_commits pega os ultimos 12 commits de um dos repo. Cada commit é uma versão a ser analisada
        commits = get_commits(repo_name)
        
        if not commits:
            print(f"Sem commits: {repo_name}")
            continue

        base_clone_dir = f"./repos/{repo_name}"
        
        # Process the last 12 commits
        for i, commit in enumerate(commits):
            commit_sha = commit['sha']
            version_dir = f"{base_clone_dir}_version_{i+1}"
            
            # Clone the repo and checkout to the specific commit
            if commit_sha and not os.path.exists(version_dir):
                clone_repo(repo_url, base_clone_dir)
                if not os.path.exists(version_dir):
                    os.mkdir(version_dir)
                checkout_version(base_clone_dir, commit_sha)
                os.rename(base_clone_dir, version_dir)
                print(f"Versão {i+1} salva no path {version_dir}")

if __name__ == "__main__":
    main()