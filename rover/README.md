# Mars rover simulator

The goal of this project is to simulate some rovers receiving instructions to walk over a plateau on mars.

## Installation

### With docker
Simply build the image:
```bash
make docker-build
```
Then activate a shell into it
```bash
make docker-shell
```

### Without docker
This project requires [poetry](https://python-poetry.org) to be installed to manage deps.

After having poetry installed, run:
```bash
make install
```

Then, activate the virtual environment by running:
```bash
poetry shell
```


## Running
To run the simulation, run:
```bash
python app.py input.txt
```
(you might have to share volumes if you are using docker, or simply edit the placeholder [input.txt](./input.txt) file)

To check all the options
```bash
python app.py --help
```


## Testing
To test, run the follow command:
```bash
make test
```

To check test coverage, run:
```bash
make coverage
```
