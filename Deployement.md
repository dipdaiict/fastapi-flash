

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

#### Copy a Directory

To copy directories, use the `-r` (recursive) flag to copy all the contents of the directory:

```bash
cp -r /path/to/source/directory /path/to/destination
```

### Load Environment Variables on Login/System Reboot

To ensure that your environment variables are loaded every time you log in, add the following line to your `.profile` file:

Beofre setting please add also the required environment variable in .env file in your app directory. 
Ensure your .env file contains the following environment variables without any spaces around the = sign: Example like: database_hostname=your_database_hostname

1. Open the `.profile` file in your home directory:

    ```bash
    nano ~/.profile
    ```

2. Add the following line to the file:

    ```bash
    set -o allexport; source /home/<username>/app/.env; set +o allexport
    ```

    Replace `<username>` with your actual username.

3. Save and exit the editor (Ctrl+O to write out, then Ctrl+X to exit in nano).

4. Apply the changes:

    ```bash
    source ~/.profile
    ```
### Set The Service up when you boot the system:

To create a systemd service file, you need root permissions. You can use `sudo` to create and edit the service file. Here’s how to do it:

1. **Create the service file with sudo**:

    ```bash
    sudo touch /etc/systemd/system/fastapi-flash.service
    ```

2. **Edit the service file with sudo**:

    ```bash
    sudo nano /etc/systemd/system/fastapi-flash.service
    ```

3. **Add the following content to the service file**:

    ```ini
    [Unit]
    Description=FastAPI Flash Service
    After=network.target
    
    [Service]
    User=dippatel
    Group=www-data
    WorkingDirectory=/home/dippatel/app/src/fastapi-flash
    EnvironmentFile=/home/dippatel/app/.env
    ExecStart=/home/dippatel/app/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8080
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    ```

4. **Save and close the editor** (Ctrl+O to write out, then Ctrl+X to exit in nano).

5. **Reload systemd to recognize the new service**:

    ```bash
    sudo systemctl daemon-reload
    ```

6. **Start the service**:

    ```bash
    sudo systemctl start fastapi-flash.service
    ```

7. **Enable the service to start on boot**:

    ```bash
    sudo systemctl enable fastapi-flash.service
    ```

8. **Check the status of the service**:

    ```bash
    sudo systemctl status fastapi-flash.service
    ```

9. **If you encounter any issues, you can check the logs for the service using**:

    ```bash
    journalctl -u fastapi-flash.service -f -n 50
    ```
#### Install and Configure NGINX

1. **Install NGINX:**

   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Configure NGINX:**

   - Create or edit your NGINX site configuration file in `/etc/nginx/sites-available/`:

     ```bash
     sudo nano /etc/nginx/sites-available/your_site
     ```

     Add the following configuration:

     ```nginx
     server {
         listen 80 default_server;
         listen [::]:80 default_server;
         server_name _; # Replace with your specific domain name like sanjeev.com

         location / {
             proxy_pass http://localhost:8000;
             proxy_http_version 1.1;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header Upgrade $http_upgrade;
             proxy_set_header Connection 'upgrade';
             proxy_set_header Host $http_host;
             proxy_set_header X-NginX-Proxy true;
             proxy_redirect off;
         }

         error_page 404 /404.html;
         location = /404.html {
             root /usr/share/nginx/html;
             internal;
         }
     }
     ```

3. **Create a Symbolic Link:**

   ```bash
   sudo ln -s /etc/nginx/sites-available/your_site /etc/nginx/sites-enabled/
   ```

4. **Test NGINX Configuration:**

   ```bash
   sudo nginx -t
   ```

5. **Restart NGINX:**

   ```bash
   sudo systemctl restart nginx
   ```
#### 2. Firewall Configuration

1. **Check UFW Status:**

   ```bash
   sudo ufw status
   ```

2. **Allow Necessary Ports:**

   ```bash
   sudo ufw allow http
   sudo ufw allow https
   sudo ufw allow ssh
   sudo ufw allow 5432
   ```

3. **Enable UFW:**

   ```bash
   sudo ufw enable
   ```

4. **Verify UFW Status:**

   ```bash
   sudo ufw status
   ```

   Ensure the output includes:

   ```plaintext
   Status: active

   To                         Action      From
   --                         ------      ----
   Nginx Full                 ALLOW       Anywhere
   80/tcp                     ALLOW       Anywhere
   443                        ALLOW       Anywhere
   22/tcp                     ALLOW       Anywhere
   5432                       ALLOW       Anywhere
   Nginx Full (v6)            ALLOW       Anywhere (v6)
   80/tcp (v6)                ALLOW       Anywhere (v6)
   443 (v6)                   ALLOW       Anywhere (v6)
   22/tcp (v6)                ALLOW       Anywhere (v6)
   5432 (v6)                  ALLOW       Anywhere (v6)
   ```

5. **Delete a UFW Rule:**

   - **Find the Rule Number:**

     ```bash
     sudo ufw status numbered
     ```

     This will list all rules with their respective numbers.

   - **Delete the Rule:**

     ```bash
     sudo ufw delete <rule_number>
     ```

     Replace `<rule_number>` with the number of the rule you want to delete. For example, to delete rule number 3:

     ```bash
     sudo ufw delete 3
     ```
---
