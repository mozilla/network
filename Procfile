release: cd network-api && python ./manage.py migrate --no-input && python ./manage.py block_inventory
web: cd network-api && gunicorn networkapi.wsgi:application
