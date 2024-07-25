import streamlit as st
import pandas as pd

# Set page title and layout
st.title('Hello, World!')
st.markdown('# Hello, World!')

# Create a header section
header = st.header('This is a header')

# Create a text input field
text_input = st.text_input('Enter your name', 'World')

# Create a button that prints the user's name when clicked
if st.button('Say hello'):
    st.write(f'Hello, {text_input}!')

# Create a sidebar with a slider and radio buttons
sidebar = st.sidebar
slider = sidebar.slider('Select a number between 1 and 10', min_value=1, max_value=10)
radio_buttons = sidebar.radio('Choose an option', ('Option 1', 'Option 2'))

# Display the user's input in the main section of the page
st.write(f'You selected {slider} and chose {radio_buttons}')

# Create a table with some sample data
data = {'Name': ['John', 'Mary', 'Bob'], 
        'Age': [25, 31, 42]}
st.dataframe(data)

# Загрузка файла
uploaded_file = st.file_uploader("Загрузите XLSX файл", type="xlsx")

if uploaded_file is not None:
    # Чтение файла в DataFrame
    df = pd.read_excel(uploaded_file)

    # Создание таблицы с возможностью фильтрации
    st.subheader("Таблица данных")
    filtered_df = st.dataframe(df, height=400)  

    # Добавление столбцов для фильтрации
    selected_columns = st.multiselect('Выберите столбцы для отображения', df.columns)
    filtered_df = df[selected_columns]

    # Создание кнопки для обновления таблицы
    if st.button("Обновить таблицу"):
        st.experimental_rerun() 
