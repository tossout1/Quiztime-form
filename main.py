from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Serve the HTML form creation page
@app.route('/')
def index():
    return render_template_string(open("index.html").read())

# Route to save the form as an HTML file
@app.route('/save-form', methods=['POST'])
def save_form():
    data = request.get_json()

    # Extract form data
    email = data['email']
    form_title = data['formTitle']
    form_caption = data['formCaption']
    questions = data['questions']

    # Create HTML content for the form
    form_html = f"""
    <html>
    <head>
        <title>{form_title}</title>
    </head>
    <body>
        <h1>{form_title}</h1>
        <p>{form_caption}</p>
    """

    # Add each question to the HTML content
    for i, question in enumerate(questions):
        form_html += f"""
        <div>
            <label>{question['questionText']}</label><br>
            {"".join([f'<input type="radio" name="q{i}" value="{opt}"> {opt}<br>' for opt in question['options']])}
            <p>Correct Answer: {question['correctAnswer']}</p>
        </div>
        """

    form_html += "</body></html>"

    # Save HTML to a file named after the user's email
    filename = f"forms/{email}.html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create directory if it doesn't exist

    with open(filename, 'w') as file:
        file.write(form_html)

    return jsonify({"status": "success", "message": "Form saved successfully."})

if __name__ == '__main__':
    app.run(debug=True)
