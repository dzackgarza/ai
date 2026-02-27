#!/bin/bash
# Create 10G swap file

# 1. Create a 10G swap file
sudo fallocate -l 10G /swapfile

# 2. Set secure permissions (root only)
sudo chmod 600 /swapfile

# 3. Format the file as swap
sudo mkswap /swapfile

# 4. Enable the swap file
sudo swapon /swapfile

# 5. Make it permanent (add to fstab)
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 6. Verify swap is active
sudo swapon --show
free -h
