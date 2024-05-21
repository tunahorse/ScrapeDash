from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup
import os
import datetime
from werkzeug.utils import secure_filename
import re
from playwright.sync_api import sync_playwright


app = Flask(__name__)

def sanitize_directory_name(directory):
    if directory is None:
        directory = ''
    elif not isinstance(directory, str):
        directory = str(directory)

    # Remove invalid characters and replace spaces with underscores
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '', directory)
    sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', sanitized_name)
    sanitized_name = re.sub(r'_+', '_', sanitized_name)
    sanitized_name = sanitized_name.strip('_')
    return sanitized_name
# Custom filter to format timestamp
@app.template_filter('datetime')
def format_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    return redirect('/dash')

@app.route('/input', methods=['GET', 'POST'])
def input_url():
    if request.method == 'POST':
        url = request.form['url']
        if url:
            return redirect(f'/scrape?url={url}')
        else:
            return redirect('/manual_input/')
    return render_template('input.html')

@app.route('/scrape')
def scrape():
    url = request.args.get('url')

    try:
        # Try scraping with BeautifulSoup first
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()
        else:
            raise Exception(f"HTTP error: {response.status_code}")

    except Exception as e:
        print(f"BeautifulSoup scraping failed: {str(e)}. Falling back to Playwright.")

        # If BeautifulSoup fails, use Playwright as a fallback
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url)
                text_content = page.content()
                browser.close()

        except Exception as e:
            print(f"Playwright scraping failed: {str(e)}")
            return f"There was an issue scraping the data for {url}. You will need to debug this."

    # Save the scraped data to a file
    directory = sanitize_directory_name(url)
    if not os.path.exists(directory):
        os.makedirs(directory)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/data_{timestamp}.txt"
    with open(filename, 'w', encoding='utf-8') as file:

        try:
            file.write(text_content)
        except UnicodeEncodeError:
            #print the actual error 
            print(text_content)
            print(f"Error writing to {filename}")
            return f"There was an issue saving the scraped data for {url}. You will need to debug this."
        

    return redirect('/dash')

@app.route('/dash')
def dashboard():
    directories = [dir for dir in os.listdir('.') if os.path.isdir(dir) and dir not in ['templates', 'static','.git']]
    return render_template('dashboard.html', directories=directories)

@app.route('/data/<path:directory>')
def display_data(directory):
    # Sanitize the directory name
    sanitized_directory = sanitize_directory_name(directory)
    
    # Get the list of all files in the directory
    files = sorted(os.listdir(sanitized_directory), reverse=True)
    
    return render_template('data.html', directory=directory, files=files)


@app.route('/manual_input/', defaults={'directory': ''}, methods=['GET', 'POST'])
@app.route('/manual_input/<path:directory>', methods=['GET', 'POST'])
def manual_input(directory):
    try:
        if request.method == 'POST':
            # Get the directory name from the form
            directory = request.form.get('directory', directory)
            
            # Sanitize the directory name
            sanitized_directory = sanitize_directory_name(directory)
            
            # Print the sanitized directory name
            print(f"Sanitized Directory: {sanitized_directory}")
            
            # Create the directory if it doesn't exist
            if not os.path.exists(sanitized_directory):
                os.makedirs(sanitized_directory)
            
            # Handle file uploads
            uploaded_files = request.files.getlist('files')
            for file in uploaded_files:
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(sanitized_directory, filename)
                    file.save(file_path)
            
            # Handle manual text input
            manual_text = request.form.get('manual_text', '')
            if manual_text:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"manual_text_{timestamp}.txt"
                file_path = os.path.join(sanitized_directory, filename)
                with open(file_path, 'w') as file:
                    file.write(manual_text)
            
            return redirect(f'/data/{sanitized_directory}')
        
        return render_template('manual_input.html', directory=directory)
    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e), 500

@app.route('/data/<path:directory>/<path:filename>')
def view_data(directory, filename):
    # Sanitize the directory name
    sanitized_directory = sanitize_directory_name(directory)
    
    # Construct the full file path
    full_path = os.path.join(sanitized_directory, filename)
    
    with open(full_path, 'r') as file:
        data = file.read()
    
    return render_template('view_data.html', directory=directory, filename=filename, data=data)

if __name__ == '__main__':
    app.run(debug=True)
