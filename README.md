# Information Agency Portfolio Project

This is a Django-based web application developed as a portfolio project.  
The system represents an information agency where redactors create and manage newspapers and topics.

## ✨ Features

- User authentication (login, logout, registration)
- Custom user model `Redactor` with additional field: `years_of_experience`
- CRUD functionality for:
  - Newspapers 📰
  - Topics 🏷
  - Redactors 🧑‍💼
- Search functionality
- Bootstrap UI integration
- Many-to-many relations:
  - Redactors ↔ Newspapers
  - Topics ↔ Newspapers

## 📌 Tech Stack

| Technology | Version |
|-----------|---------|
| Python | 3.12+ |
| Django | 5.x |
| Bootstrap | 5.x |

## 🚀 Install & Run locally

```bash
git clone https://github.com/YOUR-USERNAME/Information-agency-Portfolio-Project.git
cd Information-agency-Portfolio-Project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

##  Test Login

- login: user
- password: user12345

