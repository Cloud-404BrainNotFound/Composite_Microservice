import httpx
from typing import Optional, Any, Dict
from fastapi import HTTPException
import asyncio

class ServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    async def _make_async_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e))
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    def _make_sync_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        with httpx.Client() as client:
            try:
                response = client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e))
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    async def get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        return await self._make_async_request("GET", endpoint, params=params, headers=headers)

    def get_sync(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        return self._make_sync_request("GET", endpoint, params=params, headers=headers)

    async def post(
        self,
        endpoint: str,
        data: dict,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        return await self._make_async_request("POST", endpoint, data=data, params=params, headers=headers)

    def post_sync(
        self,
        endpoint: str,
        data: dict,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        return self._make_sync_request("POST", endpoint, data=data, params=params, headers=headers)

    async def put(
        self,
        endpoint: str,
        data: dict,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        return await self._make_async_request("PUT", endpoint, data=data, params=params, headers=headers)

    def put_sync(
        self,
        endpoint: str,
        data: dict,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        return self._make_sync_request("PUT", endpoint, data=data, params=params, headers=headers)

    async def patch(
        self,
        endpoint: str,
        data: dict,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        return await self._make_async_request("PATCH", endpoint, data=data, params=params, headers=headers)

    def patch_sync(
        self,
        endpoint: str,
        data: dict,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        return self._make_sync_request("PATCH", endpoint, data=data, params=params, headers=headers)

    async def delete(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        return await self._make_async_request("DELETE", endpoint, params=params, headers=headers)

    def delete_sync(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Any:
        return self._make_sync_request("DELETE", endpoint, params=params, headers=headers)
