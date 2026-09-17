# Bookstore

Bookstore APP from Backend Python course from EBAC

## Prerequisites

```
Python 3.14+
Poetry
Docker && docker-compose
```

## Quickstart

1. Clone this project

   ```shell
   git clone git@github.com:santiagobruna/bookstore.git
   ```

2. Install dependencies:

   ```shell
   cd bookstore
   poetry install
   ```

3. Run local dev server:

   ```shell
   poetry run python manage.py migrate
   poetry run python manage.py runserver
   ```

4. Run docker dev server environment:

   ```shell
   docker-compose up -d --build
   docker-compose exec web python manage.py migrate
   ```

5. Run tests inside of docker:

   ```shell
   docker-compose exec web python manage.py test
   ```

## Continuous Delivery (Render)

The app is deployed on Render. On every push to `main`, GitHub Actions runs tests and triggers a Render deploy.

### Setup

1. On Render → your Web Service → **Settings** → **Deploy Hook** → copy the URL
2. On GitHub → repo **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: the deploy hook URL
3. Optional: disable **Auto-Deploy** on Render to avoid double deploys (Actions will trigger deploys)

### Manual deploy

In GitHub Actions, run the workflow **Deploy to Render** with **Run workflow**.
