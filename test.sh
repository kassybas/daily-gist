#!/bin/bash

envsubst < secrets/config.yaml.dist  > secrets/config.yaml
python3 src/reddit_runner.py
