import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.template import Template, Context

try:
    t = Template('pattern="[0-9]{{{ phone_length }}}"')
    print("Test 1:", t.render(Context({'phone_length': 10})))
except Exception as e:
    print("Test 1 Failed:", e)

try:
    t = Template('pattern="[0-9]{{{{{ phone_length }}}}"')
    print("Test 2:", t.render(Context({'phone_length': 10})))
except Exception as e:
    print("Test 2 Failed:", e)

try:
    t = Template('pattern="[0-9]{{{ phone_length|default:10 }}}"')
    print("Test 3:", t.render(Context({'phone_length': 10})))
except Exception as e:
    print("Test 3 Failed:", e)

try:
    t = Template('pattern="[0-9]{{ "{" }}{{ phone_length|default:10 }}{{ "}" }}"')
    print("Test 4:", t.render(Context({'phone_length': 10})))
except Exception as e:
    print("Test 4 Failed:", e)

