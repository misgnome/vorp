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

migrations_dir_path = "migrations"
rollback_dir_path = os.path.join(migrations_dir_path, 'rollback')
rollback_dir = os.fsencode(rollback_dir_path)

with open(os.path.join(migrations_dir_path, '.last'), 'r') as last_run_file:
    last_run = last_run_file.read().strip()
    current_version = last_run

# roll back all migrations to (and including) target migration
# No arguments rolls back last migration
try:
    target = sys.argv[1]
except IndexError as e:
    target = current_version

conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT)

rollback_files = sorted(os.listdir(rollback_dir), reverse=True)
for i,_file in enumerate(rollback_files):
     filename = os.fsdecode(_file)
     if filename.endswith(".pgsql") and filename >= target and filename <= current_version:
        print("Rolling back {}...".format(filename))
        cur = conn.cursor()
        cur.execute(open(os.path.join(rollback_dir_path, filename),
            'r').read())
        conn.commit()
        cur.close()


        try:
            last_run = os.fsdecode(rollback_files[i+1])
        except IndexError:
            last_run = '00000000000.pgsql'
        # important that it is here in case migration fails
        with open(os.path.join(migrations_dir_path, '.last'), 'w') as last_run_file:
            last_run_file.write(last_run)

conn.close()

