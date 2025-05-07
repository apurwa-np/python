pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'apurwasingh/flask'
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                script {
                    //docker.build("test-image")
                    sh 'docker run -d --rm --name test_flask --network jenkins_net test-image'
                    sleep 5

                    def running = sh(script: 'docker ps -q -f name=test_flask', returnStdout: true).trim()
                    if (!running) {
                        error "test_flask container exited early. Likely app.py has errors."
                    }

                    sh 'docker run --rm --network jenkins_net curlimages/curl:latest curl -f http://test_flask:7000'
                    sh 'docker stop test_flask || true'
                }
            }
        }

        stage('Security Scan') {
            steps {
                script {
                    // Save the image locally
                    sh 'docker save -o test-image.tar test-image'

                    // Scan using Trivy in a container
                    sh '''
                        docker run --rm \
                          -v $(pwd):/root/scan \
                          aquasec/trivy:latest image --input /root/scan/test-image.tar \
                          --exit-code 1 --severity HIGH,CRITICAL
                    '''
                }
            }
        }

        stage('Build & Push') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh "docker exec -u flaskuser ansible ansible-playbook /root/deploy.yml"
                }
            }
        }
    }
}