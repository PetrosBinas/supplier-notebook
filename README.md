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
