## Instructions to run, are at the end

eEvent is an online event attendance.

There are two users:
- Organizer who creates events and discounts for events
- Attender who attends in events with or without using discounts

These users have their own panel and signup section
Login is same for all



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

install maildev
```bash
npm -g install maildev
```
and run maildev
```bash
maildev
```

and you can see the mails on:
```http://{host}:1080```


and run tailwind to show styles

```bash
python manage.py tailwind start
```

finally run the app

```bash
python manage.py runserver
```

Database configuration should be done via settings.py
