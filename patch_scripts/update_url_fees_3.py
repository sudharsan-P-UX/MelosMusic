with open('website/urls.py', 'r') as f:
    content = f.read()

new_urls = """    path('fees/pending/', views.pending_fees_view, name='pending_fees'),
    path('fees/receipts/', views.receipts_view, name='receipts'),
    path('fees/refunds/', views.refunds_view, name='refunds'),
"""
if "path('fees/pending/'," not in content:
    content = content.replace("path('fees/assign/', views.assign_fees_view, name='assign_fees'),", "path('fees/assign/', views.assign_fees_view, name='assign_fees'),\n" + new_urls)

with open('website/urls.py', 'w') as f:
    f.write(content)
