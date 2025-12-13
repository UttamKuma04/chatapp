# ChatApp (Django)

A simple real-time style chat application built using **Python** and **Django**. This project demonstrates Django fundamentals such as apps, templates, database models, and basic message handling.

---

## 📁 Project Structure

```
chatapp/
│
├── app/                # Main Django app (views, models, urls)
├── templates/          # HTML templates
├── .tables/            # Database-related tables/configs
├── db.sqlite3          # SQLite database
├── manage.py           # Django project runner
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🚀 Features

* User-friendly chat interface
* Django template-based frontend
* SQLite database integration
* Clean project structure
* Beginner-friendly Django setup

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS (Django Templates)
* **Database:** SQLite3

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/UttamKuma04/chatapp.git
   cd chatapp
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the development server**

   ```bash
   python manage.py runserver
   ```

6. Open your browser and visit:

   ```
   http://127.0.0.1:8000/
   ```

---

## 📦 Requirements

All required packages are listed in `requirements.txt`. Main dependency:

* Django

---

## 🧪 Usage

* Run the server
* Open the app in your browser
* Start chatting using the provided interface

---

## 📌 Future Improvements

* User authentication (login/signup)
* Real-time chat using WebSockets (Django Channels)
* Message timestamps & read receipts
* User profile & avatars
* Deployment (Render / Railway / AWS)

---

## 👤 Author

**Uttam Kumar**
GitHub: [@UttamKuma04](https://github.com/UttamKuma04)

---

## 📄 License

This project is open-source and available under the **MIT License**.
