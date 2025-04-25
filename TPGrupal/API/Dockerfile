FROM python:3.12-slim

# Instalar pipenv
RUN pip install pipenv

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos Pipfile y Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Instalar las dependencias del Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Verificar la instalación de Flask
RUN pipenv run pip list

# Copiar el contenido del proyecto
COPY . .


# Exponer el puerto en el que correrá la aplicación
EXPOSE 5000

# Definir el comando por defecto
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]