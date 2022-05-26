#!/bin/sh

cd notebooks
export PYTHONPATH="${PYTHONPATH}:/app"
nohup cron.sh & jupyter notebook --allow-root --port=8888 --no-browser --ip=0.0.0.0