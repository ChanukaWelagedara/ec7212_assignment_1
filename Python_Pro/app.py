import os
import cv2
import time
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from intensity_reducer import process_image as reduce_intensity
from spatial_averager import process_image as spatial_average
from image_rotator import process_image as rotate_image
from block_averager import process_image as block_average

# Create Flask app
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs' 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_output_image(image, name):
    timestamp = int(time.time())
    filename = f"{name}_{timestamp}.png"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    cv2.imwrite(output_path, image)
    return f"outputs/{filename}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
  
    if 'file' not in request.files:
        return render_template('index.html', error='No file was uploaded')
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file was selected')
    
    if not allowed_file(file.filename):
        return render_template('index.html', 
                            error=f'Unsupported file type. Please use: {", ".join(ALLOWED_EXTENSIONS)}')
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    operation = request.form.get('operation')
    results = []
    
    try:
        # Task 1: Reduce intensity levels
        if operation == 'intensity':
            levels = int(request.form.get('levels', '2'))
            result, error = reduce_intensity(file_path, levels)
            if error:
                return render_template('index.html', error=error)
            
            output_path = save_output_image(result, f"intensity_{levels}")
            results.append({
                'title': f'Intensity levels: {levels}',
                'image': output_path
            })
        
        # Task 2: Spatial averaging with different neighborhoods
        elif operation == 'spatial':
            for size in [3, 10, 20]:
                result, error = spatial_average(file_path, size)
                if error:
                    return render_template('index.html', error=error)
                output_path = save_output_image(result, f"spatial_{size}x{size}")
                results.append({
                    'title': f'{size}×{size} Average',
                    'image': output_path
                })
        
        # Task 3: Image rotation
        elif operation == 'rotate':
            for angle in [45, 90]:
                result, error = rotate_image(file_path, angle)
                if error:
                    return render_template('index.html', error=error)
                output_path = save_output_image(result, f"rotate_{angle}")
                results.append({
                    'title': f'Rotated {angle}°',
                    'image': output_path
                })
        
        # Task 4: Block averaging (spatial resolution reduction)
        elif operation == 'block':
            for size in [3, 5, 7]:
                result, error = block_average(file_path, size)
                if error:
                    return render_template('index.html', error=error)
                output_path = save_output_image(result, f"block_{size}x{size}")
                results.append({
                    'title': f'{size}×{size} Block',
                    'image': output_path
                })
        
        original_img = cv2.imread(file_path)
        original_path = save_output_image(original_img, "original")
        return render_template('results.html', original=original_path, results=results)
        
    except Exception as e:
        return render_template('index.html', error=f'Error: {str(e)}')
if __name__ == '__main__':
    app.run(debug=True)
