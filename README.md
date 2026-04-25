# Tech365 Ecommerce Django API

## Features
- Register
- Login with token authentication
- Edit profile
- Product categories
- Product listing and detail
- Search and category filter
- Cart
- Checkout
- Orders
- Offline payment only
- Django admin for back office work

## Setup
```bash
python -m venv venv
source venv/bin/activate  # Linux or Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints
### Accounts
- POST `/api/accounts/register/`
- POST `/api/accounts/login/`
- GET `/api/accounts/profile/`
- PUT `/api/accounts/profile/`

### Store
- GET `/api/store/categories/`
- GET `/api/store/products/`
- GET `/api/store/products/?search=shoe`
- GET `/api/store/products/?category=1`
- GET `/api/store/products/<id>/`
- GET `/api/store/cart/`
- POST `/api/store/cart/`
- PUT `/api/store/cart/items/<item_id>/`
- DELETE `/api/store/cart/items/<item_id>/`

### Orders
- POST `/api/orders/checkout/`
- GET `/api/orders/`
- GET `/api/orders/<order_id>/`

## Notes
- Checkout uses offline payment only.
- Orders are created with `payment_status = pending`.
- Use Django admin to review and manage products and orders.
