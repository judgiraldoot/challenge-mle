FROM python:3.10

# Define el directorio de trabajo
WORKDIR /app

# Copia todo el contenido de la carpeta "challenge" al directorio de trabajo en el contenedor
COPY ./challenge /app/challenge

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt /app/requirements.txt

# Elimina el archivo exploration.ipynb y los archivos .pyc (archivos compilados de Python)
RUN rm -f /app/challenge/exploration.ipynb && \
    find /app/challenge -name '*.pyc' -delete

# Instala las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expone el puerto 8080 para que sea accesible desde fuera del contenedor
EXPOSE 8080

# Establece la variable de entorno PYTHONPATH al directorio de trabajo
ENV PYTHONPATH="/app"

# Define el comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
