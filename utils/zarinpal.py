import requests

MERCHANT_ID = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX" # کد مرچنت زرین‌پال
CALLBACK_URL = "https://vyoel-5-202-36-16.run.pinggy-free.link"

def send_request(amount, description, user_id, plan_id):
    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount * 10, # زرین‌پال مبالغ را به ریال دریافت می‌کند
        "callback_url": f"{CALLBACK_URL}?user_id={user_id}&plan_id={plan_id}",
        "description": description,
    }
    headers = {'content-type': 'application/json'}
    try:
        res = requests.post("https://api.zarinpal.com/pg/v4/payment/request.json", json=data, headers=headers).json()
        if res['data']['code'] == 100:
            return True, f"https://www.zarinpal.com/pg/StartPay/{res['data']['authority']}"
        return False, "خطا در ساخت لینک بانکی"
    except Exception as e:
        return False, str(e)

def verify_payment(authority, amount):
    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount * 10,
        "authority": authority,
    }
    headers = {'content-type': 'application/json'}
    try:
        res = requests.post("https://api.zarinpal.com/pg/v4/payment/verify.json", json=data, headers=headers).json()
        if res['data']['code'] in [100, 101]: # 100: موفق، 101: قبلاً تایید شده
            return True, res['data']['ref_id']
        return False, res['errors']['message']
    except Exception as e:
        return False, str(e)