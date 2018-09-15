# wine_gallery_test

This project runs entirely on Docker containers. Make sure to [have it][docker-download] in your environment.

## Using this template

Run the following to create a Django project with this repo as template:

```bash
$ pip install django
$ mkdir <your_project_name>
$ django-admin startproject \
  --template=https://github.com/jourdanrodrigues/django-template/archive/master.zip \
  --extension=po,yml,md,py \
  ${_} ./${_}
$ # If the above fails, you might have different versions of Python.
$ # Using "python -m django" instead of "django-admin" might fix.
$ # "python" could also be "python2" or "python3".
```

You may remove this section from the `README.md` generated for your project.  

## Setting up development environment

Before doing anything, run the following:

```bash
./scripts/setup_dev_env.sh
```

## Running the app

To make your life slightly easier, the script [`compose.sh`](compose.sh) is there for you to run commands in your
container. It's just a wrapper for `docker-compose`, so you might want to take a look at
[its documentation][docker-compose-docs].

### Production mode

```bash
./compose.sh up
```

### Development mode

```bash
./compose.sh dev up
```

[docker-download]: https://www.docker.com/community-edition#/download
[docker-compose-docs]: https://docs.docker.com/compose/reference/
