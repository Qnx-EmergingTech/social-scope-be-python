from datetime import datetime
from fastapi import APIRouter, WebSocket
import asyncio
from DBmodels.CommentModel import PageComment
from core.database_celery_sync import SessionLocal
from sqlalchemy import select, desc
import redis
import json

router = APIRouter()
redisNotify = redis.Redis(host="redis",port=6379, db=0)

connections = []

@router.websocket("/notifications-comments")
async def websocket_notifications(ws: WebSocket):
    await ws.accept()
    print("CONNECTED")

    
    pubsub = redisNotify.pubsub() 
    pubsub.subscribe("new_comments")

    try:
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message: 
                data = json.loads(message["data"]) 
                await ws.send_text( f"New message: {data}" )
            else:
                await ws.send_text(f"No new Comments")
        

            await asyncio.sleep(5)

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print("Connection closed")
        await ws.close()
