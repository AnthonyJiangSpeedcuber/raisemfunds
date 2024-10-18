import sqlite3
import csv

conn = sqlite3.connect('main.db')
cursor = conn.cursor()

def append_data_from_csv(csv_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
            INSERT INTO posts (name, place_of_origin, story, amount_raised)
            VALUES (?, ?, ?, ?)
            ''', (row['name'], row['place_of_origin'], row['story'], float(row['amount_raised'])))
    
    conn.commit()
    print(f"Data from {csv_file} has been appended to the database.")

csv_file_path = input()

append_data_from_csv(csv_file_path)

conn.close()
