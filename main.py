import requests
import time
import logging

line_notify_token = 'line notify token'
p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=551&limit=1'
last_earthquake_id = None
scale_dict = {10: '1', 20: '2', 30: '3', 40: '4', 45: '5弱', 50: '5強', 55: '6弱', 60: '6強', 70: '7'}

# ロギングの設定
logging.basicConfig(level=logging.INFO)

while True:
    try:
        response = requests.get(p2pquake_url)
        response.raise_for_status()
        data = response.json()

        if data:
            latest_earthquake = data[0]
            earthquake_id = latest_earthquake['id']

            if earthquake_id != last_earthquake_id:
                last_earthquake_id = earthquake_id
                hypocenter_name = latest_earthquake['earthquake']['hypocenter']['name']
                magnitude = latest_earthquake['earthquake']['hypocenter']['magnitude']
                max_scale = latest_earthquake['earthquake']['maxScale']
                earthquake_time = latest_earthquake['earthquake']['time']
                max_scale_str = scale_dict.get(max_scale, '不明')

                message = f"地震情報\n震源地: {hypocenter_name}\nマグニチュード: {magnitude}\n最大震度: {max_scale_str}\n発生時刻: {earthquake_time}"
                headers = {'Authorization': f'Bearer {line_notify_token}'}
                payload = {'message': message}
                line_notify_url = 'https://notify-api.line.me/api/notify'
                requests.post(line_notify_url, headers=headers, data=payload)

                logging.info("新しい地震を検出し、通知を送信しました。")
    except requests.exceptions.RequestException as e:
        logging.error(f"地震データの取得中にエラーが発生しました: {e}")

    time.sleep(600)