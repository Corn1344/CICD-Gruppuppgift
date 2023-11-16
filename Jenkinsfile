pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                git url: 'https://github.com/nackc8/cicd-grp--ga-pa-flask-an', branch: 'main'
                sh '''
                python3 -m venv backend/.venv
                . backend/.venv/bin/activate
                pip install -r backend/requirements.txt
                '''
            }
        }
        stage('Pytest') {
            steps {
                sh '''
                python3 -m venv backend/.venv
                . backend/.venv/bin/activate
                pytest backend/
                '''
            }
        }
        stage('Test Lint') {
            steps {
                sh '''
                python3 -m venv backend/.venv
                . backend/.venv/bin/activate
                pylint backend/
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                docker build -t flask_app backend/.
                if [ "$(docker ps -a -q -f name=flask_application)" ]; then
                    docker stop flask_application
                    docker rm flask_application
                fi
                docker run -d --name flask_application flask_app -p 5000:5000 
                IP_ADDR=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' flask_application)
                echo "Flask app running on: http://$IP_ADDR:5000"
                '''

            }
        }
    }
}
