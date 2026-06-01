# End project for Full-stack Django with HTMX and Tailwind course

This is how the project should looks like at then of the [Full-stack Django with HTMX and Tailwind](https://testdriven.io/courses/django-htmx/) course.

To see it in browser, run:
```shell
uv run python manage.py migrate
uv run python manage.py runserver
```

Login page requires Google and Meta login to be set.
To avoid that, create superuser (`uv run python manage.py createsuperuser`) and login via [admin](http://localhost:8000/admin/). The app can than be navigated as admin.

To load the pre-prepared test data, run:
```shell
uv run python manage.py loaddata initial_parties.json initial_guests.json initial_gifts.json
```

