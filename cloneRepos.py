import os
import requests
from datetime import datetime, timedelta
from git import Repo
from git.remote import RemoteProgress

class Progress(RemoteProgress):
    def update(self, *args):
        print(self._cur_line)

# Define the list of repositories to be analyzed
repos = {
    "public-apis/public-apis": "https://github.com/public-apis/public-apis",
    "AUTOMATIC1111/stable-diffusion-webui": "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
    "ytdl-org/youtube-dl": "https://github.com/ytdl-org/youtube-dl",
    "huggingface/transformers": "https://github.com/huggingface/transformers",
    "langchain-ai/langchain": "https://github.com/langchain-ai/langchain",
    "pytorch/pytorch": "https://github.com/pytorch/pytorch"
}

GITHUB_TOKEN = ""

def get_commits(repo_name):
    url = f"https://api.github.com/repos/{repo_name}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_version_dates():
    today = datetime.today()
    six_months_ago = today - timedelta(days=180)
    return today.strftime('%Y-%m-%d'), six_months_ago.strftime('%Y-%m-%d')

def filter_commits_by_date(commits, desired_date):
    for commit in commits:
        commit_date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').date()
        if commit_date <= desired_date:
            return commit['sha']
    return None

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
    for repo_name, repo_url in repos.items():
        print(f"Processing: {repo_name}")
        commits = get_commits(repo_name)
        
        # Get version dates
        today_str, six_months_ago_str = get_version_dates()
        today_date = datetime.strptime(today_str, '%Y-%m-%d').date()
        six_months_ago_date = datetime.strptime(six_months_ago_str, '%Y-%m-%d').date()
        
        # Filter commits by date
        latest_commit_sha = filter_commits_by_date(commits, today_date)
        older_commit_sha = filter_commits_by_date(commits, six_months_ago_date)
        
        # Define directories for versions
        base_clone_dir = f"./repos/{repo_name}"
        latest_dir = f"{base_clone_dir}_latest"
        older_dir = f"{base_clone_dir}_older"
        
        # Clone the repository and checkout the latest version
        if latest_commit_sha and not os.path.exists(latest_dir):
            clone_repo(repo_url, base_clone_dir)
            if not os.path.exists(latest_dir):
                os.mkdir(latest_dir)
            checkout_version(base_clone_dir, latest_commit_sha)
            os.rename(base_clone_dir, latest_dir)
            print(f"Latest version saved in {latest_dir}")

        # Checkout the older version
        if older_commit_sha and not os.path.exists(older_dir):
            clone_repo(repo_url, base_clone_dir)
            if not os.path.exists(older_dir):
                os.mkdir(older_dir)
            checkout_version(base_clone_dir, older_commit_sha)
            os.rename(base_clone_dir, older_dir)
            print(f"Older version saved in {older_dir}")

if __name__ == "__main__":
    main()