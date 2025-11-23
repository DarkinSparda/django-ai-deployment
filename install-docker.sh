#!/bin/bash
# Docker Installation Script for Ubuntu/Debian
# Run with: bash install-docker.sh

set -e  # Exit on any error

echo "========================================="
echo "Docker Installation Script"
echo "========================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "This script is for Linux only."
    echo "For macOS, download Docker Desktop from: https://www.docker.com/products/docker-desktop"
    echo "For Windows, download Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if already installed
if command -v docker &> /dev/null; then
    echo "Docker is already installed!"
    docker --version
    echo ""
    read -p "Do you want to reinstall? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

echo "Starting Docker installation..."
echo ""

# Update package index
echo "Step 1: Updating package index..."
sudo apt-get update

# Install prerequisites
echo "Step 2: Installing prerequisites..."
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
echo "Step 3: Adding Docker's GPG key..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo "Step 4: Setting up Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index again
echo "Step 5: Updating package index with Docker packages..."
sudo apt-get update

# Install Docker Engine
echo "Step 6: Installing Docker Engine..."
sudo apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

# Add current user to docker group
echo "Step 7: Adding current user to docker group..."
sudo usermod -aG docker $USER

# Start and enable Docker
echo "Step 8: Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

echo ""
echo "========================================="
echo "Docker Installation Complete!"
echo "========================================="
echo ""
docker --version
docker compose version
echo ""
echo "IMPORTANT: You need to log out and log back in for group changes to take effect."
echo "Or run: newgrp docker"
echo ""
echo "Test your installation with:"
echo "  docker run hello-world"
echo ""
