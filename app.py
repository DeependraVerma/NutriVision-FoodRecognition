from dotenv import load_dotenv
load_dotenv()  
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image

import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


def main():
    st.set_page_config(page_title="NutriVision-FoodRecognition", page_icon="🍲")
    st.header("Your Dietitian and Nutritionist")

    language_options = ["English", "Hindi"]
    selected_language = st.selectbox("Select Language:", language_options)

    if selected_language == "English":
        input_prompt1 = """
        Embark on a culinary exploration as you uncover the secrets of the delectable dish captured in the uploaded image:
        1. Discover key details about the dish, including its name and culinary essence.
        2. Explore the fascinating origins of the dish, unraveling its cultural and historical significance.
        3. Dive into the rich tapestry of ingredients, presented pointwise, that contribute to the dish's exquisite flavor profile.
        """

        input_prompt2 = """
        As the culinary maestro guiding eager chefs, lay out the meticulous steps for crafting the featured dish:
        1. Start with selecting the finest ingredients, emphasizing quality and freshness.
        2. Detail the process of washing, peeling, and chopping each ingredient with precision.
        3. Unveil the culinary artistry behind the cooking process, step by step.
        4. Share expert tips and techniques to elevate the dish from ordinary to extraordinary.
        """

        input_prompt3 = """
        In your role as a nutritional advisor, present a comprehensive overview of the dish's nutritional value:
        1. Display a table showcasing nutritional values in descending order, covering calories, protein, fat, and carbohydrates.
        2. Create a second table illustrating the nutritional contribution of each ingredient, unraveling the dietary secrets within.
        """


        input_prompt4 = """
        Act as a dietitian and nutritionist:
        1. Your task is to provide 2 vegeterian dish alternative to the dish uploaded in the image which have the same nutritional value.
        2. Your task is to provide 2 Non-vegeterian dish alternative to the dish uploaded in the image which have the same nutritional value.
        """


    elif selected_language == "Hindi":
        input_prompt1 = """
        उपयुक्त छवि में कैद किए गए स्वादिष्ट व्यंजन के रहस्यों की खोज में एक रसोईय अन्वेषण पर प्रवृत्त हों:
        1. डिश के बारे में मुख्य विवरण जानें, जिसमें इसका नाम और रसोईय स्वभाव है।
        2. डिश की आकर्षक उत्पत्ति की खोज करें, जो इसके सांस्कृतिक और ऐतिहासिक महत्व को खोलती है।
        3. डिश के सर्वोत्तम स्वाद प्रोफाइल में योगदान करने वाली आइटमों की समृद्धि में डूबें।
        """

        input_prompt2 = """
        उत्सुक शेफ्स को मार्गदर्शन करने वाले रसोई के मास्टर शेफ के रूप में, विवेचना करें:
        1. सर्वोत्तम सामग्री का चयन करने की शुरुआत करें, गुणवत्ता और ताजगी पर जोर दें।
        2. प्रत्येक आइटम को सहीपन से धोने, छीलने और काटने की प्रक्रिया की विस्तार से बताएं।
        3. खाद्य प्रक्रिया के पीछे रसोईय कला को एक-एक कदम से बताएं।
        4. सामान्य से अद्वितीय बनाने के लिए डिश को उच्चतम करने के लिए विशेषज्ञ सुझाव और तकनीक साझा करें।
        """

        input_prompt3 = """
        एक पोषण सलाहकार के रूप में, डिश के पोषण सम्बंधी सम्पूर्ण अवलोकन प्रस्तुत करें:
        1. कैलोरी, प्रोटीन, वसा और कार्बोहाइड्रेट की घटाई गई पोषण मूल्यों को दिखाने वाला एक तालिका प्रदर्शित करें।
        2. हर आइटम के पोषण योगदान को बताने वाली दूसरी तालिका बनाएं, जिसमें आहार रहस्य हैं।
        """

        input_prompt4 = """
        एक रसोई समाचार पत्र के रूप में, समर्थन और पोषण में समानता के साथ एक शाकाहारी वैकल्पिक डिश की विस्तृत सूची बनाएं:
        1. प्राकृतिक और ताजगी को बढ़ावा देने के लिए एक शाकाहारी वैकल्पिक डिश के रूप में सूक्ष्मता से स्पष्टीकृत करें।
        2. मौजूदा के पोषण मूल्यों के साथ समर्थन और पोषण में समानता के लिए एक सूची बनाएं, नॉन-वेज वैकल्पिक के लिए एक लिस्ट।
        """

    input_text = st.text_input("Input Prompt: ", key="input")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Buttons organized in a 2x2 table
    col1, col2 = st.columns(2)

    submit1 = col1.button("Get Dish Name and Ingredients")
    submit2 = col1.button("How to Cook")
    submit3 = col2.button("Nutritional Value for 1 Person")
    submit4 = col2.button("Alternative Dishes with Similar Nutritional Values")

    if submit1:
        if uploaded_file is not None:
            pdf_content = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the dish image.")

    if submit2:
        if uploaded_file is not None:
            pdf_content = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the dish image.")

    if submit3:
        if uploaded_file is not None:
            pdf_content = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the dish image.")

    if submit4:
        if uploaded_file is not None:
            pdf_content = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt4, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the dish image.")


if __name__ == "__main__":
    main()
