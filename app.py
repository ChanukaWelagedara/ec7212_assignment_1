import os
import cv2
import time
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

# Import the image processing modules
from intensity_reducer import process_image as reduce_intensity
from spatial_averager import process_image as spatial_average
from image_rotator import process_image as rotate_image
from block_averager import process_image as block_average

# Create Flask app
app = Flask(__name__)

# Setup folders for uploads and results
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'  # Use forward slashes for compatibility

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Configure app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB limit

# Allowed image file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    """Check if file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_output_image(image, name):
    """Save processed image and return its path for display"""
    # Add timestamp to prevent cache issues
    timestamp = int(time.time())
    filename = f"{name}_{timestamp}.png"
    
    # Save the image
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    cv2.imwrite(output_path, image)
    
    # Return web-friendly path
    return f"outputs/{filename}"

@app.route('/')
def index():
    """Home page with upload form"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """Process the uploaded image"""
    # Validate file upload
    if 'file' not in request.files:
        return render_template('index.html', error='No file was uploaded')
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file was selected')
    
    if not allowed_file(file.filename):
        return render_template('index.html', 
                              error=f'Unsupported file type. Please use: {", ".join(ALLOWED_EXTENSIONS)}')
    
    # Save the uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Get selected operation
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
        
        # Save original for comparison
        original_img = cv2.imread(file_path)
        original_path = save_output_image(original_img, "original")
        
        # Show results
        return render_template('results.html', original=original_path, results=results)
        
    except Exception as e:
        return render_template('index.html', error=f'Error: {str(e)}')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
