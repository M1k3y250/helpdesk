
# Manual Técnico - Help Desk Web App

Este documento describe la arquitectura, instalación y funcionamiento técnico de la aplicación web Help Desk desarrollada con Flask, MariaDB, Bootstrap y jQuery.

## Descripción del sistema
Aplicación web para gestión de tickets de soporte, desarrollada con:
- **Backend:** Flask (Python)
- **Base de datos:** MariaDB/MySQL
- **Frontend:** HTML, Bootstrap, jQuery

**Funcionalidades principales**

Gestion de tickets (crear, ver, actualizar estado y asignar agente)
Comentarios en tickets
Gestion de usuarios (solo admin)
Seguridad por roles (**Admin** , **Agent** , **User**)



---

## Arquitectura

La aplicación sigue una arquitectura cliente-servidor compuesta por tres capas principales:

- **Capa de presentación (Frontend):**
  - HTML5 para la estructura de las páginas.
  - Bootstrap 5 para diseño responsivo y estilos.
  - jQuery para interacción dinámica y mejoras de experiencia de usuario.

- **Capa de lógica (Backend):**
  - Framework Flask (Python) para manejar rutas, lógica de negocio y control de acceso.
  - Uso de Blueprints para organizar las rutas (login, tickets, usuarios).
  - Gestión de sesiones y autenticación con `Werkzeug` (hash de contraseñas).
  - Control de acceso por rol mediante decoradores

- **Capa de datos (Base de datos):**
  - MariaDB/MySQL para almacenamiento persistente.
  - Tablas principales: `users`, `tickets`, `ticket_comments`.
  - Conexión mediante `flask-mysqldb` usando parámetros seguros (SQL parametrizado).

**Flujo general:**

- Autenticación y autorización por roles (**Admin**, **Agent**, **User**).
- CRUD de tickets y comentarios.
- Panel de administración de usuarios (solo Admin).
- Seguridad básica: contraseñas hasheadas, control de sesión, consultas parametrizadas.


---

## Estructura del proyecto
```
helpdesk/
├─ app/
│  ├─ __init__.py        # Inicialización Flask + MySQL
│  └─routes.py          # Rutas (login, tickets, usuarios)
├─ templates/            # HTML (base, login, dashboard, tickets, users)
│  ├─base.html
│  ├─login.html
│  ├─dashboard.html
│  ├─ticket_detail.html
│  ├─tickets_list.html
│  ├─tickets_new.html
│  └─users_list.html
├─ static/               # CSS y JS
├─ docs/                 # Manuales y capturas
│  ├─ manual_usuario.md
│  ├─ manual_tecnico.md
│  ├─ er_diagram.png
│  └─ screenshots/
├─ config.py             # Configuración (SECRET_KEY, MYSQL_*)
├─ run.py                # Punto de entrada
├─ requirements.txt      # Dependencias
├─ README.md
└─ venv/                 # Entorno virtual
```

---

## Diagrama ER
El diagrama entidad-relación se encuentra en `docs/er_diagram.png`.


---

## Tablas principales:
- **users**: id, name, email, password_hash, role, created_at
- **tickets**: id, title, description, status, priority, created_at, updated_at, created_by, assigned_to
- **ticket_comments**: id, ticket_id, user_id, comment, created_at


---

## Instalación
### Requisitos
- Python 3.x
- MariaDB/MySQL
- Git

### Pasos
a. Clonar el repositorio:
bash
git clone https://github.com/M1k3y250/helpdesk.git
cd helpdesk

b. Crear entorno virtual
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows

c. Instalar dependencias
`pip install -r requirements.txt`

d. Configurar variables de entorno

e. Crear base de datos y tablas, Ejecutar el script SQL:
CREATE DATABASE helpdesk_db;
USE helpdesk_db;
CREATE TABLE users (...);
CREATE TABLE tickets (...);
CREATE TABLE ticket_comments (...);

f. Insertar usuario administrador

INSERT INTO users (name, email, password_hash, role)
VALUES ('Admin', 'admin@example.com', '<HASH_GENERADO>', 'ADMIN');

g. Ejecutar la aplicación
`python run.py`

h. Accede en: `http://127.0.0.1:5000/login`


---

## Seguridad
- Contraseñas hasheadas (`generate_password_hash`, `check_password_hash`).
- SQL parametrizado (evita inyección).
- Control de acceso por rol (`login_required`, `role_required`).
- SECRET_KEY robusto para sesiones.


---

## Mejora adicional
- Asignacion de agentes y se refleja en la vista principal del Dashboard


---

## Capturas
Las capturas se encuentran en `docs/screenshots/`:
- login.png
- dashboard.png
- tickets_list.png
- ticket_detail.png
- users_list.png


