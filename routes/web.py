from functools import lru_cache
import json
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from config import Settings
import requests
page_router = APIRouter()

token = None

@lru_cache
def get_settings():
    return Settings()


async def authFedex(settings:Annotated[Settings, Depends(get_settings)]):
  # print(settings)
  try:
    inputpayload = {
      'grant_type':'client_credentials',
      'client_id':settings.FEDEX_API_KEY,
      'client_secret':settings.FEDEX_SECRET_KEY
    }
    headers = {
      'content-type':'application/x-www-form-urlencoded'
    }
    response = requests.post('{}/oauth/token'.format(settings.FEDEX_BASE_API_URL),data=inputpayload,headers=headers)
    # print(token,'This is token')
    return response.json()
    

  except Exception as e:
    print("error authenticating with fedex api. The error is ",e)


async def getInfo(token: str, settings: Annotated[Settings, Depends(get_settings)]):
  try:
    headers = {
      'content-type':'application/json',
      'authorization':f'Bearer {token}'
    }

    payload = json.dumps({
      'includeDetailedScans':True,
      'trackingInfo':[
        {
          "trackingNumberInfo": {
            "trackingNumber": "231300687629630" # Mock tracking number
          }
        }
      ]
    })

    response  = requests.post('{}/track/v1/trackingnumbers'.format(settings.FEDEX_BASE_API_URL),data=payload,headers=headers)
    print(response)
    return response.json()
  except Exception as e:
    print('There is some error',e)

@page_router.get('/getinfo')
async def getinfo(settings: Annotated[Settings, Depends(get_settings)]):
  authres = await authFedex(settings)
  response = await getInfo(settings)
  return {
    "order info":response
  }



@page_router.get('/track')
async def track(settings:Annotated[Settings, Depends(get_settings)]):
  authres = await authFedex(settings)
  token = authres['access_token']
  response = await getInfo(token, settings)
  return {
    "orderinfo":response
  }


