#!/usr/bin/env python3
"""
Example file with messy imports to demonstrate isort
"""
from os import path
import sys
from flask import Flask, request
import asyncio
from typing import Dict, List
import requests
from collections import defaultdict
import json

# This file has imports in random order
# isort will organize them into groups:
# 1. Standard library imports
# 2. Third-party imports 
# 3. Local imports

def example_function():
    return "This demonstrates import organization"
