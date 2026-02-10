gunicorn --bind 0.0.0.0:10000 --timeout 120 --workers 1 rainfall_prediction:app
