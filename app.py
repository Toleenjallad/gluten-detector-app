import streamlit as st
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt

gluten_keywords = ["wheat", "barley", "rye", "malt", "gluten", "semolina", "farina", "spelt", "triticale"]
safe_keywords = ["gluten-free", "gf", "corn", "rice", "quinoa", "potato", "almond flour", "oat (certified gf)"]

st.title("🥖 Gluten Ingredient Detector")

uploaded_file = st.file_uploader("Upload a receipt or label image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.subheader("🔍 OCR Extracted Text")
    text = pytesseract.image_to_string(image)
    st.text_area("Extracted Text", text, height=200)

    text_lower = text.lower()
    gluten_found = [word for word in gluten_keywords if word in text_lower]
    safe_found = [word for word in safe_keywords if word in text_lower]

    st.subheader("📊 Gluten Classification Result")

    if gluten_found:
        st.error(f"❌ Contains Gluten: {', '.join(gluten_found)}")
        label = "Contains Gluten"
    elif safe_found:
        st.success(f"✅ Likely Gluten-Free: {', '.join(safe_found)}")
        label = "Gluten-Free"
    else:
        st.warning("⚠️ Unknown — No gluten-related keywords found")
        label = "Unknown"

    st.subheader("📈 Gluten Risk Summary")
    labels = ['Contains Gluten', 'Gluten-Free', 'Unknown']
    sizes = [1 if label == l else 0 for l in labels]
    colors = ['red', 'green', 'gray']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
