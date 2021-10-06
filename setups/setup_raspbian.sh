#!/bin/bash

# Installation script for Ubuntu 20.04 systems
# simply run ./setup_raspbian.sh

# Install dependencies
sudo apt update
sudo apt -y upgrade
# sudo apt install -y ubuntu-restricted-extras
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y python3-venv
sudo apt install -y libgtk-3-dev
sudo apt-get install -y sox
sudo apt-get install -y libsox-fmt-mp3
sudo apt-get install -y python-wxgtk3.0
sudo apt-get install -y python3-wxgtk4.0 python3-wxgtk-webview4.0 python3-wxgtk-media4.0
sudo apt-get install -y git curl wget libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-2.0-0
# libpng caused a lot of trouble at first, here's a fix... I think...
# wget -O libpng12.deb https://github.com/LiuYuancheng/Power_Generator_Manager/raw/62e4acbefef467c63768c0c7a59e53fa896eccdf/lib/libpng12-0_1.2.54-1ubuntu1b_amd64.deb
# sudo dpkg -i libpng12.deb

# Create virtual env
# mkdir env
# python3 -m venv env/doordog-env
# source env/doordog-env/bin/activate

# Install pip dependencies
sudo pip3 install evdev
pip3 install -r requirements.txt
# pip3 install -U \
#     -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 \
#     wxPython

sudo apt-get install -y dpkg-dev build-essential libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev libnotify-dev freeglut3 freeglut3-dev libwebkitgtk-dev libghc-gtk3-dev libwxgtk3.0-gtk3-dev

sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev

sudo apt install -y libjpeg-dev libtiff5-dev libnotify-dev libgtk2.0-dev libgtk-3-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev libwebkitgtk-dev freeglut3 freeglut3-dev