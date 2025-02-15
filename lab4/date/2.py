from datetime import datetime, timedelta

curr_day = datetime.today()

print("Current day " + str(curr_day))

yesterday = curr_day - timedelta(days=1)

print("Yesterday " + str(yesterday))

tomorrow = curr_day + timedelta(days=1)

print("Tomorrow " + str(tomorrow))

