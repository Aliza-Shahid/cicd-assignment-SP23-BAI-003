pipeline {
    agent any

    environment {
        APP_IMAGE = "webapp-sp23-bai-003"
        TEST_IMAGE = "selenium-agent-sp23-bai-003"
        STAGING_CONTAINER = "staging-sp23-bai-003"
        PROD_CONTAINER = "prod-sp23-bai-003"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Package') {
            steps {
                sh 'docker build -t ${APP_IMAGE}:${BUILD_NUMBER} .'
                sh 'docker build -t ${TEST_IMAGE}:${BUILD_NUMBER} ./tests'
            }
        }

        stage('Start Staging') {
            steps {
                sh '''
                    docker rm -f ${STAGING_CONTAINER} || true
                    docker run -d --name ${STAGING_CONTAINER} -p 8081:80 ${APP_IMAGE}:${BUILD_NUMBER}
                    sleep 3
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    mkdir -p reports
                    chmod 777 reports
                    docker run --rm \
                        --add-host=host.docker.internal:host-gateway \
                        -e APP_URL="http://host.docker.internal:8081" \
                        -v "${WORKSPACE}/reports:/app/reports" \
                        ${TEST_IMAGE}:${BUILD_NUMBER}
                '''
            }
            post {
                always {
                    junit 'reports/results.xml'
                    sh 'docker rm -f ${STAGING_CONTAINER} || true'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f ${PROD_CONTAINER} || true
                    docker run -d --name ${PROD_CONTAINER} --restart unless-stopped -p 8082:80 ${APP_IMAGE}:${BUILD_NUMBER}
                '''
            }
        }
    }
}