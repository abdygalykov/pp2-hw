from datetime import datetime, timedelta

curr_time = datetime.today()

print("initial date:" + str(curr_time))

newtime = curr_time - timedelta(days = 5)

print("New time: " + str(newtime))


