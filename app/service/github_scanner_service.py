import json
from typing import Optional
from fastapi import HTTPException

import httpx


class GithubScannerService:
    def __init__(self):
        self.api_url = "https://githubscanner.com/collectGitHubData"
        self.headers = {
                        'authority': 'githubscanner.com',
                        'accept': '*/*',
                        'accept-language': 'en-GB,en;q=0.6',
                        'content-type': 'application/json',
                        'origin': 'https://githubscanner.com',
                        'referer': 'https://githubscanner.com/',
                        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'sec-gpc': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        }
        self.headers_get = {
                            'authority': 'githubscanner.com',
                            'accept': '*/*',
                            'accept-language': 'en-GB,en;q=0.5',
                            'referer': 'https://githubscanner.com/',
                            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            'sec-gpc': '1',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                            }   
    async def get_user_metadata_token(self, username:str) -> str:
        payload = json.dumps({
                "usernames": [
                    username
                ],
                "keywords": [
                    ""
                ]
                })
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url=self.api_url , headers=self.headers, data=payload)
                if resp.status_code == 404:
                    raise HTTPException(status_code=404, detail=" not found")
                elif resp.status_code != 200:
                    raise HTTPException(status_code=resp.status_code, detail="GithubScanner.com REST API error")
        except httpx.RequestError as e:
            print(f'exception: {e}')
            raise HTTPException(status_code=503, detail="GithubScanner.com API Service not available")
        return resp.text
    
    async def get_user_metadata_by_token(self, token:str)->Optional[str]:
        params = {"token":token}
        try:
            async with httpx.AsyncClient() as client:
                #resp = await client.get(url=f'self.api_url?token={token}' , headers=self.headers_get)
                resp = await client.get(url='https://githubscanner.com/collectGitHubDataResult', headers=self.headers_get, params=params)
                #print(f'resp status code: {resp.status_code}')
                if resp.status_code == 404:
                    return None
                elif resp.status_code != 200:
                    raise HTTPException(status_code=resp.status_code, detail="GithubScanner.com REST API error")
        except httpx.RequestError as e:
            print(f'exception: {e}')
            raise HTTPException(status_code=503, detail="GithubScanner.com API Service not available")
        return resp.text