import pyrebase
import streamlit as st
from datetime import datetime
import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import io
import json
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie 
import base64
# Firebase configuration
firebaseConfig = {
  'apiKey': "AIzaSyBc1T2F81JKKHPxZSd5psqXU-r3sdunIHs",
  'authDomain': "chit-chat-image.firebaseapp.com",
  'projectId': "chit-chat-image",
  'databaseURL': "https://chit-chat-image-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "chit-chat-image.appspot.com",
  'messagingSenderId': "938344095909",
  'appId': "1:938344095909:web:c8dc59470641196539ed4c",
  'measurementId': "G-NKWXHYL9DX"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

# Function to initialize the Gemini-Pro model
def initialize_model():
    load_dotenv(find_dotenv(), override=True)
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# Function to save chat history to Firebase
def save_chat_history(user_id, conversation):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.child(user_id).child("ChatHistory").child(timestamp).set(conversation)

# Function to retrieve chat history from Firebase
def get_chat_history(user_id):
    chat_history = db.child(user_id).child("ChatHistory").get()
    return chat_history.val()

# Function to convert Streamlit image to PIL image
def st_image_to_pil(st_image):
    image_data = st_image.read()
    pil_image = Image.open(io.BytesIO(image_data))
    return pil_image

# Function to ask question and get answer
def ask_and_get_answer(prompt, img):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, img])
    return response.text

# Function to display chat history
@st.cache_resource(hash_funcs={str: lambda _: None})
def get_cached_chat_history(user_id):
    return get_chat_history(user_id)

# Function to update cached chat history after removal
@st.cache_resource(hash_funcs={str: lambda _: None})
def update_cached_chat_history(user_id):
    # Simply invalidate the cache so that the next call to get_cached_chat_history will fetch fresh data
    return None

# Function to display chat history with remove button
def display_chat_history(user_id):
    st.subheader("Chat History")
    chat_history = get_cached_chat_history(user_id)
    if chat_history:
        for timestamp, conversation in chat_history.items():
            st.write(f"Timestamp: {timestamp}")
            st.write(f"Conversation: {conversation}")
            if st.button(f"Remove Conversation {timestamp}"):
                # Remove the conversation from Firebase
                db.child(user_id).child("ChatHistory").child(timestamp).remove()
                # Update cached chat history after removal
                update_cached_chat_history(user_id)
            st.write("---")
def display_contact_page():
    name = st.text_input("Name", "")
    email = st.text_input("Email", "")
    subject = st.text_input("Subject", "")
    message = st.text_area("Message", "")
    if st.button("Send"):
        # Store form data in Firebase
        data = {
            "Name": name,
            "Email": email,
            "Subject": subject,
            "Message": message
        }
        db.child("ContactFormSubmissions").push(data)
        st.success("Message sent successfully!")
        # Clear form inputs after submission
        name = ""
        email = ""
        subject = ""
        message = ""
    # Email Address
    st.write("You can email us at gajerakrina5@gmail.com")
    # Social Media Links
    st.write("[LinkedIn] https://www.linkedin.com/in/krinagajera")
    st.write("[GitHub] https://github.com/krina981")
    # Privacy Policy and Terms of Service
    # Feedback Form
    feedback = st.text_area("Share your feedback", "")
    if st.button("Submit Feedback"):
        # Logic to store feedback
        # For now, let's just print the feedback
        st.success("Feedback submitted successfully!")
        st.write("Feedback:", feedback)
    # Call to Action
    st.write("We value your input! Don't hesitate to reach out with any questions, feedback, or inquiries.")


    # Display project content
st.sidebar.title("IMAGE-CHIT CHAT APP")
choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign up'])

# Set background image and style for option menu
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://wallpaperaccess.com/full/1155119.jpg");
        background-size: cover;
    }

    /* Change color of option menu */
    .sidebar-content .stOptionMenu div[data-baseweb="menu"] {
        background-color: #4CAF50; /* Change the color to your desired color */
    }

    /* Change color of option menu items */
    .sidebar-content .stOptionMenu div[data-baseweb="menu"] button[data-baseweb="menu-item"] {
        color: #ffffff; /* Text color */
        background-color: #4CAF50; /* Background color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

## Function to display project content
def display_project_content(user_id):
    st.markdown("<p style='text-transform: uppercase; font-size: 20px; display: inline-block;'><img src='https://images.emojiterra.com/google/noto-emoji/unicode-15/animated/1f916.gif' style='vertical-align: middle; width: 30px;'> GEMINI-PRO VISION: INTERACTIVE IMAGE CHAT PLATFORM </p>", unsafe_allow_html=True)



    # Layout for the title and image
    col1, col2 = st.columns([1, 7])
    with col1:
        st.image("C:/Users/91932/Desktop/TYDS LAST/FINAL PROJECT/static/k2.png", width=80)  # Adjust path and width as needed

    with col2:
        st.subheader("Are You Ready To Angage In Image-Based Chit Chat? ")
    # Upload image
    img = st.file_uploader("Select an image:", type=['jpg', 'png', 'jpeg', 'gif'])

    if img:
        # Display the uploaded image
        st.image(img, caption="Let's Chit-Chat With This Image!!")

        # Layout for text input and icon for asking a question
        col1, col2 = st.columns([1, 10])
        with col1:
            st.image("C:/Users/91932/Desktop/TYDS LAST/FINAL PROJECT/static/user.png", width=30)  # Adjust path and width as needed
        with col2:
            prompt = st.text_area(label="Ask a Question About This Image:", value="")

        if prompt:
            # Convert Streamlit image to PIL image
            pil_image = st_image_to_pil(img)

            # Generate answer
            with st.spinner("Generating Response..."):
                answer = ask_and_get_answer(prompt, pil_image)

            # Layout for text input and icon for Gemini's answer
            col1, col2 = st.columns([1, 10])
            with col1:
                st.image("C:/Users/91932/Desktop/TYDS LAST/FINAL PROJECT/static/computer.png", width=30)  # Adjust path and width as needed
            with col2:
                st.text_area(label="", value=answer)

            # Save conversation to chat history
            conversation = {"Prompt": prompt, "Answer": answer}
            save_chat_history(user_id, conversation)

            # Display chat history
            display_chat_history(user_id)


# Initialize the Gemini-Pro model
initialize_model()

if choice == 'Sign up':
    # Sign up Block
    email = st.sidebar.text_input('Please Enter Your Email Address')
    password = st.sidebar.text_input('Please Enter Your Password', type='password')
    handle = st.sidebar.text_input('Please Input Your App Handle Name', value='Default')
    submit = st.sidebar.button('Create My Account')
    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your Account Is Created Successfully!')
        st.balloons()
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('WELCOME ' + handle)
        st.info('Login via login Drop Down Selection')

elif choice == 'Login':
    # Login Block
    email = st.sidebar.text_input('Please Enter Your Email Address')
password = st.sidebar.text_input('Please Enter Your Password', type='password')
login = st.sidebar.checkbox('Login')
if login:
    user = auth.sign_in_with_email_and_password(email, password)
    user_id = user['localId']
    # Assuming the selection logic is defined earlier in your code

    # Display the menus only if the user successfully logs in
    selected = option_menu(
            menu_title="Main Menu",  # required
            options=["Home", "Project", "Contact"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
        )
    if selected:
            if selected == "Home":
                image_path = "C:/Users/91932/Desktop/TYDS LAST/FINAL PROJECT/static/k3.gif"

                # Read the image file
                with open(image_path, "rb") as file:
                    image_data = file.read()

                # Encode the image data to base64
                encoded_image = base64.b64encode(image_data).decode()

                # Construct the HTML with the base64 encoded image
                html = f"<p style='text-transform: uppercase; font-size:30px; display: inline-block;'><img src='data:image/gif;base64,{encoded_image}' style='vertical-align: middle; width: 150px;'> <b>WELCOME TO CHIT-CHAT APP!!<b></p>"

                st.markdown(html, unsafe_allow_html=True)

                st.markdown("<p style='text-transform: uppercase; font-size: 14px;'>Explore the fascinating world of image-based conversations with Gemini Pro. Ask questions about any image, and let Gemini provide insightful answers. Dive into our projects to experience the future of AI-driven interactions. Don't forget to reach out to us through the Contact Us section if you have any questions or feedback. Start your journey now!</p>", unsafe_allow_html=True)

            elif selected == "Project":
                display_project_content(user_id)

            elif selected == "Contact":
                image_path = "C:/Users/91932/Desktop/TYDS LAST/FINAL PROJECT/static/k4.gif"

                # Read the image file
                with open(image_path, "rb") as file:
                    image_data = file.read()

                # Encode the image data to base64
                encoded_image = base64.b64encode(image_data).decode()
                html = f"<p style='text-transform: uppercase; font-size:60px; display: inline-block;'><img src='data:image/gif;base64,{encoded_image}' style='vertical-align: middle; width: 150px;'><b>CONTACT US<b></p>"
                st.markdown(html, unsafe_allow_html=True)
                display_contact_page()