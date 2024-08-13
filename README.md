# ASV - Simulation

Author: Naveen Anil

To simulate the ASV using Ardupilot plugin and QGround Control

## Software Dependencies
```
Ubuntu 20.04
ROS Noetic
Gazebo 11
```
## Installing Ardupilot and MAVProxy

In home directory:
```
cd ~
git clone https://github.com/ArduPilot/ardupilot.git

```
## Install dependencies:
```
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
```
Reload profile:
```
. ~/.profile
```

## Checkout Latest Copter Build
```
git checkout Copter-4.2
git submodule update --init --recursive
```
## Use pip (Python package installer) to install mavproxy:
```
sudo pip install future pymavlink MAVProxy
```
Open `~/.bashrc` for editing:
```
gedit ~/.bashrc
```

Add these lines to end of `~/.bashrc` (open file in the text editor):
```
export PATH=$PATH:$HOME/ardupilot/Tools/autotest
export PATH=/usr/lib/ccache:$PATH
```

Save and close the text editor.

Reload `~/.bashrc`:
```
. ~/.bashrc
```
Run SITL (Software In The Loop) once to set params:
```
sim_vehicle.py -v APMrover2
```
## Installing Gazebo and Ardupilot Plugin

### Install Gazebo

Setup your computer to accept software from http://packages.osrfoundation.org:
```
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
```

Setup keys:
```
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
```

Reload software list:
```
sudo apt update
```
Install Gazebo:
```
sudo apt-get install gazebo11 libgazebo11-dev
```
### Install Gazebo plugin for APM (ArduPilot Master)
```
cd ~
git clone https://github.com/khancyr/ardupilot_gazebo.git
cd ardupilot_gazebo
git checkout dev
mkdir build
cd build
cmake ..
make -j4
sudo make install
```
Set path for Gazebo and ardupilot plugins for Gazebo:
```
echo 'source /usr/share/gazebo/setup.sh' >> ~/.bashrc
```
## Installing MAVlink and MAVROS

At this point **ROS Noetic** should be completely installed

To make use of `catkin build` instead of `catkin_make` install the following:
```
sudo apt-get install python-wstool python-rosinstall-generator python-catkin-tools
```

Install `mavros` and `mavlink` from source
```
cd ~/catkin_ws
wstool init ~/catkin_ws/src

rosinstall_generator --upstream mavros | tee /tmp/mavros.rosinstall
rosinstall_generator mavlink | tee -a /tmp/mavros.rosinstall
wstool merge -t src /tmp/mavros.rosinstall
wstool update -t src
rosdep install --from-paths src --ignore-src --rosdistro `echo $ROS_DISTRO` -y

catkin build
```
Add a line to end of `~/.bashrc` by running the following command:
```
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```

Update global variables
```
source ~/.bashrc
```
## Install *sitl_gazebo* plugin dependencies
 
 Install the 
 dependencies:

 ```bash
sudo apt-get install libprotobuf-dev
sudo apt-get install libprotoc-dev sudo apt-get install protobuf-compiler 
sudo apt-get install libeigen3-dev sudo apt-get install libxml2-utils sudo apt-get install python-rospkg sudo apt-get install python-jinja2
sudo apt-get install libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly -y
```
Build *sitl_gazebo*

Clone the repository:
```bash
mkdir -p ~/src
cd src
git clone --recursive https://github.com/PX4/sitl_gazebo.git
```
Navigate into the build directory and invoke CMake from it:

```bash
cd ~/src/sitl_gazebo
mkdir build
cd build
cmake ..
```
Now build the gazebo plugins by typing:

```bash
make -j$(nproc) -l$(nproc)
```
Next add the location of this build directory to your gazebo plugin path,
```bash
export GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH}:$HOME/src/sitl_gazebo/build
```

You also need to add the the root location of this repository, e.g. add the following line to your `.bashrc` (Linux)
```bash
export SITL_GAZEBO_PATH=$HOME/src/sitl_gazebo
sudo make install
```

## Setup boat package

```
cd ~/catkin_ws/src
git clone https://github.com/nvnanil/asv_simulation.git
cd iq_gnc
git checkout main
catkin build
```

### Add custom location to ardurover sitl

```
cd ~/catkin_ws/src/iq_sim/scripts/
./boatSetup.sh
```

### Run ASV simulation
First terminal 
```
roslaunch iq_sim boat.launch
```
Second terminal
```
sim_vehicle.py -v APMrover2 -f gazebo-rover  -m --mav10 --console -L Viridian
```
Establsh connection between the computer and ArduRover using
```
rosrun iq_gnc apm.launch
```
