import PySimpleGUI as sg

layout = [[sg.Text('MQ008')],
          [sg.Button('On', size=(3,1), button_color=('white', 'green'), key='_MQ008ON_'), sg.Button('Off', size=(3,1), button_color=('white', 'red'), key='_MQ008OFF_')],
          [sg.Text('MQ158')],
          [sg.Button('On', size=(3,1), button_color=('white', 'green'), key='_MQ158ON_'), sg.Button('Off', size=(3,1), button_color=('white', 'red'), key='_MQ158OFF_')]
          ]

window = sg.Window('Window Title', layout)

down = True

while True:             # Event Loop
    event, values = window.Read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == '_MQ008ON_':
        print("MQ008 ON")

    elif event == '_MQ008OFF_':
        print("MQ008 OFF")

    elif event == '_MQ158ON_':
        print("MQ158 ON")

    elif event == '_MQ158OFF_':
        print("MQ158 OFF")

window.Close()
