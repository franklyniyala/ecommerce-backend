pipeline {
    agent any

    stages {
        stage('Checkout code') {
            steps {
                git branch: 'main',
                credentialsId: 'GITHUB_LOGIN',
                url: 'https://github.com/franklyniyala/ecommerce-backend.git'
            }

        }

        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        docker run --rm \
                        -e SONAR_TOKEN=$SONAR_TOKEN \
                        -v $(pwd):/usr/src \
                        sonarsource/sonar-scanner-cli \
                        -Dsonar.projectKey=frank-org_ecommerce-backend \
                        -Dsonar.organization=frank-org \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=https://sonarcloud.io \
                    '''

                }
            }
        }

        stage ('Build Image') {
            steps {
                sh 'docker build -t ekenefranklyn/ecommerce-backend:latest .'
            }
        }

        stage ('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'DOCKER_LOGIN',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }
            }
        }

        stage ('Push Image to DockerHub') {
            steps {
                sh 'docker push ekenefranklyn/ecommerce-backend:latest'
            }
        }

        stage ('Deploy Application') {
            steps {
                sh '''
                docker run -d --name ecommerce-backend -p 2500:8080 ekenefranklyn/ecommerce-backend:latest
                '''
            }
        }
    }
    

    post {
        success {
            echo ' ✅ SonarQube Analysis Successful!'
            echo ' ✅ Docker Image Built and Pushed Successfully!'
            echo ' ✅ Application Deployed Successfully!'
        }
        failure {
            echo ' ❌ SonarQube Analysis Failed. Please check the logs for details.'
        }
    }
}