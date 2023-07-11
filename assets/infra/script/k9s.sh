#!/bin/bash
set -e

echo "==> Checking version of k9s"
k9s version

echo "==> Updating K9s..."
cd ~
curl -sSL https://github.com/derailed/k9s/releases/download/v0.26.3/k9s_Linux_x86_64.tar.gz -o k9s 
tar -xvf k9s 
chmod 755 k9s
rm LICENSE README.md

echo "==> Moving to new directory"
k9s_dir=$(which k9s)
sudo mv k9s $k9s_dir

echo "==> Updating done!"
k9s version