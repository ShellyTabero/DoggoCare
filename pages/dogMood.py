import torch
from torchvision import transforms
from PIL import Image
import os
import streamlit as st
from streamlit_extras.grid import grid
import io
import config
import google.generativeai as genai


config.local_css("style.css")
config.add_bg_from_url(config.background_link)

genai.configure(api_key=config.GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def get_random_recommendation(mood):
    if mood == 'happy!' or mood == 'relaxed!':
        prompt = f'What should I do to keep my dog {mood[:-1]} like they are now? Give only one recommendation, up to 20 words please'
    else:
        prompt = f'What should I do if my dog is {mood[:-1]}? Give only one recommendation, up to 20 words please'

    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
    response = model.generate_content(prompt, safety_settings=safety_settings)
    gen_recommendation = response.text
    return gen_recommendation


def get_mood(image):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    model_path = os.path.join(parent_dir, 'model.pth')
    loaded_model = torch.load(model_path)

    preprocess = transforms.Compose([
        transforms.Resize((375, 500)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image_tensor = preprocess(image)
    image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension

    # Perform inference
    loaded_model.eval()
    with torch.no_grad():
        outputs = loaded_model(image_tensor)

    # Process the predictions
    _, predicted = torch.max(outputs, 1)
    predicted_label_index = predicted.item()

    # Map the predicted index to the corresponding class label
    emotion_classes = ['angry.', 'happy!', 'relaxed!', 'sad.']  # Rreplace with your actual class labels
    predicted_label = emotion_classes[predicted_label_index]

    return predicted_label

if st.button("Back"):
    st.switch_page("pages/page4.py")

st.markdown("<h1 style='text-align: center; color: black;'>DoggoCare</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Upload a picture of your dog & Check its mood!</h1>", unsafe_allow_html=True)

my_grid = grid(1, [1,3,1], 1, 1, vertical_align="bottom")

# Row 1
uploaded_file = my_grid.file_uploader("dog-image", label_visibility='hidden')

# Row 2
my_grid.markdown("")
placeholder = my_grid.empty()
my_grid.markdown("")

if uploaded_file is not None:
    file_contents = uploaded_file.getvalue()
    image = Image.open(io.BytesIO(file_contents))
    placeholder.image(image, width=300)
    # Row 3
    curr_mood = get_mood(image)
    text_emotion = f"Your dog is {curr_mood}"
    font_size = 22

    html_string_emotion = f"<p class='custom-text' style='font-size: {font_size}px;'>{text_emotion}</p>"
    my_grid.write(html_string_emotion, unsafe_allow_html=True)

    # Row 4
    recommendation = get_random_recommendation(curr_mood)
    html_string_recommendation = f"<p class='custom-text' style='font-size: {font_size}px;'>{recommendation}</p>"
    my_grid.write(html_string_recommendation, unsafe_allow_html=True)




