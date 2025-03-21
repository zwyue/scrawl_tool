# Use an official Python runtime as a parent image
FROM python:3.13.2

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip3 install --upgrade pip

# Install any Python dependencies specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# 设置环境变量TZ
ENV TZ=Asia/Shanghai

# 配置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV ENV_FILE=.env.prod

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && apt-get clean

# Install Google Chrome
#RUN wget -q -O chrome.deb https://dl.google.com/linux/deb/pool/main/g/google-chrome-stable/google-chrome-stable_134.0.6998.88-1_amd64.deb && \
#    apt-get install -y ./chrome.deb && \
#    rm chrome.deb
RUN apt-get install -y ./doc/google-chrome-stable_134.0.6998.88-1_amd64.deb

## Install ChromeDriver
#RUN wget -q -O chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.88/linux64/chromedriver-linux64.zip && \
#    unzip chromedriver.zip && \
#    mv chromedriver-linux64 /usr/local/bin/ && \
#    rm chromedriver.zip
RUN unzip ./doc/chromedriver-linux64.zip -d /usr/local/bin/

## RUN pkill -9 chrome || true

# Make the Python script executable
CMD ["python", "task.py"]
