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
                sh './deploy.sh'
            }
        }
        stage('API Tests') {
            steps {
                sh './curltests.sh'
            }
        }
    }
}
