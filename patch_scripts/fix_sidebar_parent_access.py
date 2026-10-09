import re

with open('website/context_processors.py', 'r') as f:
    content = f.read()

old_processor = """        # Build tree
        def build_tree(parent_id=None):
            tree = []
            for m in all_menus:
                if m.parent_menu_id == parent_id and m.menu_id in access_set:
                    m.children = build_tree(m.menu_id)
                    tree.append(m)
            return tree

        top_menus = build_tree(None)"""

new_processor = """        # Build tree
        def build_tree(parent_id=None):
            tree = []
            for m in all_menus:
                if m.parent_menu_id == parent_id:
                    # Recursively build children first
                    children = build_tree(m.menu_id)
                    # Include this menu if it's explicitly accessible, or if it has accessible children
                    if m.menu_id in access_set or len(children) > 0:
                        m.children = children
                        tree.append(m)
            return tree

        top_menus = build_tree(None)"""

content = content.replace(old_processor, new_processor)

with open('website/context_processors.py', 'w') as f:
    f.write(content)
