DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shop',
        'USER': 'saleor_shop',
        'PASSWORD': 'zaq1!QAZ',
        'HOST': 'localhost',
        'PORT': '',
    }
}
