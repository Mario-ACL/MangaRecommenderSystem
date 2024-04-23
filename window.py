import PySimpleGUI as sg
from libraryAI import (
    full_calc,
    quick_calc,
)

# Configurar el diseño de la interfaz de usuario
layout = [
    [sg.Text('Ingrese un título de manga:'), sg.InputText(key='manga_title')],
    [sg.Button('Crear recomendaciones')],
    [sg.Text('Recomendaciones de Manga:')],

]

# Add a row for each recommendation
for i in range(1):
    layout.append([
        sg.Text(f"Titulo: ", size=(50, 1)),
        sg.Text(f"Puntaje: ", size=(10, 1)),
        sg.Text(f"Generos: ", size=(50, 1)),
        sg.Text(f"Temas: ", size=(40, 1)),
        sg.Text(f"Demografia: ", size=(25, 1)),
        sg.Text(f"Similaridad: ", size=(10, 1)),
    ])
for i in range(6):
    layout.append([
        sg.Text(f"", size=(50, 1), key=f'title_text_{i}'),
        sg.Text(f"", size=(10, 1), key=f'score_text_{i}'),
        sg.Text(f"", size=(50, 1), key=f'genres_text_{i}'),
        sg.Text(f"", size=(40, 1), key=f'themes_text_{i}'),
        sg.Text(f"", size=(25, 1), key=f'demographics_text_{i}'),
        sg.Text(f"", size=(5, 1), key=f'similarity_{i}'),
    ])

layout += [
    [sg.Text('')],
    [sg.Text('Pre-proceso de datos:'), sg.ProgressBar(bar_color='green on white', max_value=100, orientation='h',
                                                      size=(20, 20), key='progress_data')],
    [sg.Text('Similitud de Cosenos:'), sg.ProgressBar(bar_color='green on white', max_value=100, orientation='h',
                                                      size=(20, 20), key='progress')],
]

# Crear la ventana
window = sg.Window('Recomendaciones de Manga', layout)

# Loop principal para manejar eventos
recommendations_with_details = None
similarity_matrix = None
titles = None
df = None
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Crear recomendaciones':
        manga_title = values['manga_title'].lower()
        if manga_title:

            if recommendations_with_details is None:
                # Restablece la barra de progreso
                window['progress_data'].update(0)
                window['progress'].update(0)
                # Obtener recomendaciones con detalles
                recommendations_with_details, similarity_matrix, titles, df = full_calc(manga_title,
                                                                                        window['progress_data'],
                                                                                        window['progress'])
            else:
                recommendations_with_details = quick_calc(manga_title, similarity_matrix, titles, df)

            if recommendations_with_details is []:
                window[f'title_text_{1}'].update('Manga no encontrado')
                continue

            # Clear previous recommendation details
            for i in range(6):
                window[f'title_text_{i}'].update('')
                window[f'score_text_{i}'].update('')
                window[f'genres_text_{i}'].update('')
                window[f'themes_text_{i}'].update('')
                window[f'demographics_text_{i}'].update(''),
                window[f'similarity_{i}'].update('')

            # Update recommendation details
            for i, manga in enumerate(recommendations_with_details):
                window[f'title_text_{i}'].update(f"{manga['Title'].title()}")
                window[f'score_text_{i}'].update(f"{round(manga['Score'], 2)}")
                window[f'genres_text_{i}'].update(f"{', '.join(manga['Genres'])}")
                window[f'themes_text_{i}'].update(f"{', '.join(manga['Themes'])}")
                window[f'demographics_text_{i}'].update(f"{', '.join(manga['Demographics'])}"),
                window[f'similarity_{i}'].update(f"%{round(manga['Similarity'] * 100, 2)}")

# Cerrar la ventana
window.close()
