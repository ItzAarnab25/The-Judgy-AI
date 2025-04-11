from flask import Flask, render_template, request, jsonify

from google import genai
from google.genai import types
import requests
import base64

app = Flask(__name__)

client = genai.Client(api_key="AIzaSyBzMsoqR1LEsBO6T4h8ILWwDabOYeejt6g")


@app.route('/')
def index():
    return render_template('index.html')

def generate_comments(image_data):
    prompt = """You are a quirky and slightly gossipy auntie at an Indian wedding. 
    I will provide you with a face image of a person. 
    Please analyze their facial features and give a funny and lighthearted description of them,
    as if you were describing them to another auntie. Focus on things like their potential profession, 
    their personality quirks (based on their face), and what kind of rishta (marriage proposal) they might attract. 
    Use playful stereotypes and cultural references specific to India, but keep it respectful and humorous. 
    Avoid anything offensive or mean-spirited. 
    Provide a short, funny, and slightly sarcastic comment about it.
    Give all the comments in hindi, No translation needed and add emojis to make it interesting.
    """ 
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, types.Part.from_bytes(data=image_data, mime_type="image/jpeg")])
        return response.text.split('\n')
    except Exception as e:
        print(f"Error generating comments: {e}")
        return ["Error generating comments."]

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()
        image_data = data.get('image')
        if not image_data:
            return jsonify({'error': 'No image data received.'}), 400

        comment = generate_comments(image_data)
        return jsonify({'comment': comment})

    except Exception as e:
        print(f"Error handling upload: {e}")
        return jsonify({'error': 'Failed to process the image.'}), 500

if __name__ == '__main__':
    app.run(debug=True)