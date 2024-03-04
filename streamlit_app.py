import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import google.generativeai as genai

# Configure GenAI API
genai.configure(api_key='AIzaSyDlBFVsmV8pao6Ax-bcR0dc5h4CusiNCsc')

# Define function to identify manga character
def identify_manga_character(image):
    image.thumbnail((450,400))
    st.image(image, caption='Uploaded Image',output_format='auto')

    # Use GenAI model to identify character
    vision_model = genai.GenerativeModel('gemini-pro-vision')
    response = vision_model.generate_content(["Who is the character shown in the image? which manga/manhua is the character from? What is their role?", image])
    st.write(response.text)

# Streamlit app
def main():
    st.title('Manga Character Identification')

    # Image upload or URL input
    option = st.radio('Choose an option:', ('Upload Image', 'Enter Image URL'))

    if option == 'Upload Image':
        uploaded_file = st.file_uploader('Choose an image:', type=['jpg', 'jpeg', 'png'])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            identify_manga_character(image)
    else:
        image_url = st.text_input('Enter the URL of the image:')
        if st.button('Identify Character'):
            if image_url:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))
                    identify_manga_character(image)
                else:
                    st.error('Failed to fetch the image. Status code: {}'.format(response.status_code))
            else:
                st.warning('Please enter the URL of the image.')

if __name__ == '__main__':
    main()
