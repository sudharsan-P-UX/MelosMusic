with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

bad = """                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Total Sessions</label>
                                <input type="number" name="total_sessions" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Course Fee (₹) <span class="text-red-500">*</span></label>"""

good = """                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Total Sessions</label>
                                <input type="number" name="total_sessions" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Days</label>
                                <input type="text" name="days" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm" placeholder="e.g. Mon, Wed">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Course Fee (₹) <span class="text-red-500">*</span></label>"""

content = content.replace(bad, good)

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
