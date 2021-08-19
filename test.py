import datetime

now = datetime.datetime.now()
start_hour = 10
start_min = 0
end_hour = 13
end_min = 10
start_day = 0
end_day = 6


def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        a = nowTime >= startTime and nowTime <= endTime
        print(endTime)
        return nowTime >= startTime and nowTime <= endTime
    else:
        # Over midnight:
        return nowTime >= startTime or nowTime <= endTime


while True:
    a = isNowInTimePeriod(datetime.time(start_hour, start_min),
                          datetime.time(end_hour, end_min), now.time())
    print(a)
    if a and start_day <= now.weekday() <= end_day:
        print("done")
        break
# print(now.weekday())
