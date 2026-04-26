# MMK Panel

MMK Panel is the official Django backend for the MMK game.

## PostgreSQL 15 Setup

To install and set up PostgreSQL 15 as the database for MMK Panel, follow the steps:

1. Install and enable PostgreSQL 15 following the [official instructions](https://www.postgresql.org/download).

2. Set up the database and user:

```bash
sudo -i -u postgres
psql
```

In the shell, run:

```bash
CREATE DATABASE mmkpanel_db;
CREATE USER mmkpanel_db_user WITH PASSWORD 'mypassword';

ALTER ROLE mmkpanel_db_user SET client_encoding TO 'utf8';
ALTER ROLE mmkpanel_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE mmkpanel_db_user SET timezone TO 'UTC';

ALTER DATABASE mmkpanel_db OWNER TO mmkpanel_db_user;
GRANT ALL PRIVILEGES ON DATABASE mmkpanel_db TO mmkpanel_db_user;

\c mmkpanel_db
ALTER SCHEMA public OWNER TO mmkpanel_db_user;
```

3. Update listen addresses:

```bash
sudo nano /var/lib/pgsql/15/data/postgresql.conf
```

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
