pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'apurwasingh/flask'
        DOCKER_IMAGE_TAG = 'latest'
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
                    docker.build("test-image")
                    sh "docker run -d --name test_flask -p 8000:7000 test-image"
                    sleep 5
                    def code = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000", returnStdout: true).trim()
                    sh "docker stop test_flask && docker rm test_flask"
                    if (code != '200') {
                        error("❌ App test failed with HTTP $code")
                    }
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
                    sh "docker exec -u root ansible ansible-playbook /root/deploy.yml"
                }
            }
        }
    }
}

