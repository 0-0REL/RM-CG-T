FROM python:3.12-slim

# Instalar dependencias del sistema para OpenCV con GUI
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libgtk2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements e instalar Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigos necesarios
COPY src/ .
COPY dev/robot/sim/simMyCobot.py .

CMD ["/bin/bash"]