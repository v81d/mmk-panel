# MMK Panel

MMK Panel is the official Django backend for the MMK game.

This server is hosted officially on Oracle Cloud Infrastructure with S3 bucket storage. To replicate this setup, follow the instructions below.

## PostgreSQL 15 Setup (Oracle Linux 9, aarch64)

To install and set up PostgreSQL 15 on an ARM64 Oracle Linux 9 server, follow the steps:

1. Install and enable PostgreSQL 15:

```bash
# Install the repository RPM:
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-aarch64/pgdg-redhat-repo-latest.noarch.rpm

# Install PostgreSQL:
sudo dnf install -y postgresql15-server

# Optionally initialize the database and enable automatic start:
sudo /usr/pgsql-15/bin/postgresql-15-setup initdb
sudo systemctl enable postgresql-15
sudo systemctl start postgresql-15
```

2. Set up the database and user:

```bash
# Login to PostgreSQL user
sudo -i -u postgres
psql
```

In the shell, run:

```bash
CREATE DATABASE mmkpaneldb;
CREATE USER superuser WITH PASSWORD 'mypassword';  # set a secure password!!!
ALTER ROLE superuser SET client_encoding TO 'utf8';
ALTER ROLE superuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE superuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mmkpaneldb TO superuser;
\c mmkpaneldb
GRANT ALL ON SCHEMA public TO superuser;
```

3. Update listen addresses:

```bash
sudo nano /var/lib/pgsql/15/data/postgresql.conf ```

In the main configuration file, append this line:

```conf
listen_addresses = '*'
```

4. Allow remote users:

```bash
sudo nano /var/lib/pgsql/15/data/pg_hba.conf
```

In that configuration file, append this line:

```conf
host    all     all     0.0.0.0/0     md5
```

5. Update `.env` accordingly with your values:

```
PSQL_NAME=
PSQL_USER=
PSQL_PASSWORD=
PSQL_HOST=
PSQL_PORT=
```

## S3 Bucket Storage

To implement S3 bucket storage, simply specify the following data in `.env`:

```
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_BUCKET_NAME=
S3_ENDPOINT_URL=
S3_REGION_NAME=
S3_SIGNATURE_VERSION=
S3_ADDRESSING_STYLE=
```

For most setups, `S3_SIGNATURE_VERSION` would be `s3v4`.
