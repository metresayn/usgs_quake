# usgs_earthquake
A python application which loads data from the [api](https://earthquake.usgs.gov/fdsnws/event/1/), into postgresql. The repo consists of a docker compose file which sets up the container. You need to have Docker installed to run this application. The application is packaged by using a package manager -> [poetry](https://github.com/python-poetry/poetry). If you have not used poetry before, please check out this [tutorial](https://python-poetry.org/docs/basic-usage/) for easy installation and use.


### Steps to run the application locally:

- Set up the docker container in the root folder
    ```sh
        docker compose up -d
    ```

- Setup entrypoint, this script initializes your database and creates the tables required
  ```sh
    poetry run python3 entrypoint.py
  ```
- Run Python application
  ```sh
    poetry run python3 -m app.py
  ```

## Some additional functionalities

- Log into postgres once you have your docker-container-id, and run your queries
  - To view your docker-container-id, please run 
    - ```sh
        - docker ps
         ```
  - From docker container, log into postgresql       
  ```sh
    docker exec -it <docker-container-id> psql -U postgres \usgs
  ```
  - Run queries
  ```sql
    select count(*) from events;
  ```
    
- Execute Python Testing Locally
    ```sh
        poetry run pytest -s
    ```

- Format Python Code
  ```sh
    poetry run black --check .
  ```