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
                    // Build the Docker image
                    docker.build("test-image")

                    // Create a Docker network if it doesn't exist
                    sh 'docker network create test_net || true'

                    // Run the test container in that network
                    sh 'docker run -d --rm --name test_flask --network test_net test-image'

                    // Give the container some time to start
                    sleep 5

                    // Run curl from another container in the same network
                    def response = sh(
                        script: 'docker run --rm --network test_net curlimages/curl:latest curl -s -o /dev/null -w "%{http_code}" http://test_flask:7000',
                        returnStdout: true
                    ).trim()

                    // Stop the test container manually (optional since --rm is used)
                    sh 'docker stop test_flask || true'

                    // Fail the build if the response is not 200
                    if (response != '200') {
                        error "Health check failed with HTTP code: ${response}"
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

