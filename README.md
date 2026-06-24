
# Inventory Management

A full-stack inventory management system built for a small retail business. Manages product categories, stock items with quantities, multi-user access and a complete audit trail of all activity.

## Tech Stack

- Backend:  FastAPI, PostgreSQL, Redis, SQLAlchemy, Alembic, Docker

- Frontend: React, Vite, Tailwind CSS


## Features

### Inventory
- Contains Hierarchical structure with categories and sub-categories.
- Per product quantity tracking with a dedicated PATCH endpoint.
- Cascade delete with complete deletion of a category.
- Paginated item listing with configurable skip/limit.

### Auth & Security
- JWT authentication with separate access and refresh tokens.
- Argon2 password hashing.
- Account lockout after repeated failed login attempts.
- Role-based access control: users - admin
- Rate limiting on sensitive endpoints via Redis.

### Audit logging 
- Automatic request logging via Starlette middleware — every action is recorded without touching route handlers
- Logs capture: user ID, IP address, endpoint, HTTP method, status code, timestamp
- Self-exclusion: /logs endpoints don't generate new log entries
- Security log view for admins (failed logins, rate limit hits, unauthorized access attempts)

### Architecture
- Layered: routes → services → repositories — business logic is separated from DB queries
- BaseModelMixin for DRY serialization across all ORM models.
- Alembic migrations for schema versioning
- Separate test environment with its own DB and conftest.py


## Screenshots
![Login](docs/screenshots/Login_page.png)
![Register](docs/screenshots/Register_page.png)
![Inventory](docs/screenshots/Inventory-mainpage.png)

 
## Project Structure

app/
- back/
    - routes/          
    - services/  
    - repositories/
    - alembic/         
    - tests/           
    - main.py
    - auth.py          
    - logs_middleware.py
    - db_models.py
    - model.py         
- front/               


## API Endpoints
### Auth

| Method | Endpoint | Auth | Description                |
| :-------- | :------- | :------- | :------------------------- |
| POST | /register |  | Create account |
|POST| /login| | Returns access & refresh tokens|
| POST| /refresh| Refresh token| Get new access token|

#### Items/Categories


| Method |Endpoints   | Auth| Description                       |
| :-------- | :------- | :--------|:-------------------------------- |
| GET  | /items | User | Paginated list of user's categories |
| GET | /items/{id} | User | Single category with its sub-items|
| POST | /items| User | Create category |
| PUT | /items/{id} | User | Rename category |
| DELETE | /items/{id} | User | Delete category (cascades to sub-items) |

#### Sub-Items


| Method |Endpoints   | Auth| Description                       |
| :-------- | :------- | :--------|:-------------------------------- |
| GET  | /items/{id}/sub-items | User | List products in a category |
| POST | /items/{id}/sub-items | User | Add product|
| PUT | /items/{id}/sub-items/{sid}| User | Update product name |
| PATCH | /items/{id}/sub-items/{sid}/quantity | User | Update stock quantity |
| DELETE | /items/{id}/sub-items/{sid} | User | Remove product |

### Logs

| Method |Endpoints   | Auth| Description                       |
| :-------- | :------- | :--------|:-------------------------------- |
| GET  | /logs/me | User | Current user's activity |
| GET | /logs/all | Admin | All user activity|
| GET | /logs/security| Admin | Failed logins, rate limits, 403s |

## Run Locally

Clone the project

```bash
    git clone https://github.com/panven-ops/Inventory-.git
    
    cd Inventory-

    pip install -r requirements.txt
   
    docker compose up
```

API will be available at http://localhost:8000 for backend and http://localhost:5173 for frontend
## Environment Variables

Copy the example file and fill in the values:

```bash
cp back/.env.example back/.env
```

| Variable | Description |
| :------- | :---------- |
| SECRET_KEY | Secret key for JWT signing |
| DATABASE_URL | PostgreSQL connection string |
| REDIS_HOST | Redis hostname (default: redis) |
| REDIS_PORT | Redis port (default: 6379) |
| ENABLE_RATE_LIMIT | Enable rate limiting (true/false) |

## Running Tests

To run tests, run the following command

```bash
    docker compose up -d
    docker exec <container_id> pytest tests/ -v
```

## Creating an Admin User

First register a normal account via `POST/register` and then run:

```bash
cd app/back
python create_admin.py <username>
```

The created admin user will have access to `/logs` admin endpoints and to future admin-only endpoints

## Roadmap

- Notification to admin about items that are out of stock.
- Auto-generate restock order email: scheduled job detects low/out-of-stock 
items and drafts an email; admin reviews, selects items to reorder, 
and sends with one click (SendGrid / SMTP).
