from flask import Flask, request, jsonify
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/api/submit/', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        text = request.form.get('text')
        screenshot = request.files.get('screenshot')

        if screenshot:
            print(f"Received file: {screenshot.filename}, Content-Type: {screenshot.content_type}")
            
            if screenshot.content_type == 'image/png':
                screenshot_path = os.path.join(app.config['UPLOAD_FOLDER'], screenshot.filename)
                screenshot.save(screenshot_path)

                return jsonify({'status': 'success', 'text': text, 'screenshot_path': screenshot_path})
            else:
                print("Invalid file format received.")
                return jsonify({'status': 'error', 'message': 'Invalid file format. Please upload a PNG file.'})

        return jsonify({'status': 'error', 'message': 'No file received.'})
    else:
        return jsonify({'status': 'error', 'message': 'Only POST requests are allowed.'})


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
