#!/usr/bin/env python3
"""
Run script for the ECLI Metadata Dashboard.
"""

import os
import sys
from dashboard import app

if __name__ == '__main__':
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
