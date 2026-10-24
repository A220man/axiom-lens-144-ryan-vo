"""Device management endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Mock device data (production: query ADB)
_devices: dict[str, dict] = {}


class DeviceResponse(BaseModel):
    id: str
    name: str
    platform: str
    status: str
    properties: dict


@router.get("", response_model=list[DeviceResponse])
async def list_devices():
    return [DeviceResponse(**d) for d in _devices.values()]


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str):
    if device_id not in _devices:
        raise HTTPException(status_code=404, detail="Device not found")
    return DeviceResponse(**_devices[device_id])


@router.post("/{device_id}/connect")
async def connect_device(device_id: str):
    # Mock connection
    if device_id not in _devices:
        _devices[device_id] = {
            "id": device_id,
            "name": f"Device {device_id}",
            "platform": "android",
            "status": "connected",
            "properties": {},
        }
    _devices[device_id]["status"] = "connected"
    return DeviceResponse(**_devices[device_id])


@router.post("/{device_id}/disconnect")
async def disconnect_device(device_id: str):
    if device_id not in _devices:
        raise HTTPException(status_code=404, detail="Device not found")
    _devices[device_id]["status"] = "disconnected"
    return DeviceResponse(**_devices[device_id])
