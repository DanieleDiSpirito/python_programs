import datetime
from sys import argv

today = datetime.date.today().strftime("%Y-%m-%d")

months = ["January", "February", "March", "April", "May", "June", "Sun", "July", "August", "September", "October", "November", "December", "Year's Day"]

def how_many_days(day):
    year = int(day.split("-")[0])
    first_january = datetime.datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
    day = datetime.datetime.strptime(day, "%Y-%m-%d")
    return (day - first_january).days + 1

def is_year_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def center_text(text, width):
    if len(text) >= width:
        return text
    total_padding = width - len(text)
    right_padding = total_padding // 2
    left_padding = total_padding - right_padding
    return ' ' * left_padding + text + ' ' * right_padding

def calendar(year: int, n: int): # calendar.calendar() analog
    day, month = get_date(n)
    s = f"                                  {year}                                  \n"
    leap_year = is_year_leap(year)
    for group in range(0, 14+1, 3):
        group_months = months[group:group+3]
        for m in group_months:
            if m == month:
                s += "\x1b[7m"
            s += center_text(m, 20)
            if m == month:
                s += "\x1b[0m"
            if (len(group_months) == 3 and m != group_months[2]) or (len(group_months) == 2 and m != group_months[1]):
                s += "      "
        s += "\n"
        for i in range(len(group_months)):
            if len(group_months) != 2 or i != 1: # exclude Year's Day
                s += "Mo Tu We Th Fr Sa Su"
            if i != len(group_months) - 1:
                s += "      "
        s += "\n"
        for jdx in range(4):
            for i in range(len(group_months)):
                if i != 1 or len(group_months) != 2: # exclude Year's Day
                    for idx in range(1, 8):
                        if (idx + jdx*7 + i*28 + group*28) == n:
                            s += "\x1b[7m"
                        s += f"{idx+jdx*7:>2}"
                        if (idx + jdx*7 + i*28 + group*28) == n:
                            s += "\x1b[0m"
                        if idx != 7:
                            s += " "
                    s += "      "
            s += "\n"
        if group == 3 and leap_year:
            s += " " * 52
            if month == "June" and day == 29:
                s += "\x1b[7m29\x1b[0m"
            else:
                s += "29"
            s += "\n"
            n -= 1
        s += "\n"
    return s

day = today
if len(argv) >= 2:
    day = argv[1]

year = int(day.split('-')[0])
n = how_many_days(argv[1])


def get_date(n: int, to_print = False):
    if n == 28*6 + 1 and is_year_leap(year):
        if to_print: print(f"{day} -> 29th of June")
        return [29, "June"]
    elif (n == 28*13 + 2 and is_year_leap(year)) or (n == 28*13 + 1 and not is_year_leap(year)):
        if to_print: print(f"{day} -> Year's Day")
        return [1, "Year's Day"]
    n -= n > 28*6 + 1 and is_year_leap(year)
    month = months[n // 28 if n % 28 != 0 else n // 28 - 1]
    Day = n % 28 if n % 28 != 0 else 28
    if to_print: print(f"{day} -> {Day}th {month}")
    return [day, month]

get_date(n, to_print=True)
print(calendar(year, n))