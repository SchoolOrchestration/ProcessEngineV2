import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', 'postgres'),
        'USER': os.environ.get('DATABASE_USER', 'postgres'),
        'HOST': os.environ.get('DATABASE_HOST', 'db'),
        'PORT': 5432,
    }
}
db_password = os.environ.get('DATABASE_PASSWORD', False)
if db_password:
    DATABASES.get('default').update({'PASSWORD': db_password})
