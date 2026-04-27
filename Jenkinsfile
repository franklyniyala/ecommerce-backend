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
    }

    post {
        success {
            echo ' ✅ SonarQube Analysis Successful!'
        }
        failure {
            echo ' ❌ SonarQube Analysis Failed. Please check the logs for details.'
        }
    }
}