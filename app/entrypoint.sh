#!/bin/bash

uvicorn main:app --reload --proxy-headers --host 0.0.0.0 --port ${PORT}