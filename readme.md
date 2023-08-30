Installation
============
 - `pip install -r requirements.txt`

Windows
=======
 - `set FLASK_APP=run.py`
 - `flask run`
 
Linux
======
 - `. venv/bin/activate`
 - `FLASK_APP=run.py flask run`
 
 
Docker
======
**Build**
- `docker build . -t nasefirmy`

**Run**
- `docker run -d -p 5000:5000 nasefirmy`