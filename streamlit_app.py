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

# Начальные данные
df = pd.DataFrame({
    'Column 1': ['A', 'B', 'C'],
    'Column 2': [1, 2, 3]
})

# История изменений
if 'history' not in st.session_state:
    st.session_state.history = [df.copy()]

def save_to_history(dataframe):
    """Сохранение текущего состояния таблицы в историю."""
    st.session_state.history.append(dataframe.copy())

def undo_last_change():
    """Отмена последнего изменения."""
    if len(st.session_state.history) > 1:
        st.session_state.history.pop()  # Удалить последнее состояние
        return st.session_state.history[-1]  # Вернуть предыдущее состояние
    return st.session_state.history[0]  # Если изменений нет, вернуть начальное состояние

# Основной код Streamlit
if 'df' not in st.session_state:
    st.session_state.df = df

# Интерфейс для редактирования данных
edited_df = st.experimental_data_editor(st.session_state.df)
if not edited_df.equals(st.session_state.df):
    save_to_history(edited_df)
    st.session_state.df = edited_df

# Кнопка для отмены изменений
if st.button('Undo (Ctrl+Z)'):
    st.session_state.df = undo_last_change()

st.write(st.session_state.df)

# JavaScript для отслеживания нажатий Ctrl+Z
undo_js = """
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'z') {
        document.querySelector('button[aria-label="Undo (Ctrl+Z)"]').click();
    }
});
"""
st.markdown(f"<script>{undo_js}</script>", unsafe_allow_html=True)
