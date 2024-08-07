pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'jenkins-dockerhub-integration'
        DOCKER_IMAGE_NAME = 'dippdatel/jenkins-test'
        DOCKER_TAG = 'latest'
        GIT_REPO_URL = 'https://github.com/dipdaiict/fastapi-flash.git'
        SONARQUBE_URL = 'http://localhost:9000'
        SONARQUBE_SERVER = 'SonarServer'
        SONARQUBE_TOKEN = credentials('sonarqube-jenkins-integration-token') // Ensure this ID is correct
        SONARQUBE_SCANNER = "sonarscanner installation" // Ensure this name matches your SonarQube Scanner installation in Jenkins
        SONAR_PROJ_TOKEN = credentials('sonar-toke-fastapi-proj') // If this is the correct token
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull code from GitHub
                git branch: 'main', url: "${GIT_REPO_URL}"
            }
        }
        
        stage('Run SonarQube Analysis') {
            steps {
                script {
                    // Ensure SonarQube Scanner is installed and available in PATH
                    // Comment out the `sh` command and use `bat` command for Windows
                    // sh """
                    // sonar-scanner \
                    // -Dsonar.projectBaseDir=${WORKSPACE} \
                    // -Dsonar.properties=${WORKSPACE}/sonar-project.properties \
                    // -Dsonar.login=${env.SONAR_PROJ_TOKEN}
                    // """
                    
                    bat """
                    "C:\\Program Files\\sonar-scanner-cli-6.0.0.4432-windows\\sonar-scanner-6.0.0.4432-windows\\bin\\sonar-scanner.bat" ^
                    -Dsonar.projectBaseDir=${WORKSPACE} ^
                    -Dsonar.properties=${WORKSPACE}\\sonar-project.properties ^
                    -Dsonar.login=${env.SONAR_PROJ_TOKEN}
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_TAG}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Log in to Docker Hub and push the Docker image
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_TAG}").push("${DOCKER_TAG}")
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
