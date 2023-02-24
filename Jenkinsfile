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
        stage('Store paths of all python files in repo') {
            steps {
                bat 'python get_python_file_paths.py'
            }
        }
        stage('Install black') {
            steps {
                bat 'pip install black'
            }
        }
        stage('Run black') {
            steps {
                bat 'For //f %i in (python_file_paths.txt) do python -m black %i'
            }
        }
        stage('Install Flake8') {
            steps {
                bat 'pip install flake8'
            }
        }
        stage('Run Flake8') {
            steps {
                bat 'For //f %i in (python_file_paths.txt) do flake8 %i'
            }
        }        
    }
}
