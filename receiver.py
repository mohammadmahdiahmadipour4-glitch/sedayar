import requests
import json
import time
from db.base import SessionLocal
from db.models.queue import UpdateQueue
from main import bot

print("📥 Receiver is ON: Only saving raw messages to Database Queue...")
bot.remove_webhook() 
offset = None

while True:
    try:
        url = f"https://api.telegram.org/bot{bot.token}/getUpdates"
        params = {'timeout': 20}
        if offset:
            params['offset'] = offset
            
        response = requests.get(url, params=params).json()
        
        if response.get('ok') and response.get('result'):
            updates = response['result']
            
            with SessionLocal() as session:
                for up in updates:
                    json_string = json.dumps(up)
                    # ذخیره با وضعیت پردازش‌نشده
                    new_update = UpdateQueue(update_json=json_string, is_processed=False)
                    session.add(new_update)
                session.commit()
            
            print(f"✅ {len(updates)} message(s) safely stored in Database Queue!")
            offset = updates[-1]['update_id'] + 1
            
    except Exception as e:
        print(f"Error in receiver: {e}")
        time.sleep(5)