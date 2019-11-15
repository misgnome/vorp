#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import psycopg2
import sys

load_dotenv()

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']

conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT)

migrations_dir_path = "migrations"
change_dir_path = os.path.join(migrations_dir_path, 'change') 
change_dir = os.fsencode(change_dir_path)

try:
    with open(os.path.join(migrations_dir_path, '.last'), 'r') as last_run_file:
        last_run = last_run_file.read().strip()
except FileNotFoundError as e:
    last_run = '00000000000.pgsql'

for _file in sorted(os.listdir(change_dir)):
     filename = os.fsdecode(_file)
     if filename.endswith(".pgsql") and filename > last_run:
        print("Running migration {}...".format(filename))
        cur = conn.cursor()
        cur.execute(open(os.path.join(change_dir_path, filename),
            'r').read())
        conn.commit()
        cur.close()

        last_run = filename
        # important that it is here in case migration fails
        with open(os.path.join(migrations_dir_path, '.last'), 'w') as last_run_file:
            last_run_file.write(last_run)

conn.close()

