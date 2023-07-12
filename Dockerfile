# El muchacho de los ojos tristes

# PTYHON ELEMENTS
FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# WORKSPACE
COPY . /gp
WORKDIR /gp

# ENV REQUIREMENTS
RUN apt clean && apt update
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip==22.3.1
RUN pip install setuptools==57.0.0

# APP REQUIREMENTS
RUN pip install --upgrade pip
RUN pip install -r requirements.txt  --no-cache-dir

EXPOSE 80
