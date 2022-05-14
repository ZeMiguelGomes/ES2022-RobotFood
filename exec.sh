#!/bin/sh
echo "yes" | python manage.py collectstatic
pip freeze > requirements.txt
zip -r sv.zip .

if [[ $1 == "-rs" ]]
then
    python manage.py runserver
fi