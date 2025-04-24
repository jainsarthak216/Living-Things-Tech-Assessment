# 📝 Task Management Application

This is a full-stack application that supports:
- ✅ User Authentication via Node.js backend
- ✅ Task Creation, Update, Delete via Django REST API
- ✅ Exporting Tasks to Excel
- ✅ Frontend in Vue.js

---

## 📦 Project Structure

```
project-root/
├── frontend/        # Vue.js app
├── backend1/        # Node.js Auth API (JWT)
├── backend2/        # Django DRF API for tasks + Excel export
└── README.md
```

---

## ⚙️ Setup Instructions

### 📁 1. Backend1 – Node.js (Auth API)

#### ✅ Requirements
- Node.js v14+

#### 🔧 Setup
```
cd backend1
npm install
```

#### 🔑 Create `.env`
```
JWT_SECRET=super_secret_key
```

#### 🚀 Start Server
```bash
node server.js
```

> Runs on: `http://localhost:3000`

#### 🧪 Endpoints
- `POST /api/register` — `{ email, password }`
- `POST /api/login` — `{ email, password }` → `{ token }`

---

### 📁 2. Backend2 – Django + DRF (Task API)

#### ✅ Requirements
- Python 3.8+
- pip / venv

#### 🔧 Setup
```bash
cd backend2
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, create one:
```txt
Django
djangorestframework
openpyxl
PyJWT
```

#### ⚙️ Migrate DB
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 🚀 Run Server
```bash
python manage.py runserver 8000
```

> Runs on: `http://localhost:8000`

#### 🧪 API Endpoints
- `GET/POST /api/tasks/` — List or Create tasks
- `PUT/DELETE /api/tasks/<id>/` — Update/Delete task
- `GET /api/tasks/export/` — Download tasks as Excel

> 🔒 Pass the token from Node backend as `Authorization: Bearer <JWT>` header

---

### 📁 3. Frontend – Vue.js App

#### ✅ Requirements
- Node.js
- Vue CLI (Optional)

#### 🔧 Setup
```bash
cd frontend
npm install
npm run dev  # or npm run serve
```

#### 🔌 Configuration
Make sure API URLs point to:

- Auth: `http://localhost:3000/api`
- Tasks: `http://localhost:8000/api/tasks/`

---

## 🔐 Auth Flow

1. Register/Login via Node.js → Receive JWT
2. Store JWT in localStorage
3. Use JWT for authenticated requests to the Django task API

---

## 📤 Export to Excel

- Click **"Export to Excel"** on frontend
- Triggers `GET /api/tasks/export/`
- Downloads `.xlsx` file containing the user's tasks

---

## 🛠 Development Notes

- JWT is validated in Django using the same secret key (`super_secret_key`)
- User IDs from token (`id`) are used to link tasks

---

## 📬 API Interop Sample

**Request Header** (to Django from Vue):
```
Authorization: Bearer <token_from_node>
```

---

## ✅ To Do
- [ ] Vue task views (create/edit/delete)
- [ ] Vue route guards with token
- [ ] Deploy-ready `.env` configs
