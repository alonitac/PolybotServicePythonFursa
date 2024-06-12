#!/bin/bash

git checkout dev
git pull dev
sudo systemctl daemon-reload
sudo systemctl restart tel.service
