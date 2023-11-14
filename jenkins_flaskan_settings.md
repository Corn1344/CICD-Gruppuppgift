1. 
   python3 -m venv backend/.venv
   . backend/.venv/bin/activate
   pip install -r backend/requirements.txt
   pylint /var/jenkins_home/workspace/<projekt_name>/backend/pingurl
   

2. 
   docker build -t flask_app backend/.
   docker stop flask_application
   docker rm flask_application
   docker run -d --name flask_application flask_app -p 5000:5000 
   echo "Running on: "
   docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' flask_application


3. Poll SCM
   * * * * *
