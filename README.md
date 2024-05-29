# WagerBrain
WagerBrain is a toolbox for online money-making across niches like sports betting, crypto, and affiliate marketing. By offering essential math and tools, WagerBrain empowers users to become efficient and reach professional levels of success in their chosen online income path


## Table of Content
* [Environment](#environment)
* [Installation](#installation)
* [Usage](#usage)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

## Environment
This project is interpreted/tested on Windows using the GitBash cmd using Python (version 3.11.3)


## Installation
* Clone this repository: `git clone https://github.com/PeterEkwere/WagerBrain.git`
* Access WagerBrain directory: `cd WagerBrain`
* install dependencies: pip -r install requirements.txt
* create db: cat Wagerbrain_mysql_setup.sql | mysql -u root



## Usage
```
$ WagerBrain_MYSQL_USER=peter WagerBrain_MYSQL_PWD=Peter1234 WagerBrain_MYSQL_HOST=localhost WagerBrain_MYSQL_DB=WagerBrain_db WagerBrain_API_HOST=0.0.0.0 WagerBrain_API_PORT=5000 WagerBrain_SecretKey=b784f8a70df956ba188bfeed2e49f09a423a9e7d70d9d19e31cebf8ee0e8c29e python -m api.v1.app
```

## Go To https://127.0.0.1:5000/api/v1/Home to view the webapp

## Bugs
No known bugs at this time. 

## Authors
Ekwere Peter - [Github](https://github.com/PeterEkwere)

## License
