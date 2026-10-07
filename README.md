# HealthScanX

## Diagnostic Healthcare Booking API

HealthScanX is a production-minded REST API for diagnostic healthcare workflows. It connects patients with diagnostic centres, manages test availability and pricing, supports appointment bookings and simulated payments, and gives patients and staff access to diagnostic reports.

The project demonstrates a complete backend workflow built with Django REST Framework, including JWT authentication, role-based access control, database constraints, caching, background tasks, webhook verification, API documentation, Docker support, and automated tests.

**Repository:** [github.com/Aayush6560/HealthScanX](https://github.com/Aayush6560/HealthScanX)

## Highlights

- JWT-based signup, login, token refresh, and user profile endpoints
- Diagnostic centre catalogue with searchable locations
- Test catalogue with category filtering:
  - Radiology
  - Pathology
  - Nuclear Medicine
- Centre-specific test offerings with independent pricing and availability
- Booking lifecycle with pending, confirmed, failed, and cancelled states
- Payment workflow with signed webhook processing and retryable background tasks
- Patient diagnostic reports with draft and final statuses
- Staff-only management for centres, tests, offerings, payments, and reports
- Query validation and database constraints for reliable data integrity
- Cached centre listings with cache invalidation after catalogue changes
- OpenAPI schema and Swagger UI
- Docker Compose setup with PostgreSQL, Redis, API, and Celery services
- Automated test suite covering authentication, bookings, payments, webhooks, concurrency, and platform behavior

## Technology Stack

| Area | Technology |
| --- | --- |
| Language | Python |
| Framework | Django 5.2 |
| API | Django REST Framework |
| Authentication | JSON Web Tokens with Simple JWT |
| API documentation | drf-spectacular / OpenAPI |
| Database | SQLite for local development, PostgreSQL for Docker/production |
| Cache and broker | Redis |
| Background jobs | Celery |
| Production server | Gunicorn |
| Testing | pytest, pytest-django |
| Deployment | Docker Compose |

## Architecture

The application is organized into focused Django apps:

```text
apps/
├── accounts/   # User model, signup, login, profile
├── bookings/   # Booking state machine and appointment workflow
├── centres/    # Centres, diagnostic tests, categories, and offerings
├── payments/   # Payment records, signatures, webhooks, and retries
├── reports/    # Patient diagnostic reports
└── core/       # Permissions, middleware, pagination, exceptions, throttling
config/         # Django settings, URLs, WSGI, and Celery configuration
tests/          # API and workflow tests
```

### Core domain model

```text
User
 ├── Booking ── CentreTest ── DiagnosticCentre
 │                  └────── DiagnosticTest
 ├── Payment
 └── Report ─────── DiagnosticTest
```

`CentreTest` is the offering relationship between a centre and a test. This keeps pricing and availability specific to each centre instead of incorrectly storing them on the global test catalogue.

## API Reference

The API is available under the root URL. When running locally, use `http://127.0.0.1:8000`.

### Authentication

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/signup/` | Create a patient account |
| `POST` | `/auth/login/` | Obtain access and refresh tokens |
| `POST` | `/auth/refresh/` | Refresh an access token |
| `GET` | `/auth/me/` | Get the authenticated user |

### Diagnostic catalogue

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/centres/` | List diagnostic centres |
| `GET` | `/centres/{id}/` | Retrieve a centre and available tests |
| `GET` | `/centres/?search=Bengaluru` | Search by centre name or location |
| `GET` | `/centres/?test={test_id}` | Find centres offering a test |
| `GET` | `/tests/` | List diagnostic tests |
| `GET` | `/tests/?category=RADIOLOGY` | Filter tests by category |
| `GET` | `/centres/{id}/tests/` | List tests offered by a centre |

Supported category values are `RADIOLOGY`, `PATHOLOGY`, and `NUCLEAR`.

Centre, test, and offering write operations are restricted to staff users.

### Bookings and payments

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/bookings/` | Create a booking |
| `GET` | `/bookings/` | List the authenticated user's bookings |
| `GET` | `/bookings/{id}/` | Retrieve a booking |
| `POST` | `/bookings/{id}/cancel/` | Cancel a booking |
| `GET` | `/payments/` | List payment records available to the caller |
| `POST` | `/payments/{id}/pay/` | Start a payment |
| `POST` | `/payments/webhook/` | Process a signed payment webhook |

Bookings enforce future appointment times, valid centre/test offerings, positive amounts, and protection against duplicate active bookings for the same patient and slot.

### Reports

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/reports/` | List the caller's reports |
| `POST` | `/reports/` | Create a report |
| `GET` | `/reports/{id}/` | Retrieve a report |
| `PATCH` | `/reports/{id}/` | Update a report |
| `DELETE` | `/reports/{id}/` | Delete a report |

Patients automatically become the owner of reports they create. Staff users can create reports for a specific patient by providing `patient_id`.

### Operations and documentation

| Endpoint | Description |
| --- | --- |
| `/health/` | Health check |
| `/schema/` | OpenAPI schema |
| `/docs/` | Swagger UI |

## Quick Start

### Option 1: Local development

Requirements:

- Python 3.12+
- Git

```powershell
git clone https://github.com/Aayush6560/HealthScanX.git
cd HealthScanX

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open the API documentation at [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/).

SQLite, local-memory caching, and eager Celery execution are used by default, so the API can run locally without PostgreSQL or Redis.

### Option 2: Docker Compose

Docker Compose starts PostgreSQL, Redis, the API, and the Celery worker:

```powershell
docker compose up --build
```

The API is available at [http://127.0.0.1:8000](http://127.0.0.1:8000), and Swagger UI is available at [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/).

Stop the stack with:

```powershell
docker compose down
```

## Example Requests

Create an account:

```http
POST /auth/signup/
Content-Type: application/json

{
  "email": "patient@example.com",
  "password": "Str0ng-pass-123",
  "full_name": "Aayush Kumar"
}
```

Filter for radiology tests:

```http
GET /tests/?category=RADIOLOGY
```

Create a patient report:

```http
POST /reports/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "test_id": 1,
  "findings": "No abnormality detected.",
  "report_date": "2026-10-07",
  "status": "FINAL"
}
```

## Configuration

Copy `.env.example` to `.env` for local configuration. Important settings include:

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Enables development behavior |
| `ALLOWED_HOSTS` | Allowed host names |
| `DATABASE_URL` | Optional PostgreSQL connection URL |
| `REDIS_URL` | Optional Redis URL for cache and Celery |
| `WEBHOOK_SECRET` | HMAC secret for payment webhooks |
| `PAYMENT_SUCCESS_RATE` | Simulated payment success probability |

Never use the example secrets in a public deployment. Store production secrets in the deployment platform's secret manager.

## Testing

Run the complete test suite:

```powershell
python -m pytest
```

Run the Django system checks:

```powershell
python manage.py check
```

The test suite covers:

- Authentication and permissions
- Centre and test catalogue behavior
- Category filtering
- Patient report isolation
- Booking validation and state transitions
- Payment processing and webhook signatures
- Cache behavior
- Concurrency and database constraints
- Background task behavior

## Engineering Practices Demonstrated

- Clear separation of domain apps and service-layer logic
- Explicit serializers and validation for API input
- Staff-only write permissions with patient-level data isolation
- Database-level constraints for uniqueness and positive monetary values
- Transaction-safe booking and payment workflows
- Signed webhook verification
- Structured logging and consistent JSON error responses
- Pagination, search, throttling, and cache invalidation
- API-first documentation through OpenAPI
- Automated regression tests for critical workflows

## Security Notes

This repository is intended as a portfolio and development project. Before production use:

- Replace all development secrets.
- Configure a restricted `ALLOWED_HOSTS` value.
- Run behind HTTPS.
- Use a managed PostgreSQL database and Redis instance.
- Configure secure cookie, proxy, and logging settings for the hosting platform.
- Store webhook secrets outside source control.
- Review staff account provisioning and audit requirements.

## License

No license has been selected yet. Add a license before distributing or accepting external contributions.
