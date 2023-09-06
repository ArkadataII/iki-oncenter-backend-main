## ******** ONCENTER PROJECTS ********

### Cấu trúc project
``` commandline
.  
├── alembic  
│   ├── versions    // thư mục chứa file migrations  
│   └── env.py  
├── app  
│   ├── api         // các file api được đặt trong này  
│   ├── core        // chứa file config load các biến env & function tạo/verify JWT access-token  
│   ├── db          // file cấu hình make DB session  
│   ├── helpers     // các function hỗ trợ như login_manager, paging  
│   ├── models      // Database model, tích hợp với alembic để auto generate migration  
│   ├── schemas     // Pydantic Schema  
│   ├── services    // Chứa logic CRUD giao tiếp với DB  
│   └── main.py     // cấu hình chính của toàn bộ project  
├── tests  
│   ├── api         // chứa các file test cho từng api  
│   ├── faker       // chứa file cấu hình faker để tái sử dụng  
│   ├── .env        // config DB test  
│   └── conftest.py // cấu hình chung của pytest  
├── .gitignore  
├── alembic.ini  
├── docker-compose.yaml  
├── Dockerfile  
├── env.example  
├── logging.ini     // cấu hình logging  
├── postgresql.conf // file cấu hình postgresql, sử dụng khi run docker-compose  
├── pytest.ini      // file setup cho pytest  
├── README.md  
└── requirements.txt
```

### Environment and Requirements Installation  (You can choose 1 of the 2 ways below)
#### Install common
``` bash
* sudo apt-get update
* sudo apt install -y build-essential libssl-dev libffi-dev
* sudo apt-get install g++ gcc
* sudo apt-get install libpq-dev
* sudo apt install apt-transport-https ca-certificates curl software-properties-common
* sudo apt-get install wget ca-certificates

```

#### C1: install canda
``` bash
> cd /tmp
> curl -O https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh (YES HẾT)
> source ~/.bashrc
> sudo rm -rf Anaconda3-2021.05-Linux-x86_64.sh
> conda update --all
> conda update -n base conda
> conda env list
> conda create -n <name_environment> python=3.8
> conda activate <name_environment>
> sudo pip install --upgrade -r requirements.txt 

```


#### C2: install pipenv
``` bash
> python3 -m pip install --user virtualenv
> python3 -m venv envs
> source envs/bin/activate
> sudo pip install --upgrade -r requirements.txt 

Hoặc

#### 👇️ if you get permissions error  #####

* sudo pip3 install virtualenv
* pip install virtualenv --user
* virtualenv envs
* source envs/bin/activate
* sudo pip install --upgrade -r requirements.txt 

```


### Databases
#### B1: Install postgresql database on ubuntu 20.04
``` bash
* sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
* sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
* sudo apt-get update
* sudo apt-get -y install postgresql-14
```

#### B2: create databases
``` bash
* sudo -u postgres psql
* CREATE DATABASE spincontents;
* CREATE USER user_spincontents WITH PASSWORD '123456';
* GRANT ALL PRIVILEGES ON DATABASE spincontents TO user_spincontents;
```

#### B3: Connect databases
``` bash
* change your username , password, database_name in path to file ./env.example
* cp env.example .env
* echo APP_ENV=dev >> .env
* echo SECRET_KEY=$(openssl rand -hex 32) >> .env
```

#### B4: init tables
``` bash
* alembic revision --autogenerate
* alembic upgrade head
```

### Run APP
``` bash
* uvicorn app.main:app --host 0.0.0.0 --port 5000
* uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload (not run on production)

```


### Dump Database
``` bash
* pg_dump -h 14.225.204.139 -p 2005 -U user_spincontents spincontents > spincontents-20221121-1502.sql
* docker exec -it docker_db_1 pg_dump -U user_spincontents spincontents > /home/thotx/thonx/db_backup/spincontents-20221121-1502.sql  ``` nếu chạy docker ```

```

``` commandline
packages = [
    {
      "id": 1,
      "name": "FREE_PACKAGE",
      "original_price": 0,
      "discount_price": 0,
      "description": "Gói Miễn Phí"
    },
    {
      "id": 2,
      "name": "DAY_PACKAGE",
      "original_price": 10000,
      "discount_price": 10000,
      "description": "Gói Ngày"
    },
    {
      "id": 3,
      "name": "MONTH_PACKAGE",
      "original_price": 150000,
      "discount_price": 150000,
      "description": "Gói Tháng"
    },
    {
      "id": 4,
      "name": "VIP_PACKAGE",
      "original_price": 750000,
      "discount_price": 750000,
      "description": "Gói 6 Tháng"
    },
    {
      "id": 5,
      "name": "PREMIUM_PACKAGE",
      "original_price": 1100000,
      "discount_price": 1100000,
      "description": "Gói 12 Tháng"
    },
    {
      "name": "ADVANCE_BASIC_PACKAGE",
      "original_price": 750000,
      "discount_price": 750000,
      "description": "Gói Nâng Cao Cơ Bản"
    },
    {
      "name": "ADVANCE_PRO_PACKAGE",
      "original_price": 750000,
      "discount_price": 750000,
      "description": "Gói Nâng Cao Pro"
    }
  ],


packages_detail = [
    {
      "id": 1,
      "package_id": 1,
      "no_ads": false,
      "is_support": false,
      "max_number_spin_turns": 5,
      "max_number_spin_words": 200,
      "high_level_spin": [
        3,
        4,
        5
      ],
      "high_level_spin_value": 2,
      "high_level_spin_value_free": 2,
      "check_level_spin": true,
      "max_number_plagiarism_turns": 1,
      "max_number_plagiarism_words": 200,
      "high_level_plagiarism": [
        2,
        3
      ],
      "high_level_plagiarism_value": 3,
      "check_level_plagiarism": false,
      "max_number_grammar_turns": 20,
      "max_number_grammar_words": 200,
      "high_level_grammar": [
        2,
        3
      ],
      "high_level_grammar_value": 0,
      "check_level_grammar": true
    },
    {
      "id": 2,
      "package_id": 2,
      "no_ads": true,
      "is_support": false,
      "max_number_spin_turns": 10,
      "max_number_spin_words": 1000,
      "high_level_spin": [
        3,
        4,
        5
      ],
      "high_level_spin_value": 10,
      "high_level_spin_value_free": 10,
      "check_level_spin": false,
      "max_number_plagiarism_turns": 2,
      "max_number_plagiarism_words": 1000,
      "high_level_plagiarism": [
        2,
        3
      ],
      "high_level_plagiarism_value": 50,
      "check_level_plagiarism": false,
      "max_number_grammar_turns": 200,
      "max_number_grammar_words": 1000,
      "high_level_grammar": [
        2,
        3
      ],
      "high_level_grammar_value": 0,
      "check_level_grammar": false
    },
    {
      "id": 3,
      "package_id": 3,
      "no_ads": true,
      "is_support": true,
      "max_number_spin_turns": 10,
      "max_number_spin_words": 1000,
      "high_level_spin": [
        3,
        4,
        5
      ],
      "high_level_spin_value": 10,
      "high_level_spin_value_free": 10,
      "check_level_spin": false,
      "max_number_plagiarism_turns": 50,
      "max_number_plagiarism_words": 1000,
      "high_level_plagiarism": [
        2,
        3
      ],
      "high_level_plagiarism_value": 50,
      "check_level_plagiarism": false,
      "max_number_grammar_turns": 200,
      "max_number_grammar_words": 1000,
      "high_level_grammar": [
        2,
        3
      ],
      "high_level_grammar_value": 0,
      "check_level_grammar": false
    },
    {
      "id": 4,
      "package_id": 4,
      "no_ads": true,
      "is_support": true,
      "max_number_spin_turns": 400,
      "max_number_spin_words": 2000,
      "high_level_spin": [
        3,
        4,
        5
      ],
      "high_level_spin_value": 400,
      "high_level_spin_value_free": 0,
      "check_level_spin": false,
      "force_spin": true,
      "force_spin_value": 400,
      "force_spin_value_free": 0,
      "max_number_plagiarism_turns": 20,
      "max_number_plagiarism_words": 2000,
      "high_level_plagiarism": [
        2,
        3
      ],
      "high_level_plagiarism_value": 20,
      "check_level_plagiarism": false,
      "max_number_grammar_turns": 400,
      "max_number_grammar_words": 2000,
      "high_level_grammar": [
        2,
        3
      ],
      "high_level_grammar_value": 400,
      "check_level_grammar": false,
      "check_summary": false,
      "max_number_summary_turns": 20,
      "max_number_summary_words": 2000,
      "check_rewrite": false,
      "max_number_rewrite_turns": 20,
      "max_number_rewrite_words": 2000
    },
    
    {
      "package_id": 7,
      "no_ads": true,
      "is_support": true,
      "max_number_spin_turns": 10,
      "max_number_spin_words": 200,
      "high_level_spin": [
        3,
        4,
        5
      ],
      "high_level_spin_value": 0,
      "high_level_spin_value_free": 3,
      "check_level_spin": true,
      "force_spin": false,
      "force_spin_value": 0,
      "force_spin_value_free": 0,
      "max_number_plagiarism_turns": 3,
      "max_number_plagiarism_words": 200,
      "high_level_plagiarism": [
        2,
        3
      ],
      "high_level_plagiarism_value": 0,
      "check_level_plagiarism": true,
      "max_number_grammar_turns": 0,
      "max_number_grammar_words": 0,
      "high_level_grammar": [
        2,
        3
      ],
      "high_level_grammar_value": 0,
      "check_level_grammar": true,
      "check_summary": true,
      "max_number_summary_turns": 0,
      "max_number_summary_words": 0,
      "check_rewrite": true,
      "max_number_rewrite_turns": 0,
      "max_number_rewrite_words": 0
    },
    
  ]

```
