
# Help Desk Web App

Aplicación web para gestión de tickets de soporte (Help Desk) desarrollada con **Flask**, **MariaDB**, **Bootstrap** y **jQuery**.

---

## Descripción
Este sistema permite:
- Registro e inicio de sesión.
- Creación y seguimiento de tickets.
- Comentarios en tickets.
- Panel de administración de usuarios (solo para rol **Admin**).
- Control de acceso por roles (**Admin**, **Agent**, **User**).

Arquitectura:
- **Frontend:** HTML + Bootstrap + jQuery.
- **Backend:** Flask (Python).
- **Base de datos:** MariaDB/MySQL.

---

## Tecnologías usadas
- Python 3.x
- Flask
- flask-mysqldb
- MariaDB/MySQL
- Bootstrap 5
- jQuery

---


## Instalación y configuración

### 1. Clonar el repositorio
git clone https://github.com/tuusuario/helpdesk.git
cd helpdesk

### 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows

### 3. Instalar dependencias
pip install -r requirements.txt

### 4. Configurar variables de entorno
Crear un archivo **.env** o exportar las variables en tu sistema:

SECRET_KEY=<tu_secreto>
MYSQL_HOST=localhost
MYSQL_USER=<usuario_mysql>
MYSQL_PASSWORD=<contraseña_mysql>
MYSQL_DB=helpdesk_db

### 5. Crear base de datos y tablas
Ejecutar en MariaDB:

CREATE DATABASE helpdesk_db;
USE helpdesk_db;

-- Crear tabla users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('ADMIN','AGENT','USER') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla tickets
CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('OPEN','IN_PROGRESS','RESOLVED','CLOSED') NOT NULL DEFAULT 'OPEN',
    priority ENUM('LOW','MEDIUM','HIGH') NOT NULL DEFAULT 'LOW',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    assigned_to INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);

-- Crear tabla ticket_comments
CREATE TABLE ticket_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    user_id INT NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);


### 6. Insertar usuario administrador

INSERT INTO users (name, email, password_hash, role)
VALUES ('Admin', 'admin@example.com', '<HASH_GENERADO>', 'ADMIN');

Nota: **<HASH_GENERADO>** debe ser creado con **generate_password_hash("tu_contrasena")** en Python.

### 7. Ejecutar la aplicacion
python run.py

Acceder en: http://localhost:5000

**Uso rapido**
1.**Inicio de session:** accede con tu email y contrasena.
2.**Dashboard:** Resumen de Tickets por estado.
3.**Tickets:**
. Crear ticket: **Tickets -> New ticket**
. Ver tickets: Tickets: **Tickets**
. Detalle: clic en el ID -> ver informacion, comentarios, cambiar estado?assign (si Admin o Agent)

4.**Usuario** (solo Admin): Ver lista y cambiar roles
5.**comentarios:** Anadir dede la vista detalle del ticket.

**Capturas y manuales**
. Manual de usuario: **docs/manual_usuario.md**
. Manual tecnico: **docs/manual_tecnico.md**
. Capturas de pantalla: **docs/screenshots/**
. login.png
. dashboard.png
. tickets_list.png
. ticket_detail.png
. users_list.png

**Repositorio Github**


**Mejora adicional**
. Dashboard con estadisticas de tickets por estado (OPEN, IN_PROGRESS< RESOLVED).
. Asignacion automatica de agentes.