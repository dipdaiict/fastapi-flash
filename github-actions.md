# GitHub Actions: Build and Deploy Code

This document provides a detailed explanation of the GitHub Actions workflow defined in the `build-deploy.yml` file for the FastAPI-Flash project. The workflow includes building the application, running tests, creating and publishing a Docker image, and deploying to an AWS EC2 instance.

## Workflow Directory Structure

The GitHub Actions workflow files are located in the `.github/workflows` directory. Ensure that the directory structure looks like this:

```
.github/
└── workflows/
    └── build-deploy.yml
```

## Workflow Overview

The workflow is triggered on `push` and `pull_request` events. It consists of three jobs:

1. **Build**: Sets up the environment, installs dependencies, runs tests, and prints a message.
2. **Docker Build and Publish**: Builds and publishes a Docker image to Docker Hub.
3. **Deploy**: Deploys the Docker image to an AWS EC2 instance.

## Job: Build

### Environment Variables

The job uses several environment variables stored as GitHub secrets:

- `DATABASE_HOSTNAME`
- `DATABASE_PORT`
- `DATABASE_PASSWORD`
- `DATABASE_NAME`
- `DATABASE_USERNAME`
- `SECRET_KEY`
- `ALGORITHM`
- `EXPIRATION_TIME_OF_TOKEN`

### Services

A PostgreSQL service is set up for testing purposes:

- **Image**: `postgres`
- **Environment Variables**:
  - `POSTGRES_PASSWORD`
  - `POSTGRES_DB`
- **Ports**: `5432:5432`
- **Health Check**:
  - Command: `pg_isready`
  - Interval: 10 seconds
  - Timeout: 5 seconds
  - Retries: 5

### Steps

1. **Pulling Git Repository**:
   ```yaml
   uses: actions/checkout@v2
   ```

2. **Install Python 3.11**:
   ```yaml
   uses: actions/setup-python@v2
   with:
     python-version: "3.11"
   ```

3. **Update Pip**:
   ```yaml
   run: python -m pip install --upgrade pip
   ```

4. **Install Dependencies**:
   ```yaml
   run: pip install -r requirements.txt
   ```

5. **Run Tests with Pytest**:
   ```yaml
   run: |
     pip install pytest
     pytest --disable-warnings -v -s
   ```

6. **Print Message**:
   ```yaml
   run: echo "Workflow Running... Well done"
   ```

## Job: Docker Build and Publish

### Prerequisites

This job depends on the successful completion of the `build` job.

### Steps

1. **Set up Docker Buildx**:
   ```yaml
   uses: docker/setup-buildx-action@v3
   ```

2. **Login to Docker Hub**:
   ```yaml
   uses: docker/login-action@v3
   with:
     username: ${{ secrets.DOCKER_HUB_USERNAME }}
     password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
   ```

3. **Build and Push Docker Image**:
   ```yaml
   uses: docker/build-push-action@v6
   with:
     push: true
     tags: ${{ secrets.DOCKER_HUB_USERNAME }}/fastapi-flash:latest
     cache-from: type=registry,ref=${{ secrets.DOCKER_HUB_USERNAME }}/fastapi-flash:latest
     cache-to: type=inline
   ```

## Job: Deploy

### Prerequisites

This job depends on the successful completion of the `docker_build_and_publish` job. 

#### Steps for Generating Private Key Readable format: Converting PuTTY Private Key (PPK) to OpenSSH Format

1. **Download PuTTYgen**:
   - If you haven't already, download PuTTYgen from the PuTTY website. PuTTYgen is a utility that allows you to generate, convert, and manage SSH keys.

2. **Open PuTTYgen**:
   - Launch PuTTYgen on your local machine.

3. **Load your PPK file**:
   - Click on `Load` in PuTTYgen.
   - Navigate to where your PPK file is stored and select it.

4. **Convert and Save as OpenSSH Key**:
   - Once loaded, PuTTYgen will display the details of the key.
   - Click on `Conversions` in the menu.
   - Choose `Export OpenSSH Key`.
   - Save the converted key file (typically with a `.pem` extension).

5. **Store in then GitHub Secrets**:
   - In your GitHub repository, go to `Settings -> Secrets`.
   - Add a new secret with a meaningful name (e.g., PROD_PRIVATE_KEY) and paste the contents of your .pem file into the value field.

6. **Default Usernames by Operating System**:

    - For Amazon Linux 2 or Amazon Linux AMI: ec2-user
    - For CentOS: centos
    - For Ubuntu: ubuntu
    - For Debian: admin
    - For Fedora: fedora
    - For RHEL (Red Hat Enterprise Linux): ec2-user or root (depends on configuration)
    - For SUSE Linux: ec2-user or root (depends on configuration)

    - Store it Same as PROD_PRIVATE_KEY.

7. **Host**: 
    - Host is the IP Address of Your System. If Elastic IP Then No Problem you have to Store it one time. Otherwise Normal IP Then it modified when you Start the container. [Production]

### Steps

1. **Deploy to AWS EC2 Container**:
   ```yaml
   uses: appleboy/ssh-action@v1.0.3
   with:
     host: ${{ secrets.PROD_HOST }}
     username: ${{ secrets.PROD_USERNAME }}
     key: ${{ secrets.PROD_PRIVATE_KEY }}
     script: |
       whoami
       echo ${{ secrets.PROD_PASSWORD }} | sudo -S -u dippatel bash -c '
         cd /home/dippatel/app/src/fastapi-flash
         git pull
         echo ${{ secrets.PROD_PASSWORD }} | sudo -S systemctl restart fastapi-flash
       '
   ```

This step uses the `appleboy/ssh-action` to connect to the EC2 instance via SSH, pull the latest code from the repository, and restart the FastAPI-Flash service.

## Conclusion

This GitHub Actions workflow automates the build, test, Docker image creation, and deployment process for the FastAPI-Flash project. By defining these jobs and steps, we ensure a consistent and reliable CI/CD pipeline.