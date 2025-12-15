
# Manual de Usuario - Help Desk Web App

##  Introducción
Este manual explica cómo utilizar la aplicación web de Help Desk para gestionar tickets de soporte. Está dirigido a usuarios finales con roles **Admin**, **Agent** y **User**.

---

##  Inicio de sesión
1. Accede a la URL del sistema: `http://localhost:5000`.
2. Ingresa tu **correo electrónico** y **contraseña** en el formulario de login.
3. Haz clic en **Login**.
4. Si las credenciales son correctas, serás redirigido al **Dashboard**.

---

##  Dashboard
- Muestra un resumen de los tickets por estado (OPEN, IN_PROGRESS, RESOLVED, CLOSED).
- Desde el menú superior puedes acceder a:
  - **Tickets** (listado y creación).
  - **Usuarios** (solo si eres Admin).

  -Admin puede ver todos los tickets y la lista de usuarios.

---

##  Gestión de Tickets
### Crear un nuevo ticket
1. Haz clic en **Tickets** → **New Ticket**.
2. Completa:
   - **Título**
   - **Descripción**
   - **Prioridad** (LOW, MEDIUM, HIGH)
3. Haz clic en **Create**.
4. El ticket tendra estado inicial de OPEN.
   - Los tickets tienen que ser asignados a un agente por un Admin o un Agent.


### Ver listado de tickets
- Accede a **Tickets**.
- Verás una tabla con:
  - ID, Título, Estado, Prioridad, Created by, Asigned to, Created at.
- Created by muestra el nombre del usuario que creo el ticket.
- Assigned to muestra el nombre del agente asignado o si aun no esta asignado.


### Ver detalle de un ticket
- Haz clic en el ID del ticket.
- Podrás:
  - Ver información completa del ticket.
  - Añadir comentarios.
  - Si eres **Admin** o **Agent**, podras cambiar estado y asignar agente desde el dropdown.
    -Solo los usuarios con rol **Agent** apareceran como opciones en el dropdown.


### Actualizar ticket
- Roles **Admin** o **Agent** pueden cambiar el Status y asignar a un agente disponible desde el dropdown de Assigned to.
- Haz clic en **Update** para guardar los cambios.
- Aparecera un mensaje de confirmacion: "Ticket actualizado correctamente".


---

##  Comentarios en tickets
- En la vista de detalle, escribe tu comentario en el formulario y haz clic en **Add Comment**.
- El comentario aparecerá en la parte de arriba.
- Cualquier usuario con accceso al ticket puede agregar comentarios.

---

##  Administración de Usuarios (solo Admin)
- Accede a **Users** desde el menú.
- Verás la lista de usuarios con ID, Nombre, Email, Rol.
- Puedes cambiar el rol seleccionando uno nuevo y haciendo clic en **Save**.


---

##  Capturas
Las capturas se encuentran en `docs/screenshots/`
- login.png
- dashboard.png
- tickets_list.png
- ticket_detail.png
- users_list.png