# Утилита для выгрузки статистики репозитория гитхаба
## Параметры
```console
usage: main.py [-h] [--branch BRANCH] [--from_datetime FROM_DATETIME] [--to_datetime TO_DATETIME] repo_url

Program to print github repository statistics

positional arguments:
  repo_url              Url of github repository to analyze

optional arguments:
  -h, --help            show this help message and exit
  --branch BRANCH       Branch to analyze (master by default)
  --from_datetime FROM_DATETIME
                        Start analyze from this date Format is YYYY-MM-DDTHH:MM:SSZ (None by default)
  --to_datetime TO_DATETIME
                        Analysis will stop at this date. Format is YYYY-MM-DDTHH:MM:SSZ (None by default)
```
## Пример
```bash
python main.py https://github.com/mvarnar/test --branch test_branch --to_datetime 2020-03-9T00:00:00Z
```
```console
Top 30 commiters
Author  Number of commits
max     3

------------------------------
Pull requests
State   Number of requests
open    0
closed  0

------------------------------
Old pull requests
Number of old requests
0

------------------------------
Issues
State   Number of issues
open    1
closed  1

------------------------------
Old issues
Number of old issues
0

------------------------------
```
## Потенциальный CI\CD
Обернуть сервис в докер-контейнер, внутри контейнера использовать крон таску, которая будет вызывать скрипт с необходимой регулярностью. В качестве сервиса для деплоя можно использовать сервис gitlab-ci или другой аналогичный сервис.