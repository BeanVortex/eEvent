First install nodejs

then in project folder run

```bash
python -m pip install django-tailwind
```
and
```bash
python -m pip install django_browser_reload
```

then 

```bash
python manage.py tailwind install
```

and run tailwind to show styles

```bash
python manage.py tailwind start
```

finally run the app

```bash
python manage.py runserver
```

Database configuration should be done via settings.py