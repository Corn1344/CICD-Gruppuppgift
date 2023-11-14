1. ```
python3 -m venv backend/.venv
. backend/.venv/bin/activate
pip install -r backend/requirements.txt
pylint /var/jenkins_home/workspace/<projekt_name>/backend/pingurl
```

2. docker build -t flask_app backend/.

3. Poll SCM
* * * * *