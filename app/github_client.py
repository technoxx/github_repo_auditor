import base64
from fastapi import HTTPException, Depends
from starlette import status
import httpx
from .config import GITHUB_API, HEADERS

class GithubClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_repo(self, owner, repo_name):
        url = f"{GITHUB_API}/{owner}/{repo_name}"
        response = await self.client.get(url, headers=HEADERS)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Repository not found or private")
        response.raise_for_status()
        return response.json()

    async def get_tree(self, owner, repo_name):
        url = f"{GITHUB_API}/{owner}/{repo_name}/git/trees/HEAD"
        response = await self.client.get(url, headers=HEADERS, params={"recursive": 1})
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Repository not found or private")
        response.raise_for_status()
        return response.json()['tree']


    async def get_file_content(self, owner, repo_name, path):
        url = f"{GITHUB_API}/{owner}/{repo_name}/contents/{path}"
        response = await self.client.get(url, headers=HEADERS)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Repository not found or private")
        response.raise_for_status()
        response_data = response.json()
        content = base64.b64decode(response_data["content"]).decode('utf-8')
        return content

    async def get_commits(self, owner, repo_name):
        url = f"{GITHUB_API}/{owner}/{repo_name}/commits"
        response = await self.client.get(url, headers=HEADERS, params={"per_page": 50},)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Repository not found or private") 
        response.raise_for_status()
        return response.json()


