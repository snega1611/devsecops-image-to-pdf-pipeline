pipeline {

    agent any
    
    environment {
    DOCKER_REPO = "dockerhubusername"
    }

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
                -t $DOCKER_REPO/upload-service:${BUILD_NUMBER} \
                -t $DOCKER_REPO/upload-service:latest \
                ./upload-service
                '''
            }
        }


        stage('Build Converter Service Image') {
            steps {
                sh '''
                docker build \
                -t $DOCKER_REPO/converter-service:${BUILD_NUMBER} \
                -t $DOCKER_REPO/converter-service:latest \
                ./converter-service
                '''
            }
        }


        stage('Trivy Scan Upload Service') {
            steps {
                sh '''
                trivy image $DOCKER_REPO/upload-service:${BUILD_NUMBER}
                '''
            }
        }


        stage('Trivy Scan Converter Service') {
            steps {
                sh '''
                trivy image $DOCKER_REPO/converter-service:${BUILD_NUMBER}
                '''
            }
        }

        stage('Push Images to Docker Hub') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                    docker push $DOCKER_REPO/upload-service:${BUILD_NUMBER}
                    docker push $DOCKER_REPO/upload-service:latest

                    docker push $DOCKER_REPO/converter-service:${BUILD_NUMBER}
                    docker push $DOCKER_REPO/converter-service:latest

                    docker logout
                    '''

                }

            }

        }

        stage('Update GitOps Repo') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-gitops',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {

                    sh '''
                    rm -rf image-to-pdf-gitops

                    git clone https://$GIT_USER:$GIT_TOKEN@github.com/snega1611/image-to-pdf-gitops.git

                    cd image-to-pdf-gitops

                    git config user.name "your name"
                    git config user.email "youe email id"

                    sed -i "s|image: dockerhubusername/upload-service:.*|image: dockerhubusername/upload-service:${BUILD_NUMBER}|g" k8s/upload-deployment.yaml

                    sed -i "s|image: dockerhubusername/converter-service:.*|image: dockerhubusername/converter-service:${BUILD_NUMBER}|g" k8s/converter-deployment.yaml

                    git add .

                    git commit -m "Update image tag to ${BUILD_NUMBER}" || echo "No changes to commit"

                    git push
                    '''
                }
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
