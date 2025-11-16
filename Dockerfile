# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala las dependencias del sistema necesarias para compilar paquetes Python
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requisitos e instala las dependencias
COPY requirements.txt .
RUN pip install -a_no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

