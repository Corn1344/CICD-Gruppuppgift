pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                git url: 'https://github.com/Corn1344/CICD-Gruppuppgift', branch: 'main'
                sh './build.sh'
            }
        }
        stage('Pytest') {
            steps {
                sh './pytest.sh'
            }
        }
        stage('Test Lint') {
            steps {
                sh './test_lint.sh'
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
