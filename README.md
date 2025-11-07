# Group-Sprint-3 Flask App (CLAS)

## Overview
This repository implements a lightweight CLAS (Colby Liberal Arts Symposium) workflow using Flask. It provides:
- user registration and authentication,
- event creation/editing with draft vs. submitted states,
- scheduling,
- a visual schedule layout that lanes concurrent sessions.




## Features

- **Authentication**
  - Register, log in, log out.
  - Roles (allows a user to chooose roles when creating an account)

- **Profile & Settings**
  - Update name, role, profile photo URL, and password.

- **Event Lifecycle**
  - Create events as **draft** or **submit** them.
  - Edit and delete events you own.
  - Server-side validation for required fields on submission.
  
- **Scheduling**
  - On submission, a **Session** is created for the Event with start/end times



## UI Overview

**Landing:**  
Base entry point; loads shared layout and routes users to login or home.

**Home:**  
Dashboard for authenticated users with links to event tools and schedule.

**Login:**  
Form for returning users to authenticate; redirects to home on success.

**Register:**  
Creates new accounts; validates required info and unique email.

**Profile:**  
Read-only summary of user details and role.

**Settings:**  
Edit personal info, role, profile image, or password.

**Create Event:**  
Form to draft or submit a CLAS event; validates fields before submission.

**Edit Event:**  
Allows revision of saved drafts or correction of submitted events.

**Event List:**  
Shows all user events with options to edit, submit, or delete.

**Schedule:**  
Visual timeline of submitted sessions organized by time and lane.

**Logout:**  
Ends the current session and returns to the login page.


## Tech Stack
- **Backend:** Python 3.10+ / Flask
- **Auth:** Flask-Login
- **ORM/DB:** SQLAlchemy / SQLite
- **Templating:** Jinja2
- **Styles:** CSS (no framework dependency)


## Setup & Running Locally

### Clone and create a virtual environment
```bash
git clone https://github.com/NotSMX/Group-Sprint-3-Flask-App.git
cd Group-Sprint-3-Flask-App

python3 -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows PowerShell