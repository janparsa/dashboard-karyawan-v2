import os
import requests
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/upload-csv', methods=['POST'])
def upload_csv_to_blob():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be CSV format'}), 400
    
    # Get Vercel Blob token
    blob_token = os.getenv("dashboardkaryawanV2_READ_WRITE_TOKEN")
    if not blob_token:
        return jsonify({'error': 'Blob token not configured'}), 500
    
    try:
        filename = secure_filename(file.filename)
        
        # Vercel Blob API endpoint
        blob_api_url = "https://blob.vercel-storage.com"
        
        headers = {
            'Authorization': f'Bearer {blob_token}',
            'Content-Type': 'text/csv'
        }
        
        # Stream file directly to Vercel Blob
        response = requests.put(
            f"{blob_api_url}/{filename}",
            headers=headers,
            data=file.stream.read()
        )
        
        if response.status_code not in [200, 201]:
            return jsonify({
                'error': f'Failed to upload to blob: {response.text}'
            }), 500
        
        blob_data = response.json()
        
        return jsonify({
            'message': 'File uploaded successfully',
            'blob_url': blob_data.get('url'),
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

# For Vercel
if __name__ == '__main__':
    app.run(debug=True)