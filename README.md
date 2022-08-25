# olime_rest_api

# runserver
# python manage.py runserver

# clear database
# docker volume ls
# olime_rest_api_dev-db-data
# docker volume rm olime_rest_api_dev-db-data


# test
# docker-compose run --rm app sh -c "python manage.py test"

# python3 -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
# python3 -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
# erase pycache

# python3 manage.py migrate --fake myApp zero
# insomnia

# requirements 다운
# pip install -r /path/to/requirements.txt

# 가상환경 만들기
# python3 -m venv myvenv
# source myvenv/bin/activate
