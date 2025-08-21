# supplier-notebook

An automation learning project. It sends automated orders to a business’s suppliers on selected days and times.  
Orders stay organized in a single notebook, while suppliers and products exist as saved items (instances) ready to be selected in the main notebook.

---

## Supplier Notebook (Django + Celery + Gmail)

This is a project I built while learning Django, Celery, and Docker.  
The idea is simple: as a business manager I want to organize suppliers and products, write down what I need, and let the app automatically send messages to each supplier instead of doing it manually.

Right now it works with **Gmail** only (Viber/WhatsApp might be added later if possible with OAuth).  
It also tracks **monthly** and **yearly** spending per product and per supplier.

---

## What it does

- Add **Suppliers** (contact info + schedule of days/times they receive orders)
- Add **Products** and assign each to a supplier
- Add **Notebook entries** (quantities of products to order)
- Celery groups entries by supplier and sends **one email per supplier** at the right time
- Track **monthly / yearly spending** per product and per supplier

---

## How to run it (with Docker)

This project is **Docker‑first** so it should run the same way for everyone.

### 1) Clone the repo

```bash
git clone https://github.com/TrosPe1/supplier-notebook.git
cd supplier-notebook
```

## 2) Create your .env

This project uses environment variables for secrets (so you don’t hard-code passwords or API keys).

There’s already a `.env.example` file in the repo. Make a copy:


Now open `.env` in a text editor and set these values:

- `DJANGO_SECRET_KEY` → any long random string  
- `DJANGO_DEBUG` → True (for development) or False (for production)  
- `GMAIL_FROM_ADDRESS` → your Gmail address  

The Gmail credentials/token paths in `.env.example` are already correct for Docker.

---

## 3) Get Gmail credentials

The app talks to Gmail using the Gmail API. For that, you need Google OAuth credentials.

1. Go to [Google Cloud Console](https://console.cloud.google.com/)  
2. Create a **Desktop OAuth client** for the Gmail API.  
3. Download the `credentials.json` file.  

Don’t put it inside your repo. Store it outside your project.


Leave `token.json` empty for now — it will be created in the next step.

---

## 4) Generate the Gmail token (first time only)

Run:

```bash
docker compose up -d redis
docker compose run --rm --service-ports quickstart
```


- It will show a Google login URL in your terminal.  
- Open it, allow Gmail access.  

When it succeeds, a `token.json` file appears in your secrets folder.  
From now on, the app can send Gmail automatically.

---

## 5) Run database migrations

Django needs to set up the database tables:

```bash
docker compose run --rm web python manage.py migrate
```


(Optional) create a Django admin user:

```bash
docker compose run --rm web python manage.py createsuperuser
```

---

## 6) Start the app

Now start everything:

```bash
docker compose up --build
```


Open your browser at:

http://localhost:8000

Have Fun Organizing Your Suppliers!!




