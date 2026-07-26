pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }


        stage('Verify Tools') {
            steps {
                sh '''
                python3 --version
                git --version
                docker --version
                trivy --version
                '''
            }
        }


        stage('Test Upload Service') {
            steps {
                sh '''
                cd upload-service

                python3 -m venv venv

                . venv/bin/activate

                pip install --upgrade pip

                pip install -r requirements.txt

                python -m pytest tests

                deactivate
                '''
            }
        }


        stage('Test Converter Service') {
            steps {
                sh '''
                cd converter-service

                python3 -m venv venv

                . venv/bin/activate

                pip install --upgrade pip

                pip install -r requirements.txt

                python -m pytest tests

                deactivate
                '''
            }
        }


        stage('Build Upload Service Image') {
            steps {
                sh '''
                docker build \
                -t upload-service:latest \
                ./upload-service
                '''
            }
        }


        stage('Build Converter Service Image') {
            steps {
                sh '''
                docker build \
                -t converter-service:latest \
                ./converter-service
                '''
            }
        }


        stage('Trivy Scan Upload Service') {
            steps {
                sh '''
                trivy image upload-service:latest
                '''
            }
        }


        stage('Trivy Scan Converter Service') {
            steps {
                sh '''
                trivy image converter-service:latest
                '''
            }
        }

    }


    post {

        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }

    }

}