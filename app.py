import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Load model and tokenizer
model = load_model("next_word_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Get max sequence length used in training
max_len = model.input_shape[1] + 1
total_words = len(tokenizer.word_index) + 1

# Predict function
def predict_next_word(seed_text):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_len-1, padding='pre')
    predicted_probs = model.predict(token_list, verbose=0)
    predicted_index = np.argmax(predicted_probs)
    predicted_word = tokenizer.index_word.get(predicted_index, "<unk>")
    return predicted_word

# Streamlit UI
st.set_page_config(page_title="Next Word Predictor", layout="centered")
st.title("🧠 Next Word Predictor")
st.write("Enter a short phrase and I'll try to predict the next word using an LSTM model!")

seed_text = st.text_input("🔡 Enter your text:", "")

if st.button("🔮 Predict"):
    if seed_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        next_word = predict_next_word(seed_text)
        st.success(f"✨ Predicted Next Word: **{next_word}**")

st.markdown("---")
st.caption("Made with ❤️ by Nilkanth Ahire | LSTM-based NLP Model")
