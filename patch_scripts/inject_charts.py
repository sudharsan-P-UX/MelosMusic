import re

with open('templates/website/enrollment_management.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Chart.js script before closing head or body
if '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>' not in html:
    html = html.replace('</head>', '    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n</head>')
    
# Replace the widgets grid
old_widgets = re.search(r'(<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">.*?)<!-- Data Table -->', html, re.DOTALL)

if old_widgets:
    new_widgets = """<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <!-- Widget 1: Pie Chart -->
            <div class="border border-gray-200 rounded p-4 bg-white shadow-sm flex flex-col justify-between">
                <h4 class="font-medium text-gray-800 mb-2 text-sm">Enrollments by Course</h4>
                <div class="flex-1 relative w-full flex items-center justify-center">
                    <canvas id="coursePieChart" style="max-height: 160px;"></canvas>
                </div>
            </div>
            
            <!-- Widget 2: Bar Chart -->
            <div class="border border-gray-200 rounded p-4 bg-white shadow-sm flex flex-col justify-between">
                <h4 class="font-medium text-gray-800 mb-2 text-sm">Student Status</h4>
                <div class="flex-1 relative w-full flex items-center justify-center">
                    <canvas id="statusBarChart" style="max-height: 160px;"></canvas>
                </div>
            </div>
            
            <!-- Widget 3: Horizontal Bar Chart -->
            <div class="border border-gray-200 rounded p-4 bg-white shadow-sm flex flex-col justify-between">
                <h4 class="font-medium text-gray-800 mb-2 text-sm">Batch Capacity vs Enrolled</h4>
                <div class="flex-1 relative w-full flex items-center justify-center">
                    <canvas id="batchBarChart" style="max-height: 160px;"></canvas>
                </div>
            </div>
        </div>

        <!-- Initialize Charts -->
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Pie Chart
                const courseLabels = [
                    {% for c in course_stats %}"{{ c.course_name|escapejs }}",{% endfor %}
                ];
                const courseData = [
                    {% for c in course_stats %}{{ c.enroll_count }},{% endfor %}
                ];
                
                if (courseLabels.length === 0) {
                    courseLabels.push("No Data");
                    courseData.push(1);
                }

                new Chart(document.getElementById('coursePieChart'), {
                    type: 'pie',
                    data: {
                        labels: courseLabels,
                        datasets: [{
                            data: courseData,
                            backgroundColor: ['#4caf50', '#ff9800', '#f44336', '#2196f3', '#9c27b0']
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { boxWidth: 12, font: {size: 10} } } } }
                });

                // Bar Chart (Student Status)
                new Chart(document.getElementById('statusBarChart'), {
                    type: 'bar',
                    data: {
                        labels: ['Active', 'Inactive'],
                        datasets: [{
                            label: 'Students',
                            data: [{{ active_students|default:"0" }}, {{ inactive_students|default:"0" }}],
                            backgroundColor: ['#81c784', '#e57373']
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { stepSize: 1, font: {size: 10} } }, x: { ticks: { font: {size: 10} } } } }
                });

                // Horizontal Bar Chart (Batch Capacity)
                const batchLabels = [
                    {% for b in batch_stats %}"{{ b.batch_name|escapejs }}",{% endfor %}
                ];
                const batchEnrolled = [
                    {% for b in batch_stats %}{{ b.enroll_count }},{% endfor %}
                ];
                const batchCapacity = [
                    {% for b in batch_stats %}{{ b.capacity|default:"0" }},{% endfor %}
                ];
                
                if (batchLabels.length === 0) {
                    batchLabels.push("No Data");
                    batchEnrolled.push(0);
                    batchCapacity.push(10);
                }

                new Chart(document.getElementById('batchBarChart'), {
                    type: 'bar',
                    data: {
                        labels: batchLabels,
                        datasets: [
                            {
                                label: 'Enrolled',
                                data: batchEnrolled,
                                backgroundColor: '#42a5f5'
                            },
                            {
                                label: 'Total Capacity',
                                data: batchCapacity,
                                backgroundColor: '#e0e0e0'
                            }
                        ]
                    },
                    options: { 
                        indexAxis: 'y', 
                        responsive: true, 
                        maintainAspectRatio: false, 
                        plugins: { legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: {size: 10} } } },
                        scales: { x: { beginAtZero: true, ticks: { font: {size: 10} } }, y: { ticks: { font: {size: 10} } } }
                    }
                });
            });
        </script>
        
        <!-- Data Table -->"""
    html = html.replace(old_widgets.group(0), new_widgets)

with open('templates/website/enrollment_management.html', 'w', encoding='utf-8') as f:
    f.write(html)
