---

# How to Install and Deploy a Backend on Ubuntu Server

## Update and Upgrade Packages

First, update and upgrade all packages on your Ubuntu server:

```bash
sudo apt update && sudo apt upgrade
```

## Check Python and Pip Versions

Verify Python and Pip installations:

```bash
python3 --version
pip --version    # Install with: sudo apt install python3-pip if needed
```

## Install Virtual Environment System

Install Python virtual environment:

```bash
sudo apt install python3-virtualenv
```

## Install PostgreSQL

Install PostgreSQL and its dependencies:

```bash
sudo apt install postgresql postgresql-contrib
```

Check PostgreSQL service status:

```bash
sudo systemctl status postgresql
```

If not running, start PostgreSQL:

```bash
sudo systemctl start postgresql
```

## Connect to PostgreSQL

Verify PostgreSQL installation and access:

```bash
psql --version
psql --help
```

To manage PostgreSQL, log in as the postgres user:

```bash
sudo -i -u postgres
```

To set a password for the postgres user:

1. Access the PostgreSQL interactive terminal:

    ```bash
    psql
    ```

2. Set the password for the postgres user:

    ```sql
    \password postgres
    ```

3. Exit the `psql` terminal:

    ```sql
    \q
    ```

4. Exit the postgres user session:

    ```bash
    exit
    ```

## Configure PostgreSQL Authentication

Adjust PostgreSQL configuration to allow connections:

Edit `postgresql.conf` to listen on specific IP addresses or all (`*`):

```bash
sudo vi /etc/postgresql/<version>/main/postgresql.conf
```

Edit `pg_hba.conf` to change authentication method to `md5` or `scram-sha-256`:

```bash
sudo vi /etc/postgresql/<version>/main/pg_hba.conf
```

Restart PostgreSQL for changes to take effect:

```bash
sudo systemctl restart postgresql
```

## Create a New User

For security, create a non-root user and grant sudo permissions if needed:

```bash
sudo adduser <username>
sudo usermod -aG sudo <username>
```

## Set Up Your Backend Environment

Navigate to your project directory and set up a virtual environment:

```bash
mkdir ~/app && cd ~/app
virtualenv venv
```

### Activate the Virtual Environment

To activate the virtual environment:

```bash
source venv/bin/activate
```

When the virtual environment is activated, your shell prompt will change to indicate that you're now working within the virtual environment.

### Deactivate the Virtual Environment

To deactivate the virtual environment when done:

```bash
deactivate
```

Clone your repository or set up your application:

```bash
mkdir src && cd src
git clone <repository_url>
```

Install required Python packages (ensure `libpq-dev` is installed for PostgreSQL):

```bash
sudo apt install libpq-dev   # Required for PostgreSQL
pip install -r requirements.txt
```

## Configure Environment Variables

Export necessary environment variables:

```bash
export VARIABLE_NAME=value
```

Check environment variables:

```bash
printenv
```

To persist environment variables across sessions, add them to `.profile` or set them system-wide.

## Start Your Backend Server

Run your backend using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

To run with Gunicorn (recommended for production):

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8080
```

## Manage Services

Monitor and manage services with systemd:

```bash
sudo systemctl start <service_name>
sudo systemctl enable <service_name>
```

Check service status and logs:

```bash
sudo systemctl status <service_name>
journalctl -u <service_name> -f -n 50    # Replace <service_name> with your service
```

## Additional Operations

To kill a process running on a specific port (e.g., 8080):

```bash
sudo ss -tulpn | grep :8080
sudo kill <PID>
```

---
