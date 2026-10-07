import re

with open('core/settings.py', 'r') as f:
    content = f.read()

# Add dotenv loading
dotenv_code = """import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))"""

# Replace the existing BASE_DIR logic
old_base_dir = """import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent"""

if 'load_dotenv' not in content and old_base_dir in content:
    content = content.replace(old_base_dir, dotenv_code)
elif 'load_dotenv' not in content:
    # If the old_base_dir was slightly different
    content = "from dotenv import load_dotenv\nimport os\nload_dotenv()\n" + content

with open('core/settings.py', 'w') as f:
    f.write(content)
