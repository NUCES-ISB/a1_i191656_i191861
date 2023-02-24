pipeline {
    agent any
    options {
        timeout(time: 200, unit: 'SECONDS')
    }
    stages {
        stage('Install dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Install Black') {
            steps {
                bat 'pip install black'
            }
        }
        stage('Run Black') {
            steps {
                bat 'python -m black --include "\.py" ./'
            }
        }
        stage('Install Flake8') {
            steps {
                bat 'pip install flake8'
            }
        }
        stage('Run Flake8') {
            steps {
                bat 'flake8 ./'
            }
        }        
    }
}
