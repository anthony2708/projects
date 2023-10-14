# Xây dựng image mới từ image ubuntu:latest
FROM ubuntu:latest

# Cập nhật apt và cài đặt git
RUN apt-get update && apt-get install -y git
# Cài đặt python3
RUN apt-get install -y python3
# Thiết lập thành thư mục /home/github
WORKDIR /home/github
# Clone repo từ github
RUN git clone https://github.com/anthony2708/projects.git
# Thay đổi thư mục
WORKDIR /home/github/projects/CN02_Socket/src/app
