import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image
import random
import requests
from io import BytesIO





st.title('Welcome to the book recommender')
st.header('Where you find your next favourite book')
# Load predictions data (replace with actual path to your predictions.csv)
predictions_df = pd.read_csv('predictions.csv')
def get_random_books(df, n=6):
    return df.sample(n).to_dict('records')

# Function to resize image to uniform size
def resize_image(image_url, size=(200, 300)):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize(size, Image.LANCZOS)
        return img
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# Streamlit app title
st.title('Random Book Covers')

# Display images in two rows of three
random_books = get_random_books(predictions_df, 6)
for i in range(0, len(random_books), 3):
    cols = st.columns(3)
    for col, book in zip(cols, random_books[i:i+3]):
        resized_image = resize_image(book['coverImg'])
        if resized_image:
            # Display image
            col.image(resized_image, caption=f"{book['title']} by {book['author']}", use_column_width=True)

            # Check if the title button was clicked
            if col.button(f"Did you enjoy {book['title']}"):
                # Get recommended book details based on class
                recommended_book = predictions_df[predictions_df['class'] == book['class']].iloc[0]
                st.title(f"You appear to enjoy {book['genre']}")

                # Display recommended book centered on the page
                st.markdown("---")  # Add a horizontal rule for separation
                st.header("Recommended Book")
                recommended_image = resize_image(recommended_book['recommended_cover'])
                if recommended_image:
                    st.image(recommended_image, caption=f"{recommended_book['recommended_title']} by {recommended_book['recommended_author']}", use_column_width=True)

# Custom CSS for uniform image size (optional)
st.markdown(
    """
    <style>
    .stImage > img {
        object-fit: cover;
    }
    </style>
    """, unsafe_allow_html=True
)
