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
            sh 'docker run -d --name test_flask --network jenkins_net test-image'
            sleep 5
            sh 'docker ps -q -f name=test_flask || (echo "Container crashed" && exit 1)'
            sh 'docker run --rm --network jenkins_net curlimages/curl:latest curl -f http://test_flask:7000'
            sh 'docker stop test_flask || true'
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

