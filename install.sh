# How to use
# sudo bash install.sh

echo "Downloading Pip!"
sudo apt-get install python3-pip -y
echo "Downloading Wifi Module!"
sudo pip3 install wifi
echo "Downloading Netifaces"
sudo apt-get install python3-setuptools -y
wget "https://pypi.python.org/packages/source/n/netifaces/netifaces-0.10.4.tar.gz#md5=36da76e2cfadd24cc7510c2c0012eb1e"
tar -xvzf netifaces-0.10.4.tar.gz
cd netifaces-0.10.4
python3 setup.py install
echo -"Netifaces installed"
echo  "Installing essentials"
sudo apt-get install build-essential python3-dev libqt4-dev qt4-dev-tools python3-pyqt4 -y
echo "Cleaning up"
cd ..
rm -R netifaces-0.10.4
echo "Done!"




