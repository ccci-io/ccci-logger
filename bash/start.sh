#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git-core
sudo apt-get install python3-pip
sudo pip3 install --upgrade setuptools
sudo pip3 install RPi.GPIO
sudo pip3 install gpiozero
sudo pip3 install adafruit-blinka

echo 'enable i2c? (y/n)'
read icc
if [ $icc == 'y' ]
then
    sudo apt-get install -y python-smbus
    sudo apt-get install -y i2c-tools
    sudo raspi-config
fi

echo 'install visual studio code?'
read vsc
if [ $vsc == 'y' ]
then
    curl -L https://raw.githubusercontent.com/headmelted/codebuilds/master/docs/installers/apt.sh | sudo bash
fi
