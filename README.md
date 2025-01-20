

# Library Management System

The **Library Management System** is a web-based application designed to simplify the management of library resources, memberships, and transactions. This system provides functionalities for both administrators and users, adhering to role-based access and validations for smooth operations.

## Application Overview

The system consists of multiple modules:
1. **Maintenance Module** (Admin only)  
   Handles backend configurations like adding, updating, and managing library resources such as books, movies, and users.
2. **Reports Module**  
   Generates reports on various library activities such as issued books, pending fines, and membership statuses.
3. **Transactions Module**  
   Facilitates the borrowing, returning, and fine management for books and other resources.
4. **User Management Module**  
   Allows administrators to manage user memberships, including adding new users and updating membership details.

---

## Features

### General Features
- **Navigation Chart**: A chart is available on all pages to aid navigation, though it’s not required in the final application. 
- **Form Validations**: Ensures that all mandatory fields are filled before form submission.
- **Radio Buttons**: Allows selection of one option at a time.
- **Checkboxes**: Checked implies "Yes," and unchecked implies "No."
- **Hidden Passwords**: Ensures passwords are hidden while typing on login pages.

### Role-Based Access
- **Admin**: Access to Maintenance, Reports, and Transactions modules.  
- **User**: Access to Reports and Transactions modules only.  

---

## Module Details

### 1. **Maintenance Module** (Admin Only)
- **Add/Update Book**:  
  - Select between "Book" or "Movie" (default: Book).  
  - All fields are mandatory.  
  - Error message is displayed if details are incomplete.

- **Add/Update User Membership**:  
  - Select between 6 months, 1 year, or 2 years (default: 6 months).  
  - Membership number is mandatory for updates.

### 2. **Reports Module**
- Generates insights into library activities such as:
  - Issued Books
  - Memberships
  - Fines

### 3. **Transactions Module**
#### Book Issue:
- **Mandatory Fields**: Name of Book, Author (auto-populated, non-editable), Issue Date, and Return Date (default: 15 days ahead, editable to an earlier date).  
- **Remarks**: Optional.  
- Validation ensures all details are provided before submission.

#### Book Return:
- **Mandatory Fields**: Name of Book, Author (non-editable), Serial Number, Issue Date (non-editable), and Return Date.  
- If fine is applicable:
  - Fine Paid checkbox must be selected.
  - Transaction proceeds to **Fine Pay** page before completion.

#### Fine Pay:
- All fields auto-populated except "Fine Paid" and "Remarks."  
- Users must confirm fine payment before returning a book.  

---

## Assumptions and Clarifications
1. **Memberships**:
   - New memberships default to 6 months unless explicitly changed.  
   - Updates allow only extensions or cancellations.  
2. **Dates**:
   - Issue Date: Cannot be earlier than today.  
   - Return Date: Default is 15 days after the issue but can be adjusted (not exceeding 15 days).  
3. **Error Messages**:
   - Displayed on the same page for incomplete forms or invalid actions.
4. **Navigation Chart**:
   - Provided on all pages for guidance, but not required in the working application.

---

## Technical Specifications
- **Frontend**: Basic formatting is sufficient for the screens.
- **Backend**: Includes robust validations for forms and role-based access controls.
- **Security**: Passwords are hidden on login pages.

---
