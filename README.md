# Placement Readiness System

A Flask-based web application that helps students evaluate their placement readiness by analyzing their performance in aptitude, coding, technical, and communication skills. Based on the entered scores, the system identifies strengths and weaknesses, calculates placement readiness, recommends learning resources, and displays eligible companies.

## Features

### Student Features

* User registration and login
* Secure session-based authentication
* Dashboard for logged-in users
* Enter scores for:

  * Aptitude
  * Coding
  * Technical Skills
  * Communication Skills
* Placement readiness analysis
* Skill-wise improvement suggestions
* Recommended learning resources
* View eligible companies based on performance
* Progress tracking

### Admin Features

* Add new companies
* Define minimum eligibility criteria for each company
* View all registered company requirements

## Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS
* **Database:** SQLite
* **Template Engine:** Jinja2

## Project Structure

```text
Place-Prep/
└── placement-readiness-system/
    ├── app.py
    ├── database.db
    ├── static/
    │   └── style.css
    └── templates/
        ├── admin.html
        ├── dashboard.html
        ├── evaluate.html
        ├── index.html
        ├── login.html
        ├── progress.html
        ├── register.html
        ├── scores.html
        └── tests.html
```

## How It Works

1. A user registers and logs in.
2. The user enters scores for aptitude, coding, technical, and communication skills.
3. The application:

   * Calculates placement readiness.
   * Identifies weak skill areas.
   * Suggests improvement strategies.
   * Recommends learning platforms.
   * Compares scores against company eligibility criteria.
4. The user can monitor progress over time.

## Default Company Eligibility

The application initializes the database with sample companies and their eligibility criteria:

| Company | Aptitude | Coding | Technical | Communication |
| ------- | -------: | -----: | --------: | ------------: |
| TCS     |       60 |     50 |        55 |            60 |
| Infosys |       65 |     60 |        60 |            65 |
| Amazon  |       75 |     80 |        80 |            70 |

Additional companies can be added through the Admin page.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/vaishnavi112006/Place-Prep.git
```

### 2. Navigate to the project folder

```bash
cd Place-Prep/placement-readiness-system
```

### 3. Install Flask

```bash
pip install flask
```

### 4. Run the application

```bash
python app.py
```

### 5. Open your browser

```
http://127.0.0.1:5000
```

## Learning Resources Recommended

The application recommends resources based on weak skill areas, including:

* IndiaBIX (Aptitude Practice)
* LeetCode (Coding Practice)
* NPTEL (Core Computer Science)
* Coursera (Communication Skills)

## Future Enhancements

* Password encryption
* Student profile management
* Company-wise analytics dashboard
* Resume builder
* Mock interview module
* Email notifications
* Charts and graphical progress reports
* AI-powered placement recommendations

## Skills Demonstrated

* Python Programming
* Flask Web Development
* SQLite Database Management
* CRUD Operations
* Authentication & Session Management
* HTML & CSS
* Git & GitHub
* Web Application Development

## Author

**Vaishnavi**

GitHub: https://github.com/vaishnavi112006
