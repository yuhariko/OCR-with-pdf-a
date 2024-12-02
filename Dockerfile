FROM python:3.9-slim

# Đặt môi trường DEBIAN_FRONTEND để tránh tương tác khi cài đặt gói phần mềm
ENV DEBIAN_FRONTEND=noninteractive

# Sao chép file requirements.txt vào thư mục /app trong container
ADD ./requirements.txt /app/requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục /app
ADD . /app

# Chuyển thư mục làm việc vào /app
WORKDIR /app

# Cập nhật gói phần mềm, cài đặt tzdata và các dependencies khác trong một lệnh duy nhất
RUN apt-get update && apt-get install -y tzdata && \
    rm -rf /var/lib/apt/lists/*

# Thiết lập múi giờ
ENV TZ="Asia/Ho_Chi_Minh"

# Cập nhật pip và cài đặt các dependencies Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

