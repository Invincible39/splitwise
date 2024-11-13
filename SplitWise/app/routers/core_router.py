import logging
from fastapi import APIRouter

core_router = APIRouter(prefix="/core")


@core_router.get("/health")
def health_api():
    return {"success": True, "version": "0.0.1", "message": "Hello From Splitwise!"}
