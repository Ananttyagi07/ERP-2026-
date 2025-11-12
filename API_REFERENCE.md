# API Reference Guide - University ERP

Complete API reference for all 658 endpoints across 43 modules.

---

## 🔐 Authentication

### Get JWT Token
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "your_password"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

### Use Token in Requests
```bash
GET /api/any-endpoint/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 📦 Phase 3 Modules (NEW)

### 1. Asset Management Module

Manage institutional assets, vendors, and inventory.

#### Endpoints:
```
GET    /api/asset-management/vendors/              # List all vendors
POST   /api/asset-management/vendors/              # Create vendor
GET    /api/asset-management/vendors/{id}/         # Get vendor details
PUT    /api/asset-management/vendors/{id}/         # Update vendor
DELETE /api/asset-management/vendors/{id}/         # Delete vendor (soft)

GET    /api/asset-management/stores/               # List all stores
POST   /api/asset-management/stores/               # Create store
GET    /api/asset-management/stores/{id}/          # Get store details
PUT    /api/asset-management/stores/{id}/          # Update store
DELETE /api/asset-management/stores/{id}/          # Delete store

GET    /api/asset-management/asset-categories/     # List categories
POST   /api/asset-management/asset-categories/     # Create category
GET    /api/asset-management/asset-categories/{id}/ # Get category
PUT    /api/asset-management/asset-categories/{id}/ # Update category
DELETE /api/asset-management/asset-categories/{id}/ # Delete category

GET    /api/asset-management/asset-items/          # List all assets
POST   /api/asset-management/asset-items/          # Create asset
GET    /api/asset-management/asset-items/{id}/     # Get asset details
PUT    /api/asset-management/asset-items/{id}/     # Update asset
DELETE /api/asset-management/asset-items/{id}/     # Delete asset

GET    /api/asset-management/asset-purchases/      # List purchases
POST   /api/asset-management/asset-purchases/      # Record purchase
GET    /api/asset-management/asset-purchases/{id}/ # Get purchase
PUT    /api/asset-management/asset-purchases/{id}/ # Update purchase
DELETE /api/asset-management/asset-purchases/{id}/ # Delete purchase

GET    /api/asset-management/asset-issues/         # List issued assets
POST   /api/asset-management/asset-issues/         # Issue asset
GET    /api/asset-management/asset-issues/{id}/    # Get issue details
PUT    /api/asset-management/asset-issues/{id}/    # Update issue
DELETE /api/asset-management/asset-issues/{id}/    # Delete issue
```

#### Example: Create Asset Item
```bash
POST /api/asset-management/asset-items/
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "college": 1,
  "category": 2,
  "name": "HP Laptop i5 8GB",
  "product_code": "HP-LAP-001",
  "item_type": "Non-Consumable",
  "store": 1,
  "unit": "Piece",
  "unit_price": 45000.00,
  "quantity": 10,
  "description": "HP Laptop for Computer Lab"
}
```

---

### 2. Library Module

Complete library management with books, members, and issue tracking.

#### Endpoints:
```
GET    /api/library/books/                         # List all books
POST   /api/library/books/                         # Add new book
GET    /api/library/books/{id}/                    # Get book details
PUT    /api/library/books/{id}/                    # Update book
DELETE /api/library/books/{id}/                    # Delete book

GET    /api/library/library-members/               # List members
POST   /api/library/library-members/               # Add member
GET    /api/library/library-members/{id}/          # Get member
PUT    /api/library/library-members/{id}/          # Update member
DELETE /api/library/library-members/{id}/          # Remove member

GET    /api/library/book-issues/                   # List all issues
POST   /api/library/book-issues/                   # Issue book
GET    /api/library/book-issues/{id}/              # Get issue details
PUT    /api/library/book-issues/{id}/              # Update issue (return)
DELETE /api/library/book-issues/{id}/              # Delete issue

GET    /api/library/ebooks/                        # List e-books
POST   /api/library/ebooks/                        # Upload e-book
GET    /api/library/ebooks/{id}/                   # Get e-book
PUT    /api/library/ebooks/{id}/                   # Update e-book
DELETE /api/library/ebooks/{id}/                   # Delete e-book
```

#### Example: Issue Book
```bash
POST /api/library/book-issues/
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "college": 1,
  "book": 5,
  "member": 3,
  "issue_date": "2025-11-09",
  "due_date": "2025-11-23",
  "note": "Handle with care"
}
```

#### Example: Return Book
```bash
PATCH /api/library/book-issues/{id}/
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "return_date": "2025-11-22",
  "note": "Returned in good condition"
}
```

---

### 3. Transport Module

School transport management with routes, stops, and members.

#### Endpoints:
```
GET    /api/transport/vehicles/                    # List vehicles
POST   /api/transport/vehicles/                    # Add vehicle
GET    /api/transport/vehicles/{id}/               # Get vehicle
PUT    /api/transport/vehicles/{id}/               # Update vehicle
DELETE /api/transport/vehicles/{id}/               # Delete vehicle

GET    /api/transport/routes/                      # List routes
POST   /api/transport/routes/                      # Create route
GET    /api/transport/routes/{id}/                 # Get route
PUT    /api/transport/routes/{id}/                 # Update route
DELETE /api/transport/routes/{id}/                 # Delete route

GET    /api/transport/route-stops/                 # List stops
POST   /api/transport/route-stops/                 # Add stop
GET    /api/transport/route-stops/{id}/            # Get stop
PUT    /api/transport/route-stops/{id}/            # Update stop
DELETE /api/transport/route-stops/{id}/            # Delete stop

GET    /api/transport/transport-members/           # List members
POST   /api/transport/transport-members/           # Add member
GET    /api/transport/transport-members/{id}/      # Get member
PUT    /api/transport/transport-members/{id}/      # Update member
DELETE /api/transport/transport-members/{id}/      # Remove member
```

---

### 4. Messaging Module

Internal messaging system (like email within ERP).

#### Endpoints:
```
GET    /api/messaging/messages/                    # List all messages
POST   /api/messaging/messages/                    # Send message
GET    /api/messaging/messages/{id}/               # Get message
PUT    /api/messaging/messages/{id}/               # Update message
DELETE /api/messaging/messages/{id}/               # Delete message (move to trash)
```

#### Query Parameters:
```
?folder=inbox       # Show inbox messages (where user is receiver)
?folder=sent        # Show sent messages (where user is sender)
?folder=draft       # Show draft messages
?folder=trash       # Show deleted messages
?is_read=false      # Show unread messages
```

#### Example: Send Message
```bash
POST /api/messaging/messages/
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "college": 1,
  "receiver": 5,
  "subject": "Meeting Tomorrow",
  "body": "We have a staff meeting tomorrow at 10 AM. Please be on time.",
  "is_draft": false
}
```

---

### 5. Communication Module

Bulk email and SMS sending.

#### Endpoints:
```
GET    /api/communication/email-logs/              # List email logs
POST   /api/communication/email-logs/              # Send bulk email
GET    /api/communication/email-logs/{id}/         # Get email log
PUT    /api/communication/email-logs/{id}/         # Update email
DELETE /api/communication/email-logs/{id}/         # Delete email

GET    /api/communication/sms-logs/                # List SMS logs
POST   /api/communication/sms-logs/                # Send bulk SMS
GET    /api/communication/sms-logs/{id}/           # Get SMS log
PUT    /api/communication/sms-logs/{id}/           # Update SMS
DELETE /api/communication/sms-logs/{id}/           # Delete SMS
```

#### Example: Send Bulk Email
```bash
POST /api/communication/email-logs/
Authorization: Bearer YOUR_TOKEN
Content-Type: multipart/form-data

{
  "college": 1,
  "receiver_type": "Student",
  "receiver_ids": [1, 2, 3, 4, 5],
  "subject": "Exam Schedule Released",
  "body": "Dear Students, the exam schedule has been released...",
  "attachment": <file>  # optional
}
```

---

### 6. Complain Module

Complaint management system.

#### Endpoints:
```
GET    /api/complain/complain-types/               # List complaint types
POST   /api/complain/complain-types/               # Create type
GET    /api/complain/complain-types/{id}/          # Get type
PUT    /api/complain/complain-types/{id}/          # Update type
DELETE /api/complain/complain-types/{id}/          # Delete type

GET    /api/complain/complains/                    # List complaints
POST   /api/complain/complains/                    # File complaint
GET    /api/complain/complains/{id}/               # Get complaint
PUT    /api/complain/complains/{id}/               # Update/resolve complaint
DELETE /api/complain/complains/{id}/               # Delete complaint
```

---

### 7. Announcement Module

Notice board, news, and holiday management.

#### Endpoints:
```
GET    /api/announcement/notices/                  # List notices
POST   /api/announcement/notices/                  # Create notice
GET    /api/announcement/notices/{id}/             # Get notice
PUT    /api/announcement/notices/{id}/             # Update notice
DELETE /api/announcement/notices/{id}/             # Delete notice

GET    /api/announcement/news/                     # List news
POST   /api/announcement/news/                     # Create news
GET    /api/announcement/news/{id}/                # Get news
PUT    /api/announcement/news/{id}/                # Update news
DELETE /api/announcement/news/{id}/                # Delete news

GET    /api/announcement/holidays/                 # List holidays
POST   /api/announcement/holidays/                 # Add holiday
GET    /api/announcement/holidays/{id}/            # Get holiday
PUT    /api/announcement/holidays/{id}/            # Update holiday
DELETE /api/announcement/holidays/{id}/            # Delete holiday
```

#### Query Parameter:
```
?is_view_on_web=true    # Get only public announcements
```

---

### 8. Scholarship Module

Scholarship and donor management.

#### Endpoints:
```
GET    /api/scholarship/scholarship-candidates/    # List candidates
POST   /api/scholarship/scholarship-candidates/    # Add candidate
GET    /api/scholarship/scholarship-candidates/{id}/ # Get candidate
PUT    /api/scholarship/scholarship-candidates/{id}/ # Update candidate
DELETE /api/scholarship/scholarship-candidates/{id}/ # Delete candidate

GET    /api/scholarship/donors/                    # List donors
POST   /api/scholarship/donors/                    # Add donor
GET    /api/scholarship/donors/{id}/               # Get donor
PUT    /api/scholarship/donors/{id}/               # Update donor
DELETE /api/scholarship/donors/{id}/               # Delete donor

GET    /api/scholarship/scholarships/              # List scholarships
POST   /api/scholarship/scholarships/              # Award scholarship
GET    /api/scholarship/scholarships/{id}/         # Get scholarship
PUT    /api/scholarship/scholarships/{id}/         # Update scholarship
DELETE /api/scholarship/scholarships/{id}/         # Delete scholarship
```

---

### 9. Event Module

Event management.

#### Endpoints:
```
GET    /api/event/events/                          # List events
POST   /api/event/events/                          # Create event
GET    /api/event/events/{id}/                     # Get event
PUT    /api/event/events/{id}/                     # Update event
DELETE /api/event/events/{id}/                     # Delete event
```

---

### 10. Payroll Module

Salary management for staff.

#### Endpoints:
```
GET    /api/payroll/salary-grades/                 # List salary grades
POST   /api/payroll/salary-grades/                 # Create grade
GET    /api/payroll/salary-grades/{id}/            # Get grade
PUT    /api/payroll/salary-grades/{id}/            # Update grade
DELETE /api/payroll/salary-grades/{id}/            # Delete grade

GET    /api/payroll/salary-payments/               # List payments
POST   /api/payroll/salary-payments/               # Record payment
GET    /api/payroll/salary-payments/{id}/          # Get payment
PUT    /api/payroll/salary-payments/{id}/          # Update payment
DELETE /api/payroll/salary-payments/{id}/          # Delete payment
```

#### Example: Create Salary Grade
```bash
POST /api/payroll/salary-grades/
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "college": 1,
  "grade_name": "Senior Teacher",
  "basic_salary": 50000.00,
  "house_rent": 10000.00,
  "transport_allowance": 3000.00,
  "medical_allowance": 2000.00,
  "provident_fund": 5000.00,
  "tax_deduction": 2000.00
}

# Auto-calculated fields:
# total_allowance = 15000
# total_deduction = 7000
# gross_salary = 65000
# net_salary = 58000
```

---

### 11. Accounting Module

Complete financial management system.

#### Endpoints:
```
# Discount Management
GET    /api/accounting/discounts/
POST   /api/accounting/discounts/
GET    /api/accounting/discounts/{id}/
PUT    /api/accounting/discounts/{id}/
DELETE /api/accounting/discounts/{id}/

# Fee Types
GET    /api/accounting/fee-types/
POST   /api/accounting/fee-types/
GET    /api/accounting/fee-types/{id}/
PUT    /api/accounting/fee-types/{id}/
DELETE /api/accounting/fee-types/{id}/

# Invoices
GET    /api/accounting/invoices/
POST   /api/accounting/invoices/
GET    /api/accounting/invoices/{id}/
PUT    /api/accounting/invoices/{id}/
DELETE /api/accounting/invoices/{id}/

# Payments
GET    /api/accounting/payments/
POST   /api/accounting/payments/
GET    /api/accounting/payments/{id}/
PUT    /api/accounting/payments/{id}/
DELETE /api/accounting/payments/{id}/

# Income Management
GET    /api/accounting/income-heads/
POST   /api/accounting/income-heads/
GET    /api/accounting/income-heads/{id}/
PUT    /api/accounting/income-heads/{id}/
DELETE /api/accounting/income-heads/{id}/

GET    /api/accounting/incomes/
POST   /api/accounting/incomes/
GET    /api/accounting/incomes/{id}/
PUT    /api/accounting/incomes/{id}/
DELETE /api/accounting/incomes/{id}/

# Expenditure Management
GET    /api/accounting/expenditure-heads/
POST   /api/accounting/expenditure-heads/
GET    /api/accounting/expenditure-heads/{id}/
PUT    /api/accounting/expenditure-heads/{id}/
DELETE /api/accounting/expenditure-heads/{id}/

GET    /api/accounting/expenditures/
POST   /api/accounting/expenditures/
GET    /api/accounting/expenditures/{id}/
PUT    /api/accounting/expenditures/{id}/
DELETE /api/accounting/expenditures/{id}/
```

#### Example: Create Invoice
```bash
POST /api/accounting/invoices/
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "college": 1,
  "student": 10,
  "invoice_number": "INV-2025-001",
  "gross_amount": 50000.00,
  "discount_amount": 5000.00,
  "net_amount": 45000.00,
  "due_date": "2025-12-31"
}

# Auto-calculated:
# paid_amount = 0 (initially)
# due_amount = 45000
# paid_status = "Unpaid"
```

#### Example: Record Payment
```bash
POST /api/accounting/payments/
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "college": 1,
  "invoice": 5,
  "amount": 20000.00,
  "payment_method": "Bank Transfer",
  "payment_date": "2025-11-10",
  "note": "Partial payment for semester fee"
}

# This will update invoice:
# paid_amount = 20000
# due_amount = 25000
# paid_status = "Partial"
```

---

### 12. Reporting Module

Custom report generation (TODO: Implement business logic).

#### Endpoints:
```
GET    /api/reporting/student/                     # Student reports
GET    /api/reporting/attendance/                  # Attendance reports
GET    /api/reporting/finance/                     # Finance reports
```

---

### 13. Media Gallery Module

Photo gallery for events and activities.

#### Endpoints:
```
GET    /api/media-gallery/galleries/               # List galleries
POST   /api/media-gallery/galleries/               # Create gallery
GET    /api/media-gallery/galleries/{id}/          # Get gallery
PUT    /api/media-gallery/galleries/{id}/          # Update gallery
DELETE /api/media-gallery/galleries/{id}/          # Delete gallery

GET    /api/media-gallery/gallery-images/          # List images
POST   /api/media-gallery/gallery-images/          # Upload image
GET    /api/media-gallery/gallery-images/{id}/     # Get image
PUT    /api/media-gallery/gallery-images/{id}/     # Update image
DELETE /api/media-gallery/gallery-images/{id}/     # Delete image
```

---

### 14. Frontend CMS Module

Manage school website content.

#### Endpoints:
```
GET    /api/frontend-cms/frontend-pages/           # List pages
POST   /api/frontend-cms/frontend-pages/           # Create page
GET    /api/frontend-cms/frontend-pages/{id}/      # Get page
PUT    /api/frontend-cms/frontend-pages/{id}/      # Update page
DELETE /api/frontend-cms/frontend-pages/{id}/      # Delete page

GET    /api/frontend-cms/sliders/                  # List sliders
POST   /api/frontend-cms/sliders/                  # Create slider
GET    /api/frontend-cms/sliders/{id}/             # Get slider
PUT    /api/frontend-cms/sliders/{id}/             # Update slider
DELETE /api/frontend-cms/sliders/{id}/             # Delete slider

GET    /api/frontend-cms/about-school/             # Get about info
POST   /api/frontend-cms/about-school/             # Create about
GET    /api/frontend-cms/about-school/{id}/        # Get about
PUT    /api/frontend-cms/about-school/{id}/        # Update about
DELETE /api/frontend-cms/about-school/{id}/        # Delete about
```

---

### 15. Miscellaneous Module

Awards, todos, and FAQs.

#### Endpoints:
```
GET    /api/miscellaneous/awards/                  # List awards
POST   /api/miscellaneous/awards/                  # Create award
GET    /api/miscellaneous/awards/{id}/             # Get award
PUT    /api/miscellaneous/awards/{id}/             # Update award
DELETE /api/miscellaneous/awards/{id}/             # Delete award

GET    /api/miscellaneous/todos/                   # List todos
POST   /api/miscellaneous/todos/                   # Create todo
GET    /api/miscellaneous/todos/{id}/              # Get todo
PUT    /api/miscellaneous/todos/{id}/              # Update todo
DELETE /api/miscellaneous/todos/{id}/              # Delete todo

GET    /api/miscellaneous/faqs/                    # List FAQs
POST   /api/miscellaneous/faqs/                    # Create FAQ
GET    /api/miscellaneous/faqs/{id}/               # Get FAQ
PUT    /api/miscellaneous/faqs/{id}/               # Update FAQ
DELETE /api/miscellaneous/faqs/{id}/               # Delete FAQ
```

---

### 16. Subscription Module (SaaS)

Manage subscription plans and payments.

#### Endpoints:
```
GET    /api/subscription/subscription-plans/       # List plans
POST   /api/subscription/subscription-plans/       # Create plan
GET    /api/subscription/subscription-plans/{id}/  # Get plan
PUT    /api/subscription/subscription-plans/{id}/  # Update plan
DELETE /api/subscription/subscription-plans/{id}/  # Delete plan

GET    /api/subscription/subscriptions/            # List subscriptions
POST   /api/subscription/subscriptions/            # Create subscription
GET    /api/subscription/subscriptions/{id}/       # Get subscription
PUT    /api/subscription/subscriptions/{id}/       # Update subscription
DELETE /api/subscription/subscriptions/{id}/       # Delete subscription

GET    /api/subscription/subscription-payments/    # List payments
POST   /api/subscription/subscription-payments/    # Record payment
GET    /api/subscription/subscription-payments/{id}/ # Get payment
PUT    /api/subscription/subscription-payments/{id}/ # Update payment
DELETE /api/subscription/subscription-payments/{id}/ # Delete payment
```

---

## 🔍 Common Query Parameters

All list endpoints support these query parameters:

### Filtering
```
?field=value              # Exact match
?field__contains=value    # Contains (case-sensitive)
?field__icontains=value   # Contains (case-insensitive)
?field__gt=value          # Greater than
?field__gte=value         # Greater than or equal
?field__lt=value          # Less than
?field__lte=value         # Less than or equal
?field__in=val1,val2      # In list
```

### Search
```
?search=keyword           # Search across searchable fields
```

### Ordering
```
?ordering=field           # Ascending
?ordering=-field          # Descending
?ordering=field1,-field2  # Multiple fields
```

### Pagination
```
?page=1                   # Page number
?page_size=20             # Items per page
```

---

## 📄 Response Format

### List Response
```json
{
  "count": 100,
  "next": "http://api.../resource/?page=2",
  "previous": null,
  "results": [
    {...},
    {...}
  ]
}
```

### Detail Response
```json
{
  "id": 1,
  "field1": "value",
  "field2": "value",
  "created_at": "2025-11-09T10:30:00Z",
  "updated_at": "2025-11-09T10:30:00Z"
}
```

### Error Response
```json
{
  "detail": "Error message",
  "field_name": ["Field-specific error"]
}
```

---

## 🧪 Testing Examples

### Using cURL
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password"}'

# List resources
curl http://localhost:8000/api/library/books/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create resource
curl -X POST http://localhost:8000/api/library/books/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"college": 1, "title": "Python Programming", "book_id": "BK001"}'
```

### Using Python requests
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'email': 'admin@example.com',
    'password': 'password'
})
token = response.json()['access']

# Use token
headers = {'Authorization': f'Bearer {token}'}
books = requests.get('http://localhost:8000/api/library/books/', headers=headers)
print(books.json())
```

---

## 📚 More Documentation

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

---

**Total Endpoints:** ~658 across 43 modules
**Built with:** Django REST Framework
**Last Updated:** November 9, 2025
