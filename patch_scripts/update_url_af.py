with open('website/urls.py', 'r') as f:
    content = f.read()

if "path('fees/assign/'," not in content:
    content = content.replace("path('fees/collection/', views.fee_collection_view, name='fee_collection'),", "path('fees/assign/', views.assign_fees_view, name='assign_fees'),\n    path('fees/collection/', views.fee_collection_view, name='fee_collection'),")

with open('website/urls.py', 'w') as f:
    f.write(content)
