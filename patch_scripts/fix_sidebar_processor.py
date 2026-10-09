import re

with open('website/context_processors.py', 'r') as f:
    content = f.read()

old_processor = """        # Build tree
        top_menus = []
        for m in all_menus:
            if not m.parent_menu_id:
                if m.menu_id in access_set:
                    # Check if it has children
                    children = [child for child in all_menus if child.parent_menu_id == m.menu_id and child.menu_id in access_set]
                    m.children = children
                    top_menus.append(m)"""

new_processor = """        # Build tree
        def build_tree(parent_id=None):
            tree = []
            for m in all_menus:
                if m.parent_menu_id == parent_id and m.menu_id in access_set:
                    m.children = build_tree(m.menu_id)
                    tree.append(m)
            return tree

        top_menus = build_tree(None)"""

content = content.replace(old_processor, new_processor)

with open('website/context_processors.py', 'w') as f:
    f.write(content)
