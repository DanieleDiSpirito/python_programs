import datetime
from sys import argv

today = datetime.date.today().strftime("%Y-%m-%d")

def how_many_days(day):
    year = int(day.split("-")[0])
    first_january = datetime.datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
    day = datetime.datetime.strptime(day, "%Y-%m-%d")
    return (day - first_january).days + 1

def is_year_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

day = today
if len(argv) >= 2:
    day = argv[1]

year = int(day.split('-')[0])
n = how_many_days(argv[1])
print(n - 28*6 - 1)

if n == 28*6 + 1 and is_year_leap(year):
    print(f"{day} -> 29-06 29th of June")
    exit(0)
elif (n == 28*13 + 2 and is_year_leap(year)) or (n == 28*13 + 1 and not is_year_leap(year)):
    print(f"{day} -> Y-Y Year's Day")
    exit(0)

months = ["January", "February", "March", "April", "May", "June", "Sun", "July", "August", "September", "October", "November", "December"]

n -= n > 28*6 + 1 and is_year_leap(year)

month = months[n // 28 if n % 28 != 0 else n // 28 - 1]
Day = n % 28 if n % 28 != 0 else 28
print(f"{day} -> {Day}th {month}")