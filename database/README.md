# MySQL Environment Initialization

This document describes how to initialize the MySQL environment for local development.

## Docker Compose

The `docker-compose.yaml` file is used to manage the MySQL container.

### Environment Variables

The following environment variables are required to run the MySQL container. You can set them in a `.env` file in the `mysql` directory.

-   `MYSQL_ROOT_PASSWORD`: The root password for the MySQL database.
-   `MYSQL_DATABASE`: The name of the database to create. This database will be created and granted all privileges to `MYSQL_USER`.
-   `MYSQL_USER`: The name of the user to create.
-   `MYSQL_PASSWORD`: The password for the user.
-   `MYSQL_DATA_DIR`: (Optional) The host path for the data volume. If not set, it defaults to `${HOME}/data/mysql`.

### Usage

1.  Create a `.env` file in the `database/mysql` directory with the required environment variables.
2.  Place your SQL initialization scripts (e.g., `init.sql`, `schema.sql`, `data.sql`) in the container's `/docker-entrypoint-initdb.d/` directory. These scripts will be executed when the MySQL container starts for the first time.
3.  Run `docker-compose up -d` from the `database/mysql` directory to start the MySQL container.
