import re

with open('core/settings.py', 'r') as f:
    content = f.read()

# Replace CompressedManifestStaticFilesStorage with CompressedStaticFilesStorage
content = content.replace(
    "'whitenoise.storage.CompressedManifestStaticFilesStorage'", 
    "'whitenoise.storage.CompressedStaticFilesStorage'"
)

with open('core/settings.py', 'w') as f:
    f.write(content)
