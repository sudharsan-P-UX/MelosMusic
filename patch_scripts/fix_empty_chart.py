with open('templates/website/enrollment_management.html', 'r', encoding='utf-8') as f:
    text = f.read()

bad_js = """                if (courseLabels.length === 0) {
                    courseLabels.push("No Data");
                    courseData.push(1);
                }"""

good_js = """                let sum = courseData.reduce((a, b) => a + b, 0);
                if (courseLabels.length === 0 || sum === 0) {
                    courseLabels.push("No Enrollments yet");
                    courseData.push(1);
                }"""

text = text.replace(bad_js, good_js)

with open('templates/website/enrollment_management.html', 'w', encoding='utf-8') as f:
    f.write(text)
