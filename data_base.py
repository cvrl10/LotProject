import csv
import pandas as pd
import re
import calendar
from datetime import date

txt_file = open('inventory.txt', 'r')
csv_file = open('inventory.csv', 'w', newline='')
out = csv.writer(csv_file)
out.writerow(['standard', 'lot#', 'expiration date'])

for row in txt_file.readlines():
    row = row.split()
    standard = row.pop(0)
    lot = row.pop(0)
    exp = ' '.join(row)
    out.writerow([standard, lot, exp])

txt_file.close()
csv_file.close()

df = pd.read_csv('inventory.csv')


def str_to_date(s):
    pattern = re.compile(r'(?P<month>[A-Z]{3,9}) (?P<day>[0-9]{1,2}), (?P<year>[0-9]{4})', re.IGNORECASE)
    match = pattern.fullmatch(s)
    if match:
        i = [index for index, month in enumerate(calendar.month_abbr) if month == match['month'][0:3]]
        return date(int(match['year']), i.pop(), int(match['day']))


def expired(expiration_date):
    return expiration_date < date.today()


df['expiration date'] = df['expiration date'].apply(str_to_date)
df['expired'] = df['expiration date'].apply(expired)
print(df.to_string())