pipeline {
    agent any
    options {
        timeout(time: 20, unit: 'SECONDS')
    }
    stages {
        stage('Say Hello') {
            steps {
                sh 'echo Hello'
            }
        }
    }
}
