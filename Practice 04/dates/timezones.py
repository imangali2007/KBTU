# Note: timezones often require external libraries like pytz, but here is basic usage
import datetime

utc_time = datetime.datetime.now(datetime.timezone.utc)
print(utc_time)

offset = datetime.timedelta(hours=5)
tz = datetime.timezone(offset)
local_time = datetime.datetime.now(tz)
print(local_time)
