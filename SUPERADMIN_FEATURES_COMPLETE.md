# Superadmin Portal - Complete Feature List

## 📋 Navigation Structure

```
Superadmin Portal
├── Dashboard
├── Theme Management
├── Language Management
├── Administrator
│   ├── General Settings
│   ├── Manage School/College
│   ├── Payment Settings
│   ├── SMS Settings
│   ├── Email Settings
│   ├── Academic Year
│   ├── User Role (ACL) ✅ Built
│   ├── Role Permission (ACL) ✅ Built
│   ├── Manage Super Admin
│   ├── Manage User
│   ├── Reset User Password
│   ├── Reset Username
│   ├── User Credentials
│   ├── Activity Log
│   ├── Feedback
│   └── Backup Database
├── Template
│   ├── SMS Template
│   └── Email Template
├── Front Office
│   ├── Visitor Purpose
│   ├── Visitor Info
│   ├── Call Log
│   ├── Postal Dispatch
│   └── Postal Receive
├── Human Resource
│   ├── Designation
│   └── Employee
├── Teacher
│   ├── Department
│   ├── Teacher
│   ├── Teacher Lecture
│   └── Rating
├── Leave Management
│   ├── Leave Type
│   ├── Leave Application
│   ├── Waiting Application
│   ├── Approved Application
│   └── Declined Application
├── Academic
│   ├── Class
│   ├── Section
│   ├── Subject
│   ├── Syllabus
│   └── Study Material
└── Live Class & Assignment
    ├── Live Class
    └── Assignment
```

---

## 🎯 ADMINISTRATOR MODULE

### 1. Manage Super Admin

**Purpose**: Add/edit superadmin users with full details

**Database Model**: `SuperAdmin` (extends User)
```python
# Fields
- Basic Info: name, national_id, phone, gender, blood_group, religion
- birth_date, present_address, permanent_address
- Academic: email, username, password (Argon2 hashed)
- role_id (defaults to Superadmin)
- Files: resume_url, photo_url
- other_info
```

**API Endpoints**:
```
GET    /api/superadmins/          # List all superadmins
POST   /api/superadmins/          # Create new superadmin
GET    /api/superadmins/{id}/     # Get details
PUT    /api/superadmins/{id}/     # Update
DELETE /api/superadmins/{id}/     # Delete
```

**Form Fields**:
- Name* (required)
- National ID
- Phone* (required)
- Gender* (Male/Female dropdown)
- Blood Group (A+, A-, B+, B-, O+, O-, AB+, AB-)
- Religion
- Birth Date* (date picker)
- Present Address
- Permanent Address
- Email
- Username* (unique)
- Password* (strong validation)
- Role* (Superadmin - auto-selected)
- Resume (upload: .pdf, .doc, .docx, .ppt, .pptx, .txt)
- Photo (upload: .jpg, .jpeg, .png, .gif, max 120x130px)
- Other Info (textarea)

---

### 2. Manage User

**Purpose**: View all users, activate/deactivate, edit by redirecting to specific management pages

**Features**:
- Select school dropdown
- User type filter (Admin, Teacher, Student, Guardian, Staff, etc.)
- Table with: SL, School, Photo, Name, Email, Username, Phone, Status, Action
- Actions:
  - **Set Active/Inactive**: Toggle user status
  - **Edit**: Redirect to respective management page
  - **Delete**: Remove user

**API Endpoints**:
```
GET    /api/users/                    # List all users (with filters)
GET    /api/users/{id}/               # Get user details
PUT    /api/users/{id}/status/        # Toggle active/inactive
DELETE /api/users/{id}/               # Delete user
```

**Special Behavior**:
- If user is_active = False, login returns: "Account is inactive. Please contact administrator."

---

### 3. Reset User Password

**Purpose**: Admin can reset password for any user

**Form Fields**:
- School Name* (dropdown)
- User Type* (Admin, Guardian, Student, Teacher, Accountant, Librarian, Receptionist, Staff, etc.)
- User* (dropdown - dynamically loaded based on user type)
- Password* (new password)
- Confirm Password*

**API Endpoint**:
```
POST   /api/users/reset-password/
```

**Request Body**:
```json
{
  "school_id": 1,
  "user_type": "Teacher",
  "user_id": 42,
  "new_password": "NewSecurePass123"
}
```

---

### 4. Reset Username

**Purpose**: Admin can change username for any user

**Form Fields**:
- School Name* (dropdown)
- User Type* (dropdown)
- User* (dropdown)
- New Username*

**API Endpoint**:
```
POST   /api/users/reset-username/
```

---

### 5. Manage User Credentials

**Purpose**: View login credentials of any user

**Features**:
- Search by: School Name, User Type, User Name
- Table displays: SL, School, Photo, Name, Phone, Email, Username, Password (masked), Action
- Action: **View** button shows full details in modal:
  - School Name
  - Username
  - Name
  - Department
  - National ID / Phone
  - Present Address / Permanent Address / Gender
  - Blood Group / Religion / Birth Date
  - Joining Date
  - Role
  - Salary Grade / Salary Type
  - Email
  - Other Info
  - Photo / Resume

**API Endpoint**:
```
GET    /api/users/credentials/?school_id=1&user_type=Teacher&search=John
```

---

### 6. Activity Log

**Purpose**: Audit trail of all user actions

**Database Model**: `ActivityLog` (already exists as `audit_logs`)
```python
# Fields
- id, user_id, action, table_name, record_id
- old_values (JSONB), new_values (JSONB)
- college_id, ip_address, user_agent
- timestamp
```

**Features**:
- Table: SL, Checkbox, School, User Name, Phone, Email, Activity Description, Date/Time, Action
- Bulk delete (checkboxes)
- Export all logs (CSV/PDF)
- Delete individual log

**API Endpoints**:
```
GET    /api/activity-logs/            # List all logs
DELETE /api/activity-logs/{id}/       # Delete log
POST   /api/activity-logs/export/     # Export logs
DELETE /api/activity-logs/bulk/       # Bulk delete
```

---

### 7. Feedback

**Purpose**: View feedback from guardians/users

**Database Model**: `Feedback`
```python
# Fields
- id, school_id, user_id, user_type
- feedback_text, rating (1-5)
- created_at
```

**API Endpoints**:
```
GET    /api/feedback/           # List feedback
POST   /api/feedback/           # Submit feedback (from user portal)
DELETE /api/feedback/{id}/      # Delete feedback
```

---

### 8. Backup Database

**Purpose**: Download database backups for selected schools

**Features**:
- Multi-school selector (checkboxes)
- Download button for each selected school
- Creates SQL dump file

**API Endpoint**:
```
POST   /api/database/backup/
```

**Request Body**:
```json
{
  "school_ids": [1, 2, 3]
}
```

**Response**: Returns download URL for .sql file

---

## 📧 TEMPLATE MODULE

### 1. SMS Template

**Purpose**: Pre-defined SMS templates for different user types

**Database Model**: `SMSTemplate`
```python
# Fields
- id, school_id, receiver_type
- title, template, dynamic_tags
- created_at
```

**Form Fields**:
- School Name* (dropdown)
- Receiver Type* (Admin, Guardian, Student, Teacher, Accountant, Librarian, Staff, etc.)
- Title*
- Template* (textarea with dynamic tags)
- Dynamic Tags (info box showing available variables)

**Dynamic Tags Example**:
```
{name}, {email}, {phone}, {school_name}, {date}, {time}
```

**API Endpoints**:
```
GET    /api/sms-templates/          # List all templates
POST   /api/sms-templates/          # Create template
PUT    /api/sms-templates/{id}/     # Update
DELETE /api/sms-templates/{id}/     # Delete
```

---

### 2. Email Template

**Purpose**: Pre-defined email templates (similar to SMS)

**Database Model**: `EmailTemplate`
```python
# Fields (same as SMSTemplate)
- id, school_id, receiver_type
- title, template, dynamic_tags
- created_at
```

**API Endpoints**: Same structure as SMS templates

---

## 🏢 FRONT OFFICE MODULE

### 1. Visitor Purpose

**Database Model**: `VisitorPurpose`
```python
# Fields
- id, school_id, purpose_description
```

**API Endpoints**:
```
GET    /api/visitor-purposes/
POST   /api/visitor-purposes/
PUT    /api/visitor-purposes/{id}/
DELETE /api/visitor-purposes/{id}/
```

---

### 2. Visitor Info

**Database Model**: `Visitor`
```python
# Fields
- id, school_id, name, phone
- meet_user_type, to_meet_user_id
- visitor_purpose_id, note
- check_in_time, check_out_time
```

**Form Fields**:
- School Name* (dropdown)
- Name*
- Phone*
- Meet User Type* (Staff, Student, Faculty)
- To Meet* (dropdown of users)
- Visitor Purpose* (dropdown)
- Note
- Check In Time (auto or manual)
- Check Out Time (filled when visitor leaves)

**API Endpoints**:
```
GET    /api/visitors/
POST   /api/visitors/              # Check in
PUT    /api/visitors/{id}/         # Check out / Update
DELETE /api/visitors/{id}/
GET    /api/users-to-meet/?school_id=1&user_type=Staff
```

---

### 3. Call Log

**Database Model**: `CallLog`
```python
# Fields
- id, school_id, name, phone
- call_duration, call_date, follow_up
- call_type (Incoming/Outgoing), note
```

**Form Fields**:
- School Name* (dropdown)
- Name*
- Phone*
- Call Duration* (in minutes)
- Call Date* (date picker)
- Follow Up (date picker, optional)
- Call Type* (Incoming/Outgoing radio buttons)
- Note

**API Endpoints**:
```
GET    /api/call-logs/
POST   /api/call-logs/
PUT    /api/call-logs/{id}/
DELETE /api/call-logs/{id}/
```

---

### 4. Postal Dispatch

**Database Model**: `PostalDispatch`
```python
# Fields
- id, school_id, to_title, reference
- address, from_title, dispatch_date
- note, attachment_url
```

**Form Fields**:
- School Name* (dropdown)
- To Title*
- Reference
- Address*
- From Title
- Dispatch Date* (date picker)
- Note
- Attachment (file upload)

**API Endpoints**:
```
GET    /api/postal-dispatches/
POST   /api/postal-dispatches/
PUT    /api/postal-dispatches/{id}/
DELETE /api/postal-dispatches/{id}/
POST   /api/upload-attachment/
```

---

### 5. Postal Receive

**Database Model**: `PostalReceive`
```python
# Fields (similar to PostalDispatch)
- id, school_id, to_title, reference
- address, from_title, receive_date
- note, attachment_url
```

**API Endpoints**: Same structure as Postal Dispatch

---

## 👥 HUMAN RESOURCE MODULE

### 1. Designation

**Database Model**: `Designation`
```python
# Fields
- id, school_id, name, note
```

**Form Fields**:
- School Name* (dropdown)
- Designation Name* (unique per school)
- Note (optional)

**API Endpoints**:
```
GET    /api/designations/
POST   /api/designations/
PUT    /api/designations/{id}/
DELETE /api/designations/{id}/      # Check: No employees assigned
```

---

### 2. Employee

**Database Model**: `Employee` (extends User)
```python
# All User fields +
- designation_id
- salary_grade_id, salary_type_id
- is_view_on_web, display_order
- Social media URLs (facebook, linkedin, twitter, instagram, youtube, pinterest)
```

**Form Structure** (3 tabs):
1. **Basic Information**:
   - Name*, National ID, Phone*
   - Designation*, Gender*, Blood Group
   - Religion, Birth Date*
   - Present Address*, Permanent Address

2. **Academic Information**:
   - Email, Username*, Password*
   - Salary Grade*, Salary Type*
   - Role*, Joining Date*
   - Resume (upload)

3. **Other Information**:
   - Is View on Web (Yes/No)
   - Social Media URLs (6 fields)
   - Other Info (textarea)
   - Photo (upload 120x130px)

**Special Feature**: Update Order (drag & drop to reorder employees for display)

**API Endpoints**:
```
GET    /api/employees/
POST   /api/employees/
GET    /api/employees/{id}/
PUT    /api/employees/{id}/
DELETE /api/employees/{id}/
PUT    /api/employees/update-order/
```

---

## 👨‍🏫 TEACHER MODULE

### 1. Department

**Database Model**: `Department`
```python
# Fields
- id, school_id, title, note
```

**Similar to Designation but for academic departments**

**API Endpoints**:
```
GET    /api/departments/
POST   /api/departments/
PUT    /api/departments/{id}/
DELETE /api/departments/{id}/       # Check: No teachers/classes assigned
```

---

### 2. Teacher

**Database Model**: `Teacher` (extends User)
```python
# Similar to Employee but:
- department_id (instead of designation_id)
- role_id defaults to "Teacher"
```

**Form is identical to Employee** but with:
- Department dropdown instead of Designation
- Role auto-selected as "Teacher"

**API Endpoints**:
```
GET    /api/teachers/
POST   /api/teachers/
GET    /api/teachers/{id}/
PUT    /api/teachers/{id}/
DELETE /api/teachers/{id}/
PUT    /api/teachers/update-order/
```

---

### 3. Teacher Lecture (Class Lecture)

**Database Model**: `ClassLecture`
```python
# Fields
- id, school_id, title
- class_id, section_id, subject_id
- teacher_id, lecture_type_id
- note, academic_year_id
```

**Form Fields**:
- School Name* (dropdown)
- Title*
- Class* (dropdown)
- Section* (dropdown based on class)
- Subject* (dropdown based on class/section)
- Lecture Type* (Regular, Practical, Special)
- Teacher* (dropdown)
- Note

**API Endpoints**:
```
GET    /api/class-lectures/
POST   /api/class-lectures/
PUT    /api/class-lectures/{id}/
DELETE /api/class-lectures/{id}/
```

---

### 4. Rating

**Database Model**: `Rating`
```python
# Fields
- id, school_id
- teacher_id or department_id
- rating_value (1-5), comment
- student_id (rater)
- created_at
```

**Features**: View-only interface showing teacher/department ratings

**API Endpoints**:
```
GET    /api/ratings/?teacher_id=42
GET    /api/ratings/?department_id=5
```

---

## 🏖️ LEAVE MANAGEMENT MODULE

### 1. Leave Type

**Database Model**: `LeaveTypeDefinition`
```python
# Fields
- id, school_id, applicant_type
- leave_type_name, total_leave_days_allowed
```

**Form Fields**:
- School Name* (dropdown)
- Applicant Type* (Employee, Teacher, Student)
- Leave Type* (e.g., "Sick Leave", "Casual Leave")
- Total Leave Days* (numeric)

**API Endpoints**:
```
GET    /api/leave-type-definitions/
POST   /api/leave-type-definitions/
PUT    /api/leave-type-definitions/{id}/
DELETE /api/leave-type-definitions/{id}/
```

---

### 2. Leave Application

**Database Model**: `LeaveApplication`
```python
# Fields
- id, school_id, academic_year_id
- applicant_type, applicant_id
- leave_type_definition_id
- application_date, leave_from, leave_to
- total_days_requested, leave_reason
- attachment_url, status (Waiting/Approved/Declined)
- approved_by_id, decline_reason
```

**Form Fields**:
- School Name* (dropdown)
- Academic Year* (dropdown)
- Applicant Type* (dropdown)
- Applicant* (dropdown - dynamic based on type)
- Leave Type* (dropdown)
- Application Date* (date picker)
- Leave From* (date picker)
- Leave To* (date picker)
- Leave Reason* (textarea)
- Attachment (file upload)

**API Endpoints**:
```
GET    /api/leave-applications/                    # All applications
GET    /api/leave-applications/?status=waiting     # Waiting for approval
GET    /api/leave-applications/?status=approved    # Approved
GET    /api/leave-applications/?status=declined    # Declined
POST   /api/leave-applications/                    # Submit application
PUT    /api/leave-applications/{id}/               # Update/Approve/Decline
DELETE /api/leave-applications/{id}/
```

---

## 📚 ACADEMIC MODULE

### 1. Class

**Database Model**: `SchoolClass`
```python
# Fields
- id, school_id, name (e.g., "Grade 1")
- numeric_name (e.g., 1, 2, 10)
- class_teacher_id, note
```

**Form Fields**:
- School Name* (dropdown)
- Class Name* (text, e.g., "Grade 1", "MCA")
- Numeric Name* (number, e.g., 1, 2, 10)
- Class Teacher (dropdown of teachers)
- Note

**API Endpoints**:
```
GET    /api/classes/
POST   /api/classes/
PUT    /api/classes/{id}/
DELETE /api/classes/{id}/           # Check: No sections/students assigned
```

---

### 2. Section

**Database Model**: `ClassSection`
```python
# Fields
- id, school_id, class_id
- name (e.g., "A", "B")
- section_teacher_id, note
```

**Form Fields**:
- School Name* (dropdown)
- Section Name* (text, e.g., "A", "B")
- Class* (dropdown)
- Section Teacher (dropdown)
- Note

**API Endpoints**:
```
GET    /api/sections/?class_id=1
POST   /api/sections/
PUT    /api/sections/{id}/
DELETE /api/sections/{id}/
```

---

### 3. Subject

**Database Model**: `Subject`
```python
# Fields
- id, school_id, class_id
- name, subject_code, author
- type (Core/Elective/Optional)
- teacher_id, note
```

**Form Fields**:
- School Name* (dropdown)
- Subject Name* (text)
- Subject Code (text, optional)
- Author (text, optional)
- Type* (Core/Elective/Optional dropdown)
- Class* (dropdown)
- Teacher* (dropdown)
- Note

**API Endpoints**:
```
GET    /api/subjects/?class_id=1
POST   /api/subjects/
PUT    /api/subjects/{id}/
DELETE /api/subjects/{id}/
```

---

### 4. Syllabus

**Database Model**: `Syllabus`
```python
# Fields
- id, school_id, title
- class_id, subject_id, session_year_id
- syllabus_file_url, note
```

**Form Fields**:
- School Name* (dropdown)
- Title* (text)
- Class* (dropdown)
- Subject* (dropdown based on class)
- Syllabus* (file upload: .pdf, .doc, .docx, .pptx, .txt)
- Note

**API Endpoints**:
```
GET    /api/syllabi/?class_id=1&subject_id=5
POST   /api/syllabi/
PUT    /api/syllabi/{id}/
DELETE /api/syllabi/{id}/
POST   /api/upload-syllabus-file/
```

---

### 5. Study Material

**Database Model**: `StudyMaterial`
```python
# Fields
- id, school_id, title
- class_id, subject_id
- material_file_url, description
```

**Form Fields**:
- School Name* (dropdown)
- Title* (text)
- Class* (dropdown)
- Subject* (dropdown)
- Material* (file upload)
- Description (textarea)

**API Endpoints**:
```
GET    /api/study-materials/?class_id=1
POST   /api/study-materials/
PUT    /api/study-materials/{id}/
DELETE /api/study-materials/{id}/
POST   /api/upload-study-material-file/
```

---

## 💻 LIVE CLASS & ASSIGNMENT MODULE

### 1. Live Class

**Database Model**: `LiveClass`
```python
# Fields
- id, school_id, class_id, section_id
- subject_id, teacher_id
- live_class_type_id
- class_date, start_time, end_time
- note, send_notification
- status
```

**Form Fields**:
- School Name* (dropdown)
- Class* (dropdown)
- Section* (dropdown)
- Subject* (dropdown)
- Teacher* (dropdown)
- Live Class Type* (dropdown)
- Class Date* (date picker)
- Start Time* (time picker)
- End Time* (time picker)
- Note
- Send Notification (checkbox)

**API Endpoints**:
```
GET    /api/live-classes/
POST   /api/live-classes/
PUT    /api/live-classes/{id}/
DELETE /api/live-classes/{id}/
```

---

### 2. Assignment

**Database Model**: `Assignment`
```python
# Fields
- id, school_id, title
- class_id, section_id, subject_id
- assignment_date, submission_date
- attachment_url, note
- status
```

**Form Fields**:
- School Name* (dropdown)
- Title* (text)
- Class* (dropdown)
- Section* (dropdown)
- Subject* (dropdown)
- Assignment Date* (date picker)
- Submission Date* (date picker)
- Attachment (file upload)
- Note

**API Endpoints**:
```
GET    /api/assignments/
POST   /api/assignments/
PUT    /api/assignments/{id}/
DELETE /api/assignments/{id}/
POST   /api/upload-assignment-file/
```

---

## 📊 Summary

### Total Features Documented: 40+

### Module Breakdown:
- **Administrator**: 8 features
- **Template**: 2 features
- **Front Office**: 5 features
- **Human Resource**: 2 features
- **Teacher**: 4 features
- **Leave Management**: 2 features (+ 3 filtered views)
- **Academic**: 5 features
- **Live Class & Assignment**: 2 features

### Database Tables to Create: 30+

### API Endpoints to Build: 150+

---

## 🚀 Next Steps

1. **Restore your PostgreSQL database** to see existing data structure
2. **Build authentication APIs first** (login, logout, permissions)
3. **Build role management APIs** (already have models & serializers)
4. **Incrementally build feature APIs** starting with most critical
5. **Test each module** with Postman/curl
6. **Build frontend** once APIs are stable

---

**Status**: Complete feature documentation ready ✅
**Next**: Build API views for these features 🚧
