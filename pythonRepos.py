import requests

GITHUB_TOKEN = ''

def fetch_top_repositories():
    url = 'https://api.github.com/graphql'
    headers = {
        'Authorization': f'Bearer {GITHUB_TOKEN}'
    }
    query = """
    {
      search(query: "language:Python stars:>1", type: REPOSITORY, first: 12) {
        edges {
          node {
            ... on Repository {
              name
              stargazers {
                totalCount
              }
              url
            }
          }
        }
      }
    }
    """
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"deu ruim {response.status_code}")

def print_repositories(repositories):
    for i, edge in enumerate(repositories['data']['search']['edges'], 1):
        repo = edge['node']
        print(f"{i}. {repo['name']}")
        print(f"   Stars: {repo['stargazers']['totalCount']}")
        print(f"   URL: {repo['url']}\n")

if __name__ == '__main__':
    repositories = fetch_top_repositories()
    print_repositories(repositories)