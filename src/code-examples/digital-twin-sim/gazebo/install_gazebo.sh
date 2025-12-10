#!/bin/bash

# This script installs Gazebo Garden and the ROS 2 Gazebo bridge.
# It assumes an Ubuntu 22.04 LTS environment.

# 1. Add Gazebo repository
echo "Adding Gazebo repository..."
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

# 2. Update and install Gazebo Garden
echo "Updating apt packages and installing Gazebo Garden..."
sudo apt update
sudo apt install -y gazebo-garden

# Verify Gazebo installation
echo "Verifying Gazebo installation..."
gazebo --version

# 3. Install gazebo_ros Bridge (for Humble or Iron)
echo "Installing gazebo_ros bridge..."
# Determine ROS 2 distribution (assuming Humble or Iron)
ROS2_DISTRO=$(ros2 --version | grep 'ROS_DISTRO' | cut -d'=' -f2 | xargs)

if [ -z "$ROS2_DISTRO" ]; then
    echo "Warning: Could not determine ROS 2 distribution. Please ensure ROS 2 is installed and sourced."
    echo "Attempting to install for 'humble' as a default. If this is incorrect, please install manually."
    ROS2_DISTRO="humble"
fi

sudo apt install -y ros-"$ROS2_DISTRO"-gazebo-ros

echo "Gazebo and gazebo_ros bridge installation complete."
echo "Please ensure your ROS 2 environment is sourced (e.g., source /opt/ros/$ROS2_DISTRO/setup.bash) before running ROS 2 commands with Gazebo."
