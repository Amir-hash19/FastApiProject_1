#!/bin/sh

alembic upgrade heads


uvicorn core.main:app --reload --host 0.0.0.0 --port 8000