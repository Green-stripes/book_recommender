# import streamlit as st
# import pandas as pd
# import numpy as np
# import datetime
# from PIL import Image
# import random
# import requests
# from io import BytesIO
# import ast




# st.title('Welcome to the book recommender')
# st.header('Where you find your next favourite book')
# # Load predictions data (replace with actual path to your predictions.csv)
# predictions_df = pd.read_csv('predictions.csv')

# # Function to get n random books from the dataframe
# def get_random_books(df, n=6):
#     return df.sample(n).to_dict('records')

# # Function to resize image to uniform size
# def resize_image(image_url, size=(200, 300)):
#     try:
#         if pd.isna(image_url) or not image_url.startswith(('http://', 'https://')):
#             raise ValueError("Invalid URL")
#         response = requests.get(image_url)
#         img = Image.open(BytesIO(response.content))
#         img = img.resize(size, Image.LANCZOS)
#         return img
#     except Exception as e:
#         st.error(f"Error loading image: {e}")
#         return None

# # Initialize session state for button clicks
# if 'random_books' not in st.session_state:
#     st.session_state.random_books = get_random_books(predictions_df, 6)
# if 'button_clicked' not in st.session_state:
#     st.session_state.button_clicked = False
#     st.session_state.clicked_book_index = None

# # Streamlit app title
# st.title('Choose your favourite:')

# # Refresh button below the images
# if st.button('None of these? Refresh Images'):
#     st.session_state.random_books = get_random_books(predictions_df, 6)
#     st.session_state.button_clicked = False
#     st.experimental_rerun()

# # Display images in two rows of three
# for i in range(0, len(st.session_state.random_books), 3):
#     cols = st.columns(3)
#     for col, book, idx in zip(cols, st.session_state.random_books[i:i+3], range(i, i+3)):
#         resized_image = resize_image(book['coverImg'])
#         if resized_image:
#             # Display image
#             col.image(resized_image, caption=f"{book['title']} by {book['author']}", use_column_width=True)

#             # Check if the title button was clicked
#             if col.button(f"Did you enjoy {book['title']}", key=f"button_{idx}"):
#                 st.session_state.button_clicked = True
#                 st.session_state.clicked_book_index = idx
#                 st.experimental_rerun()

# # Display the recommended book if a button was clicked
# if st.session_state.button_clicked and st.session_state.clicked_book_index is not None:
#     clicked_book = st.session_state.random_books[st.session_state.clicked_book_index]
#     recommended_books = predictions_df[predictions_df['class'] == clicked_book['class']]

#     # Debugging: Check if we have recommended books
#     st.write(f"Found {len(recommended_books)} recommended books for class {clicked_book['class']}")

#     if not recommended_books.empty:
#         recommended_book = recommended_books.sample(1).iloc[0]

#            # Parse the genres string to a list if necessary
#         if isinstance(clicked_book['genres'], str):
#             genres_list = ast.literal_eval(clicked_book['genres'])
#         else:
#             genres_list = clicked_book['genres']

#         st.title("You appear to enjoy genres such as:")
#         st.markdown(", ".join(genres_list))

#         # Display recommended book centered on the page
#         st.markdown("---")  # Add a horizontal rule for separation
#         st.header("Recommended Book")
#         recommended_image = resize_image(recommended_book['coverImg'])

#         # Debugging: Check the recommended book details
#         st.write(f"Recommended book: {recommended_book['title']} by {recommended_book['author']}")

#         if recommended_image:
#             st.image(recommended_image, caption=f"{recommended_book['title']} by {recommended_book['author']}", use_column_width=True)

# # Custom CSS for uniform image size (optional)
# st.markdown(
#     """
#     <style>
#     .stImage > img {
#         object-fit: cover;
#     }
#     </style>
#     """, unsafe_allow_html=True
# )

import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image
import random
import requests
from io import BytesIO
import ast

st.title('Welcome to the book recommender')
st.header('Where you find your next favourite book')

# Load predictions data (replace with actual path to your predictions.csv)
predictions_df = pd.read_csv('predictions.csv')

# Ensure Num Ratings column exists, otherwise add a mock column for demonstration
if 'numRatings' not in predictions_df.columns:
    predictions_df['numRatings'] = np.random.randint(1, 1000, size=len(predictions_df))  # Mock data

# Sort the DataFrame by Num Ratings in descending order
sorted_df = predictions_df.sort_values(by='numRatings', ascending=False)

# Function to get 6 random books from the top 100 books by Num Ratings
def get_top_books(df, top_n=6, select_n=6):
    top_books = df.head(top_n)
    return top_books.sample(select_n).to_dict('records')

# Function to resize image to uniform size
def resize_image(image_url, size=(200, 300)):
    try:
        if pd.isna(image_url) or not image_url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL")
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize(size, Image.LANCZOS)
        return img
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# Initialize session state for button clicks
if 'random_books' not in st.session_state:
    st.session_state.random_books = get_top_books(sorted_df, 100, 6)
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False
    st.session_state.clicked_book_index = None

# Streamlit app title
st.title('Choose your favourite:')

# Refresh button below the images
if st.button('None of these? Refresh Images'):
    st.session_state.random_books = get_top_books(sorted_df, 100, 6)
    st.session_state.button_clicked = False
    st.experimental_rerun()

# Display images in two rows of three
for i in range(0, len(st.session_state.random_books), 3):
    cols = st.columns(3)
    for col, book, idx in zip(cols, st.session_state.random_books[i:i+3], range(i, i+3)):
        resized_image = resize_image(book['coverImg'])
        if resized_image:
            # Display image
            col.image(resized_image, caption=f"{book['title']} by {book['author']}", use_column_width=True)

            # Check if the title button was clicked
            if col.button(f"Did you enjoy {book['title']}", key=f"button_{idx}"):
                st.session_state.button_clicked = True
                st.session_state.clicked_book_index = idx
                st.experimental_rerun()

# Display the recommended book if a button was clicked
if st.session_state.button_clicked and st.session_state.clicked_book_index is not None:
    clicked_book = st.session_state.random_books[st.session_state.clicked_book_index]
    recommended_books = predictions_df[predictions_df['class'] == clicked_book['class']]

    # Debugging: Check if we have recommended books
    st.write(f"Found {len(recommended_books)} recommended books for class {clicked_book['class']}")

    if not recommended_books.empty:
        recommended_book = recommended_books.sample(1).iloc[0]

        # Parse the genres string to a list if necessary
        if isinstance(clicked_book['genres'], str):
            genres_list = ast.literal_eval(clicked_book['genres'])
        else:
            genres_list = clicked_book['genres']

        st.title("You appear to enjoy genres such as:")
        st.markdown(", ".join(genres_list))

        # Display recommended book centered on the page
        st.markdown("---")  # Add a horizontal rule for separation
        st.header("Recommended Book")
        recommended_image = resize_image(recommended_book['coverImg'])

        # Debugging: Check the recommended book details
        st.write(f"Recommended book: {recommended_book['title']} by {recommended_book['author']}")

        if recommended_image:
            st.image(recommended_image, caption=f"{recommended_book['title']} by {recommended_book['author']}", use_column_width=True)

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
