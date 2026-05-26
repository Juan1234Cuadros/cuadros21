#!/bin/bash

echo "Iniciando el despliegue automatico de Don Alberto"

# Moverse a la carpeta
cd /home/cuadros21/moto-api

# Traer los cambios desde git
echo "Trayendo la ultima version desde git"
git pull origin master

# Activar el entorno virtual
echo "Asegurando las dependencias"
source venv/bin/activate
pip install -r requirements.txt --quiet

# Reiniciar el servicio de systemd
echo "Reiniciando el motor gunicorn"
sudo systemctl restart gigamoto.service

# Verificar que este vivo
echo "Despliegue completado con exito. El estado actual es:"
sudo systemctl status gigamoto.service | grep "Active:"es

