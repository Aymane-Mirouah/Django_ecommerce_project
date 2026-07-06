# Old Kech — E-Commerce Platform

## Abstract

Old Kech is a full-stack e-commerce web application developed using the Django web framework with a MySQL backend (managed via XAMPP) and styled with Tailwind CSS. The platform supports a complete online shopping workflow including product browsing, guest and authenticated cart management, stock validation, and payment processing through PayPal. A key architectural focus is the **guest checkout** flow, which allows users to complete purchases without requiring account registration. The front end is fully responsive and incorporates CSS-only interactive UI elements for a polished user experience.


##  The Team

| Avatar | Contributor |
| :---: | :--- |
| <img src="https://github.com/Aymane-Mirouah.png" width="50" height="50" style="border-radius:50%;"/> | **Aymane Mirouah**<br>[@Aymane-Mirouah](https://github.com/Aymane-Mirouah) |
| <img src="https://github.com/Abdennacer-Bousadra.png" width="50" height="50" style="border-radius:50%;"/> | **Abdennacer bousadra**<br>[@Abdennacer-Bousadra](https://github.com/Abdennacer-Bousadra) |
| <img src="https://github.com/salaheddinemondo.png" width="50" height="50" style="border-radius:50%;"/> | **salah eddine**<br>[@salaheddinemondo](https://github.com/salaheddinemondo) |
| | **Ayoub Bensaa** |


## Features

### Shopping & Cart
- **Guest Checkout** — Browse, add to cart, and purchase without signing in; cart persists via browser cookies
- **Authenticated Cart** — Logged-in users maintain a persistent cart linked to their account
- **Stock Enforcement** — Server-side and client-side validation prevents adding more items than available in stock
- **Real-Time Cart Badge** — Cart item count updates instantly via JavaScript without page reload

### Product Management
- **Product Catalog** — Grid layout with product images, prices, and categories
- **Search** — Full-text search across product names and descriptions
- **Category Filtering** — Filter products by category using URL query parameters
- **Pagination** — Products are paginated (9 per page) for performance and usability

### User System
- **Email-Based Login** — Authenticate using email and password instead of a username
- **Registration** — Account creation with form validation
- **Order History** — Authenticated users can view their completed orders

### Checkout & Payments
- **Guest Checkout Form** — Collects name, email, shipping address, and phone number
- **PayPal Integration** — Secure payment processing via the PayPal JavaScript SDK
- **Order Summary** — Displays itemized totals before payment confirmation

### UI / UX
- **Fully Responsive Design** — Adapts seamlessly to mobile, tablet, and desktop viewports using Tailwind CSS responsive utilities
- **CSS-Only Interactive Elements** — Hover effects, backdrop blur, smooth transitions, and slide-up/fade-in animations are implemented entirely through CSS for a lightweight, polished feel
- **Glassmorphism Aesthetic** — Frosted glass panels, translucent backgrounds, and subtle shadows create a modern, premium visual identity
- **Custom Scrollbar** — Styled webkit scrollbar consistent with the design language

### Admin Panel
- **Django Admin** — Full CRUD for products, categories, orders, customers, and shipping addresses
- **Jazzmin Theme** — Enhanced admin interface with modern styling

---

## Tech Stack

| Layer        | Technology                          |
|-------------|-------------------------------------|
| **Backend** | Django 6.0 (Python)                |
| **Database**| MySQL (via XAMPP / phpMyAdmin)     |
| **Frontend**| HTML5, Tailwind CSS (CDN), JavaScript |
| **Payments**| PayPal JavaScript SDK               |
| **Admin UI**| Django Admin + Jazzmin             |
| **Dev Server** | Django Development Server        |


---

## Project Structure

```
ecommerce/
├── ecommerce/              # Django project settings
│   └── settings.py
├── store/                  # Main app
│   ├── auth_backends.py    # Email authentication
│   ├── models.py           # Product, Order, Customer, etc.
│   ├── views.py            # All view logic
│   ├── utils.py            # Cart data & guest order helpers
│   └── templates/store/    # HTML templates
├── static/
│   ├── js/cart.js          # Cart JavaScript logic
│   └── images/             # Static images (bg, product uploads)
├── manage.py
└── README.md
```
