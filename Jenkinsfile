pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/dipdaiict/fastapi-flash.git'  // Replace with your repository URL
        DOCKER_IMAGE = 'dippdatel/fastapi-flash-build'  // Replace with your Docker image name
        DOCKER_CREDENTIALS_ID = 'docker-credentials-id'  // Replace with your Docker Hub credentials ID
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: "${env.REPO_URL}", branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${env.DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${env.DOCKER_CREDENTIALS_ID}") {
                        dockerImage.push('latest')
                        dockerImage.push("${env.BUILD_ID}")
                    }
                }
            }
        }

    //     stage('Deploy to Instance') {
    //         steps {
    //             sshagent([env.INSTANCE_SSH]) {
    //                 sh """
    //                     ssh -o StrictHostKeyChecking=no user@your-instance-ip <<EOF
    //                     docker pull ${env.DOCKER_IMAGE}:${env.BUILD_ID}
    //                     docker stop python-app || true
    //                     docker rm python-app || true
    //                     docker run -d --name python-app -p 80:80 ${env.DOCKER_IMAGE}:${env.BUILD_ID}
    //                     EOF
    //                 """
    //             }
    //         }
    //     }
    // }

    post {
        always {
            cleanWs()
        }
    }
}
