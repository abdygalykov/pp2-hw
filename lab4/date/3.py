from datetime import datetime

today = datetime.now()

res = today.strftime("%Y-%m-%d %H:%M:%S")

print(res)