#!/bin/bash
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest apps/tests/test_models.py apps/tests/test_views.py
