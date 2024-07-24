import streamlit as st
import pandas as pd
import keyboard

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

# Инициализация начального состояния таблицы
df = pd.DataFrame({
    'Column 1': ['A', 'B', 'C'],
    'Column 2': [1, 2, 3]
})

# Хранение истории изменений таблицы
history = [df.copy()]

def save_to_history(dataframe):
    """Сохранение текущего состояния таблицы в историю."""
    history.append(dataframe.copy())

def undo_last_change():
    """Отмена последнего изменения."""
    if len(history) > 1:
        history.pop()  # Удалить последнее состояние
        return history[-1]  # Вернуть предыдущее состояние
    return history[0]  # Если изменений нет, вернуть начальное состояние

# Функция для отслеживания нажатия Ctrl+Z
def on_key_event(event):
    if event.name == 'z' and keyboard.is_pressed('ctrl'):
        st.session_state.df = undo_last_change()
        st.experimental_rerun()

# Подключение функции для отслеживания нажатий клавиш
keyboard.on_press(on_key_event)

# Основной код Streamlit
if 'df' not in st.session_state:
    st.session_state.df = df

edited_df = st.experimental_data_editor(st.session_state.df)
if edited_df is not st.session_state.df:
    save_to_history(edited_df)
    st.session_state.df = edited_df

st.write(st.session_state.df)
