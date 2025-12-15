from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session, flash, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from werkzeug.security import check_password_hash

bp = Blueprint("routes", __name__)

# ----- Decoradores -----
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión.", "warning")
            return redirect(url_for("routes.login_view"))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_role" not in session:
                flash("Debes iniciar sesión.", "warning")
                return redirect(url_for("routes.login_view"))

            if session["user_role"] not in roles:
                flash("No tienes permiso para acceder a esta página.", "danger")
                return redirect(url_for("routes.tickets_list"))

            return f(*args, **kwargs)
        return decorated_function
    return decorator



# ----- Rutas públicas -----
@bp.route("/")
def home():
    return "Helpdesk API funcionando correctamente."

@bp.route("/test-db")
def test_db():
    from app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT 'Conexion exitosa a MariaDB!' AS mensaje;")
    result = cur.fetchone()
    cur.close()
    return jsonify({"status": "ok", "db_message": result[0]})

# ----- Login -----
@bp.route("/login", methods=["GET", "POST"])
def login_view():
    from app import mysql

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            print("PASSWORD DESDE DB:", repr(user[3]))

            # user[3] es la columna 'password' en la DB
            if check_password_hash(user[3], password):
                session["user_id"] = user[0]
                session["user_name"] = user[1]
                session["user_role"] = user[4]
                flash(f"Bienvenido, {user[1]}!", "success")
                return redirect(url_for("routes.dashboard"))
            else:
                flash("Correo o contraseña inválidos.", "danger")
        else:
            flash("Correo o contraseña inválidos.", "danger")

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("routes.login_view"))

# ----- Dashboard -----
@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# ----- Tickets -----
@bp.route("/tickets")
@login_required
def tickets_list():
    user_id = session["user_id"]
    user_role = session["user_role"]

    from app import mysql
    from MySQLdb.cursors import DictCursor  # <- agregar esta línea

    # Usar DictCursor
    cur = mysql.connection.cursor(DictCursor)

    if user_role == "ADMIN":
        cur.execute("""
            SELECT t.*, u.name AS created_by_name, a.name AS assigned_to_name
            FROM tickets t
            JOIN users u ON t.user_id = u.id
            LEFT JOIN users a ON t.assigned_to = a.id
            ORDER BY t.created_at DESC
        """)
    elif user_role == "AGENT":
        cur.execute("""
            SELECT t.*, u.name AS created_by_name, a.name AS assigned_to_name
            FROM tickets t
            JOIN users u ON t.user_id = u.id
            LEFT JOIN users a ON t.assigned_to = a.id
            WHERE t.assigned_to = %s OR t.assigned_to IS NULL
            ORDER BY t.created_at DESC
        """, (user_id,))
    else:  # USER
        cur.execute("""
            SELECT t.*, u.name AS created_by_name, a.name AS assigned_to_name
            FROM tickets t
            JOIN users u ON t.user_id = u.id
            LEFT JOIN users a ON t.assigned_to = a.id
            WHERE t.user_id = %s
            ORDER BY t.created_at DESC
        """, (user_id,))

    tickets = cur.fetchall()
    cur.close()
    return render_template("tickets_list.html", tickets=tickets)




@bp.route("/tickets/new", methods=["GET", "POST"])
@login_required
def tickets_new():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority")

        from app import mysql
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO tickets (user_id, title, description, priority) VALUES (%s, %s, %s, %s)",
            (session["user_id"], title, description, priority)
        )
        mysql.connection.commit()
        cur.close()

        flash("Ticket creado correctamente.", "success")
        return redirect(url_for("routes.tickets_list"))

    return render_template("tickets_new.html")



@bp.route("/tickets/<int:ticket_id>")
@login_required
def ticket_detail(ticket_id):
    from app import mysql

    cur = mysql.connection.cursor()

    # Obtener los detalles del ticket
    cur.execute("""
        SELECT t.*, u.name AS created_by_name, a.name AS assigned_to_name
        FROM tickets t
        JOIN users u ON t.user_id = u.id
        LEFT JOIN users a ON t.assigned_to = a.id
        WHERE t.id = %s
    """, (ticket_id,))
    ticket = cur.fetchone()

    if not ticket:
        cur.close()
        flash(f"Ticket con ID {ticket_id} no encontrado.", "danger")
        return render_template("ticket_detail.html", ticket=None, comments=[], agents=[])

    # Obtener los comentarios del ticket
    cur.execute("""
        SELECT c.id, u.name, c.comment, c.created_at
        FROM ticket_comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.ticket_id = %s
        ORDER BY c.created_at ASC
    """, (ticket_id,))
    comments = cur.fetchall()

    # Obtener todos los agentes para el dropdown
    cur.execute("""
        SELECT id, name
        FROM users
        WHERE role='AGENT'
    """)
    agents = cur.fetchall()

    cur.close()

    return render_template("ticket_detail.html", ticket=ticket, comments=comments, agents=agents)




@bp.route("/tickets/<int:ticket_id>/update", methods=["POST"])
@role_required("USER", "ADMIN", "AGENT")
def ticket_update(ticket_id):
    from app import mysql
    from flask import request, flash, redirect, url_for

    status = request.form.get("status")
    assigned_to = request.form.get("assigned_to")
    
    VALID_STATUSES = ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]
    if status not in VALID_STATUSES:
        flash("Status inválido. No se pudo actualizar el ticket.", "danger")
        return redirect(url_for("routes.ticket_detail", ticket_id=ticket_id))

    assigned_to = int(assigned_to) if assigned_to else None  

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE tickets SET status=%s, assigned_to=%s WHERE id=%s",
        (status, assigned_to, ticket_id)
    )
    mysql.connection.commit()
    cur.close()

    flash("Ticket actualizado correctamente.", "success")
    return redirect(url_for("routes.ticket_detail", ticket_id=ticket_id))




@bp.route("/tickets/<int:ticket_id>/comment", methods=["POST"])
@role_required("USER", "ADMIN", "AGENT")  # todos los roles que puedan comentar
def comment_add(ticket_id):
    from app import mysql

    comment_text = request.form.get("comment")
    user_id = session.get("user_id")

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO ticket_comments (ticket_id, user_id, comment) VALUES (%s, %s, %s)",
        (ticket_id, user_id, comment_text)
    )
    mysql.connection.commit()
    cur.close()

    flash("Comment added successfully", "success")
    return redirect(url_for("routes.ticket_detail", ticket_id=ticket_id))



# ----- Administración de usuarios (solo Admin) -----
@bp.route("/users")
@role_required("ADMIN")
def users_list():
    from app import mysql
    from MySQLdb.cursors import DictCursor

    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT id, name, email, role, created_at
        FROM users
        ORDER BY created_at DESC
    """)
    users = cur.fetchall()
    cur.close()

    return render_template("users_list.html", users=users)


@bp.route("/users/<int:user_id>/role", methods=["POST"])
@login_required
@role_required("ADMIN")
def user_change_role(user_id):
    new_role = request.form.get("role")
    if new_role not in ["ADMIN", "AGENT", "USER"]:
        flash("Rol inválido.", "danger")
        return redirect(url_for("routes.users_list"))

    from app import mysql
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    mysql.connection.commit()
    cur.close()

    flash("Rol actualizado correctamente.", "success")
    return redirect(url_for("routes.users_list"))
