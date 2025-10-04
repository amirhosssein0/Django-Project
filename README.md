# 🛍️ Django E-Commerce Project

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2%2B-green)](https://djangoproject.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A full-featured e-commerce platform built with Django.

## ✨ Features
- User Authentication: Registration, login, and profile management
- Product Catalog: Categories, filters, and search functionality
- Shopping Cart: Session-based cart system
- Order Management: Purchase history and order tracking
- Admin Dashboard: Complete backend administration

## 🚀 Quick Start

### Prerequisites
- Python 3.12
- Django 5.2
- PostgreSQL (recommended) or SQLite3

### Installation
`bash
# Clone repository
git clone https://github.com/amirhosssein0/Django-Project.git
cd Django-Project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
