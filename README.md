# V0RP

The basketball search engine.


## Getting started


- install virtualenv wrapper, using the steps
[here](https://virtualenvwrapper.readthedocs.io/en/latest/)
- create a virtualenv
```bash
mkvirtualenv -p python3 vorp
workon vorp
```
- install required packages
```bash
cd <top level of this repo>
pip install -r requirements.txt
```
- make sure postgres is installed and create the database
- create a .env file with your db credentials, ie,
```bash
export DB_NAME=vorp
export DB_USER=vorp
export DB_PASS=v0rp
export DB_HOST=localhost
export DB_PORT=5432
```
- source the file
```bash
source .env
```
- Run migrations
```bash
cd db 
python migrate.py
cd ..
```
- Run app.py
```bash
python app.py
```
