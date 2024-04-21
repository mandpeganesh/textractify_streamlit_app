import streamlit as st
import boto3
import io
import json
from PIL import Image

# Function to perform OCR using AWS Textract
def image_to_text(image_bytes):

    aws_secret_key = st.secrets["aws_secret_key"]
    aws_access_key = st.secrets["aws_access_key"]

    # Initialize AWS Textract client
    textract_client = boto3.client('textract', region_name='us-west-2', aws_access_key_id=aws_access_key,
                        aws_secret_access_key=aws_secret_key)

    # Call Textract API to detect text
    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})

     # Extract text from response
    text_lines = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text_lines.append(block['Text'])

    # Join text lines with newline character
    text = '\n'.join(text_lines)
    return text

# Page Title and Description
st.set_page_config(page_title="Textractify: Extract Text from Images", layout="wide")
st.title(":clipboard: Textractify: Extract Text from Images")

# Upload image in sidebar
uploaded_image = st.sidebar.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

# If image is uploaded
if uploaded_image is not None:
    # Read image data as bytearray
    image_bytes = bytearray(uploaded_image.read())

    # Display the uploaded image and extracted text side by side
    col1, col2 = st.columns([2, 3])
    with col1:
        st.header("Uploaded Image")
        st.image(Image.open(io.BytesIO(image_bytes)), use_column_width=True)
    with col2:
        # Button to perform OCR
        if st.button('Convert Image to Text'):
            # Perform OCR using AWS Textract
            with st.spinner('Extracting text...'):
                text_result = image_to_text(image_bytes)
            # Display the extracted text
            st.header("Extracted Text:")
            st.write(text_result)

# Credits
st.markdown("---")
st.write("Created with ❤️ by GNM")
st.write("Powered by AWS Textract")
