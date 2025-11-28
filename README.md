# Gestión de Productos Backend

Este proyecto es un backend para la gestión de productos, construido con FastAPI y SQLAlchemy. Incluye autenticación de usuarios (vendedores), gestión de productos (creación, lectura, actualización, eliminación) y utiliza la API de Gemini para generar descripciones de marketing y Pollinations.ai para generar imágenes de productos.

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para construir APIs con Python.
- **SQLAlchemy**: ORM (Object Relational Mapper) para interactuar con la base de datos.
- **PostgreSQL**: Base de datos relacional utilizada para almacenar la información de vendedores y productos.
- **Passlib[bcrypt]**: Para el hashing seguro de contraseñas.
- **Python-jose[cryptography]**: Para la implementación de JSON Web Tokens (JWT) para la autenticación.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI.
- **python-dotenv**: Para la gestión de variables de entorno.
- **Gemini API**: Para la generación de descripciones de marketing de productos.
- **Pollinations.ai**: Para la generación de URLs de imágenes de productos basadas en descripciones.
- **CORS Middleware**: Para manejar las políticas de Cross-Origin Resource Sharing.

## Despliegue en Render

Este proyecto está diseñado para ser desplegado en Render, utilizando su servicio de PostgreSQL para la base de datos.

### Configuración de la Base de Datos en Render

1.  **Crear una instancia de PostgreSQL en Render**: En tu panel de control de Render, crea un nuevo servicio de PostgreSQL. Anota la `External Database URL` que te proporciona Render.
2.  **Configurar la variable de entorno `DATABASE_URL`**: Esta URL debe ser añadida a las variables de entorno de tu servicio de Render para el backend. El formato es `postgresql://user:password@host:port/database_name`.

### Despliegue del Backend en Render

1.  **Conectar tu repositorio de GitHub**: En Render, crea un nuevo servicio web y conéctalo a tu repositorio de GitHub donde se encuentra este proyecto.
2.  **Configuración de Build y Start Command**: Render detectará automáticamente el `Dockerfile`.
    *   **Build Command**: `pip install -r requirements.txt` (Esto se maneja dentro del Dockerfile, pero Render podría requerirlo explícitamente si no usas Docker)
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000` (Asegúrate de que el puerto coincida con el `EXPOSE` en tu Dockerfile y el puerto que Render asigna, que suele ser `10000` para servicios web).
3.  **Variables de Entorno**: Asegúrate de configurar las siguientes variables de entorno en Render:
    *   `SECRET_KEY`: Una clave secreta fuerte para la firma de JWT.
    *   `GEMINI_API_KEY`: Tu clave de API para acceder a la API de Gemini.
    *   `DATABASE_URL`: La URL de conexión a tu base de datos PostgreSQL en Render.
    *   `FRONTEND_URL`: La URL de tu aplicación frontend (por ejemplo, `https://proyectback.netlify.app`).

## Configuración Local

Para ejecutar el proyecto localmente, sigue estos pasos:

1.  **Clonar el repositorio**:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd ParcialBack
    ```

2.  **Crear un entorno virtual** (recomendado):
    ```bash
    python -m venv venv
    .env\Scripts\activate  # En Windows
    # source venv/bin/activate  # En macOS/Linux
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno**: Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
    ```
    SECRET_KEY="tu_clave_secreta_aqui"
    GEMINI_API_KEY="tu_clave_gemini_aqui"
    DATABASE_URL="postgresql://user:password@host:port/database_name" # O una base de datos local como SQLite para desarrollo
    FRONTEND_URL="http://localhost:8000" # O la URL de tu frontend local
    ```
    *   Para `DATABASE_URL` en desarrollo local, puedes usar una base de datos PostgreSQL local o incluso SQLite para simplificar (aunque el proyecto está configurado para PostgreSQL). Si usas SQLite, la URL sería `sqlite:///./sql_app.db`.

5.  **Ejecutar la aplicación**:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    La API estará disponible en `http://localhost:8000`.

## Endpoints de la API

La API expone los siguientes endpoints:

-   **`/register` (POST)**: Registra un nuevo vendedor.
    -   **Request Body**: `VendedorCreate` (email, password)
    -   **Response**: `Vendedor` (id, email)

-   **`/token` (POST)**: Obtiene un token de acceso JWT para un vendedor.
    -   **Request Body**: `OAuth2PasswordRequestForm` (username, password)
    -   **Response**: `Token` (access_token, token_type)

-   **`/productos/` (GET)**: Obtiene una lista de todos los productos.
    -   **Headers**: `Authorization: Bearer <access_token>`
    -   **Response**: `list[Producto]`

-   **`/productos/` (POST)**: Crea un nuevo producto. La descripción de marketing y la URL de la imagen se generan automáticamente usando Gemini y Pollinations.ai.
    -   **Headers**: `Authorization: Bearer <access_token>`
    -   **Request Body**: `ProductoCreate` (nombre, precio)
    -   **Response**: `Producto` (id, nombre, precio, descripcion_marketing, imagen_url, vendedor_email)

-   **`/productos/{producto_id}` (PUT)**: Actualiza un producto existente.
    -   **Headers**: `Authorization: Bearer <access_token>`
    -   **Request Body**: `ProductoUpdate` (nombre, precio - opcional)
    -   **Response**: `Producto`

-   **`/productos/{producto_id}` (DELETE)**: Elimina un producto existente.
    -   **Headers**: `Authorization: Bearer <access_token>`
    -   **Response**: `{"message": "Producto eliminado exitosamente"}`

## Frontend

El frontend de este proyecto se encuentra en el directorio `frontend/` y se espera que interactúe con esta API backend. Asegúrate de configurar la `FRONTEND_URL` en tus variables de entorno para permitir las solicitudes CORS desde tu frontend.

## Variables de Entorno

Las siguientes variables de entorno son necesarias para el correcto funcionamiento de la aplicación:

-   `SECRET_KEY`: Clave secreta utilizada para firmar los tokens JWT. **¡Importante: usa una clave fuerte y mantenla segura!**
-   `GEMINI_API_KEY`: Tu clave de API para acceder a los servicios de Gemini.
-   `DATABASE_URL`: La URL de conexión a tu base de datos PostgreSQL. Ejemplo: `postgresql://user:password@host:port/database_name`.
-   `FRONTEND_URL`: La URL de tu aplicación frontend, necesaria para la configuración de CORS.