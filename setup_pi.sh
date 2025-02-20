#!/bin/bash

# Make script exit on error
set -e

echo "Setting up Discord Bot on Raspberry Pi..."

# Update system
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install Python and Git if not already installed
echo "Installing Python and Git..."
sudo apt install -y python3-pip git

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Setup systemd service
echo "Setting up systemd service..."
sudo cp discord_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable discord_bot
sudo systemctl start discord_bot

# Configure Git for auto-updates
echo "Configuring Git..."
if [ -z "$(git config --global user.email)" ]; then
    echo "Setting up Git user email..."
    git config --global user.email "discord.bot@raspberry.pi"
fi
if [ -z "$(git config --global user.name)" ]; then
    echo "Setting up Git user name..."
    git config --global user.name "Discord Bot"
fi
git config --global credential.helper store

echo "Setup complete! The bot should now be running."
echo "To check status: sudo systemctl status discord_bot"
echo "To view logs: journalctl -u discord_bot"