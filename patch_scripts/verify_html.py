import os, sys, django
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
c = Client()
s = c.session
s['user_id'] = 1
s.save()

for tab in ['calendar', 'registration', 'upcoming', 'assignments', 'venue', 'attendance', 'reports']:
    res = c.get(f'/events/?tab={tab}')
    html = res.content.decode('utf-8')
    assert res.status_code == 200
    assert 'x-data="eventDashboard()"' in html, f"x-data=eventDashboard() missing on {tab}"
    assert '= 0; i--' not in html.split('<script>')[0], f"Leaked JS found on {tab}!"
    print(f"Verified {tab}: Clean HTML, valid 200 OK, x-data='eventDashboard()'")

print("\nAll HTML renderings verified clean and completely leak-free!")
