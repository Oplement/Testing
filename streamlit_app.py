import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

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

# Функция для сохранения истории изменений
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

# Настройка таблицы
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gb.configure_default_column(editable=True)
gb.configure_grid_options(onCellValueChanged=JsCode("""
function(e) {
    if (window.historyStack === undefined) {
        window.historyStack = [];
    }
    window.historyStack.push(e.data);
}
"""))
gridOptions = gb.build()

# Создание таблицы
response = AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    update_mode='MODEL_CHANGED',
    allow_unsafe_jscode=True,
)

# Обработка нажатия Ctrl+Z с помощью JavaScript
undo_js = """
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'z') {
        const grid = window.gridOptions.api;
        const historyStack = window.historyStack || [];
        if (historyStack.length > 0) {
            const lastState = historyStack.pop();
            grid.applyTransaction({ update: [lastState] });
        }
    }
});
"""

st.markdown(f"<script>{undo_js}</script>", unsafe_allow_html=True)

# Обновление данных
if response['data'] is not None:
    edited_df = pd.DataFrame(response['data'])
    if not edited_df.equals(df):
        save_to_history(edited_df)
        df = edited_df

st.write(df)
