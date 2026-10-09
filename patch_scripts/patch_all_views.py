import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad = r"(\s+)user = User\.objects\.get\(user_id=request\.session\['user_id'\]\)"
good = r"""\1try:
\1    user = User.objects.get(user_id=request.session['user_id'])
\1except User.DoesNotExist:
\1    request.session.flush()
\1    return redirect('login')"""

# Wait, `User.DoesNotExist` requires `from users.models import User`.
# They might not have imported User.DoesNotExist at the top, but `User.DoesNotExist` is accessible from the model class!
# So `except User.DoesNotExist` is perfectly valid as long as `User` is imported. `User` is definitely imported.

new_text = re.sub(bad, good, text)

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(new_text)
