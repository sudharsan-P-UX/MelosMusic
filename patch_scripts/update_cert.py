with open('templates/website/teachers.html', 'r') as f:
    content = f.read()

certification_html = """
                <!-- Certification Section -->
                <div class="border border-gray-200 rounded-md p-4 bg-gray-50">
                    <div class="flex justify-between items-center mb-3">
                        <h4 class="text-sm font-bold text-gray-800">Certification</h4>
                        <button type="button" onclick="addCertificationRow()" class="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded hover:bg-indigo-200 font-bold transition">
                            <i class="fa-solid fa-plus mr-1"></i> Add More
                        </button>
                    </div>
                    <div id="certificationContainer" class="space-y-3">
                        <div class="certification-row grid grid-cols-12 gap-2 items-end">
                            <div class="col-span-5">
                                <label class="block text-xs font-medium text-gray-600 mb-1">Certificate Name</label>
                                <input type="text" name="cert_name[]" class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm outline-none focus:ring-1 focus:ring-indigo-500">
                            </div>
                            <div class="col-span-2">
                                <label class="block text-xs font-medium text-gray-600 mb-1">Year</label>
                                <input type="number" name="cert_year[]" class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm outline-none focus:ring-1 focus:ring-indigo-500">
                            </div>
                            <div class="col-span-5 relative flex items-center">
                                <div class="flex-1">
                                    <label class="block text-xs font-medium text-gray-600 mb-1">Document</label>
                                    <input type="file" name="cert_document[]" class="w-full border border-gray-300 rounded px-2 py-1 text-sm outline-none bg-white">
                                </div>
                                <button type="button" onclick="this.parentElement.parentElement.remove()" class="ml-2 text-red-500 hover:text-red-700 pb-1 mt-5">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
"""

content = content.replace('<!-- Experience Section -->', certification_html + '\n                <!-- Experience Section -->')

js_html = """
    // Certification Dynamic Rows
    function addCertificationRow() {
        const container = document.getElementById('certificationContainer');
        const rowHTML = `
            <div class="certification-row grid grid-cols-12 gap-2 items-end mt-2">
                <div class="col-span-5">
                    <input type="text" name="cert_name[]" placeholder="Certificate Name" class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm outline-none focus:ring-1 focus:ring-indigo-500">
                </div>
                <div class="col-span-2">
                    <input type="number" name="cert_year[]" placeholder="Year" class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm outline-none focus:ring-1 focus:ring-indigo-500">
                </div>
                <div class="col-span-5 relative flex items-center">
                    <div class="flex-1">
                        <input type="file" name="cert_document[]" class="w-full border border-gray-300 rounded px-2 py-1 text-sm outline-none bg-white">
                    </div>
                    <button type="button" onclick="this.parentElement.parentElement.remove()" class="ml-2 text-red-500 hover:text-red-700 pb-1">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </div>
            </div>`;
        container.insertAdjacentHTML('beforeend', rowHTML);
    }
"""

content = content.replace('// Experience Dynamic Rows', js_html + '\n    // Experience Dynamic Rows')

content = content.replace("document.getElementById('experienceContainer').innerHTML = '';", "document.getElementById('experienceContainer').innerHTML = '';\n        document.getElementById('certificationContainer').innerHTML = '';")
content = content.replace("addExperienceRow();", "addExperienceRow();\n        addCertificationRow();")

with open('templates/website/teachers.html', 'w') as f:
    f.write(content)
