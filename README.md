# NB-IoT Dashboard

A dashboard that displays NB-IoT traces parsed by MobileInsight. The project consists of a frontend and backend which need to be started separately if running locally. The backend consumes a file called `board.json` in the `api` directory. `board.json` is created via the redirection of running `test_analyzer.py`; i.e., `python3 test_analyzer.py` **(updated file to come to this repo)**. Upon demand, the backend analyzes `board.json` and returns its findings to the frontend. The frontend then displays that info in a human-friendly manner.

# How to Run
## The Backend

```shell
cd api

flask run
```
You'll need to install a few things into a Python environment before `flask run` will work; e.g. `pip install flask`. By default, the backend should be accessible at `localhost:5000`.

## The Frontend

In the project's root, run

```shell
yarn # to install all dependencies

npm run start # to start the frontend project at `localhost:3000`.
```
