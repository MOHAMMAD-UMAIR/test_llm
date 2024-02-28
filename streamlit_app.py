import streamlit as st
from openai  import OpenAI
import os

# # Everything is accessible via the st.secrets dict:
# st.write("OPEN_API_KEY:", st.secrets["OPEN_API_KEY"])


# And the root-level secrets are also accessible as environment variables:
st.write(
    "Has environment variables been set:",
    os.environ["OPEN_API_KEY"] == st.secrets["OPEN_API_KEY"] 
)


st.title('🦜🔗 Quickstart App')

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

# File upload widget
uploaded_file = st.file_uploader("Choose a text file", type=["txt"])


if uploaded_file is not None:
    st.success("File successfully uploaded!")
    # Read the content of the file
    file_contents = uploaded_file.read()
    # Display the content
    st.subheader("File Content:")
    st.text(file_contents)
    system_text= f''' Compose a complete cover letter for the position of [job title] at [company name],
 incorporating a strong introduction, a summary of relevant skills and experiences, an explanation of how my skills match the job requirements, 
 a highlight of my most significant achievement, an explanation of my career gap or job switch (if applicable),
 showcasing my adaptability and willingness to learn, demonstrating my passion for the industry, 
 emphasizing my strong work ethic and commitment, 
 mentioning the value of my professional network, 
 addressing the company’s values and culture, 
 and ending with a powerful conclusion that expresses my eagerness for an interview.
 Based on the my CV text: \n {file_contents}
'''






def generate_response(input_text):
    client = OpenAI( api_key=st.secrets["OPEN_API_KEY"])
    # client = OpenAI(temperature=0.5, openai_api_key=openai_api_key)
    
    # llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    # ChatCompletion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": f"Write the cover letter in 3 paragraphs and dont be too verbose. Use simple words. The job description is : {input_text}"}
        ]
        )
    st.info(response.choices[0].message.content)
    
    





with st.form('my_form'):
    text = st.text_area('Enter The Job Description here:', 'Make sure the job description is structured')
    text_cleaned=text.strip()
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text_cleaned)