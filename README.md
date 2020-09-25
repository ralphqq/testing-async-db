# testing-async-db
A simple demo that shows one approach at how to build and test apps that use async features with Postgres database storage.

## Requirements
- [Python](https://www.python.org/downloads/release/python-380/) >= 3.8
- [PostgreSQL](https://www.postgresql.org/), preferably using any of the [official Postgres Docker images](https://hub.docker.com/_/postgres)
- [Docker](https://www.docker.com/)
- [aiopg](https://aiopg.readthedocs.io/en/stable/) >= 1.0.0
- [SQLAlchemy](https://www.sqlalchemy.org/) == 1.3.17
- [pytest](https://pytest.org/) and [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)

Please see `requirements.txt` for full list of dependencies.

## Setup
1. Clone this repo
2. Create and activate a virtual environment
3. Install the dependencies:
    ```console
    $ pip install -r requirements.txt
    ```
4. Create a `.env` file in the project root and provide values to environment variables (see 'Environment Variables' section below)
5. Run Postgres docker image:
    ```console
    $ docker run --rm -p 5432:5432 --env-file .env --name db postgres
    ```
6. Run the test suite:
    ```console
    $ pytest
    ```

## Environment Variables
Please create a `.env` file that defines values for the following environment variables:

- `POSTGRES_USER` (name of Postgres user)
- `POSTGRES_PASSWORD` (Postgres password)
- `POSTGRES_DB` (database name)
- `DB_HOST` (host where Postgres is running, usually `localhost`)

## License
This project is available under the [MIT License](https://opensource.org/licenses/MIT).


