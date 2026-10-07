import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

# I want to remove the wrapper `<div x-show="tab === 'create'" x-transition style="display: none;">`
# and its closing `</div>`.
# Wait, look closely:
#         <!-- 2. Create / Edit Event -->
#         <div x-show="tab === 'create'" x-transition style="display: none;">
#             <!-- Create/Edit Modal -->
#         <div x-show="showCreateModal" ...

old_pattern = r'<!-- 2\. Create / Edit Event -->\s*<div x-show="tab === \'create\'" x-transition style="display: none;">\s*<!-- Create/Edit Modal -->'
new_pattern = '<!-- Create/Edit Modal -->'

content = re.sub(old_pattern, new_pattern, content)

# Now I need to remove the extra closing </div> that belonged to the wrapper.
# Let's find:
#             </form>
#         </div>
#         </div>
# 
#         <!-- 3. Participant Registration -->

old_end_pattern = r'            </form>\s*</div>\s*</div>\s*<!-- 3\. Participant Registration -->'
new_end_pattern = """            </form>
        </div>

        <!-- 3. Participant Registration -->"""

content = re.sub(old_end_pattern, new_end_pattern, content)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
