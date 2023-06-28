from invoke import task

@task
def makemigarations(ctx):
    ctx.run("python manage.py makemigrations")

@task
def migrate(ctx):
    ctx.run("python manage.py migrate")

@task
def runserver(ctx):
    ctx.run("python manage.py runserver")

@task
def test(ctx):
    ctx.run("python manage.py test")

@task
def migrateandtest(ctx):
    migrate(ctx)
    test(ctx)

@task
def makemigrationsandmigrate(ctx):
    makemigarations(ctx)
    migrate(ctx)
