#!/bin/bash

envsubst < config.yaml.dist  > config.yaml
python3 src/reddit_runner.py
