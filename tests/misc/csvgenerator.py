import csv
import random
import string

# Generate random company names
def generate_company_name():
    return ''.join(random.choices(string.ascii_letters, k=10))

# Generate random stock symbols
def generate_stock_symbol():
    return ''.join(random.choices(string.ascii_uppercase, k=5))

# Generate random exchange markets
def generate_exchange_market():
    return random.choice(['NYSE', 'NASDAQ', 'LSE', 'TSX', 'HKEX'])

# Generate random dates of listing
def generate_date_of_listing():
    return f'{random.randint(1990, 2022)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'

# Generate random outstanding shares
def generate_outstanding_shares():
    return random.randint(1000000, 100000000)

# Generate 1,000,000 records
records = []
for i in range(1000000):
    company_name = generate_company_name()
    stock_symbol = generate_stock_symbol()
    exchange_market = generate_exchange_market()
    date_of_listing = generate_date_of_listing()
    outstanding_shares = generate_outstanding_shares()
    record = [company_name, stock_symbol, exchange_market, date_of_listing, outstanding_shares]
    records.append(record)

# Write records to CSV file
with open('companies.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['NAME OF COMPANY', 'SYMBOL', 'Exchange Market', 'DATE OF LISTING', 'Outstanding Shares'])
    writer.writerows(records)
