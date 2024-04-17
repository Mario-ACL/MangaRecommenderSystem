import PySimpleGUI as sg
from libraryAI import (
    load_data,
    preprocess_data,
    get_encoded_data,
    concatenate_features,
    convert_to_sparse_matrix,
    calculate_similarity_matrix_with_progress,
    get_recommendations,
)

# Configurar el diseño de la interfaz de usuario
layout = [
    [sg.Text('Ingrese un título de manga:'), sg.InputText(key='manga_title')],
    [sg.Button('Crear recomendaciones')],
    [sg.Text('Manga recomendado:'), sg.Listbox(values=[], size=(50, 10), key='recommendations')],
    [sg.Text('Pre-proceso de datos:'), sg.ProgressBar(bar_color='green on white', max_value=100, orientation='h',
                                                      size=(20, 20), key='progress_data')],
    [sg.Text('Similitud de Cosenos:'), sg.ProgressBar(bar_color='green on white', max_value=100, orientation='h',
                                                      size=(20, 20), key='progress')],
]

# Crear la ventana
window = sg.Window('Recomendaciones de Manga', layout)

# Loop principal para manejar eventos
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Crear recomendaciones':
        manga_title = values['manga_title']
        if manga_title:
            # Restablece la barra de progreso
            window['progress_data'].update(0)
            window['progress'].update(0)

            # Llamar a las funciones de libraryAI y pasar la barra de progreso
            df, titles = load_data(window['progress_data'])
            df = preprocess_data(df, window['progress_data'])
            genres_encoded, themes_encoded, demographics_encoded = get_encoded_data(df, window['progress_data'])
            features = concatenate_features(genres_encoded, themes_encoded, demographics_encoded, window['progress_data'])
            sparse_features = convert_to_sparse_matrix(features, window['progress_data'])
            similarity_matrix = calculate_similarity_matrix_with_progress(sparse_features, window['progress'])

            # Obtener recomendaciones
            recommendations = get_recommendations(manga_title, similarity_matrix, titles)

            # Actualiza la lista de recomendaciones en la interfaz de usuario
            window['recommendations'].update(recommendations)

# Cerrar la ventana
window.close()
