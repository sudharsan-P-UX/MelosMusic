import re

with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

# Replace Course Modal
old_course_modal_start = '<!-- Add Course Modal -->\n    <div x-show="showCourseModal" style="display: none;" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">\n        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">\n            <div x-show="showCourseModal" @click="showCourseModal = false" x-transition.opacity class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>\n            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>\n            <div x-show="showCourseModal" x-transition class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl w-full flex flex-col max-h-[90vh]">'
new_course_modal_start = '<!-- Add Course Modal -->\n    <div x-show="showCourseModal" style="display: none;" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">\n        <div @click.away="showCourseModal = false" class="bg-white rounded-lg text-left overflow-hidden shadow-xl w-full max-w-2xl flex flex-col max-h-[90vh]">'

content = content.replace(old_course_modal_start, new_course_modal_start)
content = content.replace('</form>\n            </div>\n        </div>\n    </div>\n\n    <!-- Add Batch Modal -->', '</form>\n        </div>\n    </div>\n\n    <!-- Add Batch Modal -->')

# Replace Batch Modal
old_batch_modal_start = '<!-- Add Batch Modal -->\n    <div x-show="showBatchModal" style="display: none;" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">\n        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">\n            <div x-show="showBatchModal" @click="showBatchModal = false" x-transition.opacity class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>\n            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>\n            <div x-show="showBatchModal" x-transition class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl w-full flex flex-col max-h-[90vh]">'
new_batch_modal_start = '<!-- Add Batch Modal -->\n    <div x-show="showBatchModal" style="display: none;" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">\n        <div @click.away="showBatchModal = false" class="bg-white rounded-lg text-left overflow-hidden shadow-xl w-full max-w-2xl flex flex-col max-h-[90vh]">'

content = content.replace(old_batch_modal_start, new_batch_modal_start)
content = content.replace('</form>\n            </div>\n        </div>\n    </div>\n</div>', '</form>\n        </div>\n    </div>\n</div>')

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
