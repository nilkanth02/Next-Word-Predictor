import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Load model and tokenizer
model = load_model("next_word_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

max_len = model.input_shape[1] + 1
total_words = len(tokenizer.word_index) + 1

# Predict top 3 next words
def predict_top_3(seed_text):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_len-1, padding='pre')
    prediction = model.predict(token_list, verbose=0)[0]
    top_indices = prediction.argsort()[-3:][::-1]
    top_words = [tokenizer.index_word.get(idx, "") for idx in top_indices]
    return top_words

# Streamlit page settings
st.set_page_config(page_title="Smart Keyboard", layout="centered")
st.title("⌨️ AI Smart Keyboard")

st.markdown("#### 🔮 Suggestions (Tap to autocomplete)")

# Session to hold current input
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Predict only if text exists
if st.session_state.user_input.strip() != "":
    suggestions = predict_top_3(st.session_state.user_input)
    cols = st.columns(3)
    for i, word in enumerate(suggestions):
        if word and cols[i].button(f"🔹 {word}"):
            st.session_state.user_input += " " + word
            st.rerun()

else:
    st.info("Start typing below to get predictions...")

# Place typing input bar at bottom
st.markdown("---")
user_input = st.text_input("🖊️ Type your text here", st.session_state.user_input)

# Update session state on manual typing
if user_input != st.session_state.user_input:
    st.session_state.user_input = user_input

# Footer
st.markdown("---")
st.caption("Made by Nilkanth Ahire | LSTM-powered smart typing experience ✨")
