import os
import re

def update_model():
    with open('academics/models.py', 'r', encoding='utf-8') as f:
        content = f.read()

    if 'duration_hrs' not in content:
        content = re.sub(
            r"(duration_months = models\.IntegerField.*?)\n",
            r"\1\n    duration_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, db_column='DurationHrs')\n",
            content
        )
        with open('academics/models.py', 'w', encoding='utf-8') as f:
            f.write(content)

update_model()
print("Added duration_hrs to Course model.")
