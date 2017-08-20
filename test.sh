#!/bin/bash

envsubst < config.yaml.dist  > config.yaml
python3 reddit_runner.py
