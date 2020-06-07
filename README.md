## Requirements

- python 3.8
- RAM: 8 GB

## Quick Start Guide

### Clone git repo
```
git clone https://github.com/RakhimBek/normapi.git
```

### Copy environment variables file
```
$ cp .env.example .env
```

###  Add environment variable
```
$ source .env
$ export $(cut -d= -f1 .env)
```

### Update pip, setuptools
```
$ pip install -U pip setuptools
```

### Install requirements:
```
$ pip install -r requirements.txt
```

### Run server
```
$ python normapi/main.py
```

### API
Automatic interactive API documentation
```
/docs
```