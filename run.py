#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# run.py

import os
from nasefirmy import app

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
