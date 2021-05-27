import PySimpleGUI as sg
import pathlib
import time
import subprocess

sg.change_look_and_feel('DarkBlue12')

width = 30
height = 20
file = None


t = 0

# Makes a layout for the top menu bar on a Mac
menu_layout = [['File', ['New (Ctrl+N)', 'Open (Ctrl+O)', 'Save (Ctrl+S)', 'Save As', 'Exit']],
               ['Tools', ['Word Count']],
               ['Help', ['About']]]

# Creating a basic layout for the initial window
layout = [[sg.Menu(menu_layout)],
          [sg.Text('Notepad', font=('Consoles', 10), size=(width, 1), key='_INFO_')],
          [sg.Multiline(font=('Consoles', 12), size=(width, height), key='_BODY_')],
          [sg.Button('Alarm/Update')],
          [sg.Text('Alarm')],
          [sg.Text('Add Time')],
          [sg.Button('+1', key='+1', enable_events=True), sg.Button('+5', key='+5', enable_events=True)],
          [sg.Text(size=(30, 10), key='_TASK_')],
          [sg.Button('Set', key='Set', enable_events=True)]]

window = sg.Window('Notepad', layout=layout, margins=(0, 0), return_keyboard_events=True, finalize=True)
window['_BODY_'].expand(expand_x=True, expand_y=True)


def new_file():
    # Reset body and info bar, and clear filename variable
    window['_BODY_'].update(value='')
    window['_INFO_'].update(value='Notepad')
    file = None
    return file


def open_file():
    # Open file and update the infobar
    filename = sg.popup_get_file('Open', no_window=True)
    if filename:
        file = pathlib.Path(filename)
        window['_BODY_'].update(value=file.read_text())
        window['_INFO_'].update(value=file.absolute())
        return file


def save_file(file):
    # Save file instantly if already open; otherwise use `save-as` popup
    if file:
        file.write_text(values.get('_BODY_'))
    else:
        save_file_as()


def save_file_as():
    # Save new file or save existing file with another name
    filename = sg.popup_get_file('Save As', save_as=True, no_window=True)
    if filename:
        file = pathlib.Path(filename)
        file.write_text(values.get('_BODY_'))
        window['_INFO_'].update(value=file.absolute())
        return file


def word_count():
    # Display estimated word count
    words = [w for w in values['_BODY_'].split(' ') if w != '\n']
    word_count = len(words)
    sg.popup_no_wait('Word Count: {:,d}'.format(word_count))


def about_me():
    # This def statement sets a message to offer the user a brief idea of the programs core concepts
    sg.popup('Thank you for using Task Manager \n'
             '- This is a small program that allows you to make use of a mini notepad \n'
             '- That also doubles as a timer to help stay on task \n'
             '- Simple write your tasks within the notepad \n'
             '- Update Alarm and input your desired time \n'
             '- Please note it only works with numbers in minute format \n'
             '- When the time is up it will display a pop up and play an Alarm \n'
             '- If you wish to save or open a file please click file top left \n'
             '- Due to limitations remember that the menu works better on light mode \n'
             'Thank you for choosing Task Manager as your time management application.')

t=t
# While loop that runs the window and reads it
while True:
    event, values = window.read()
    if event in ('Exit', None):
        break
    if event in ('New (Ctrl+N)', 'n:78'):
        file = new_file()
    if event in ('Open (Ctrl+O)', 'o:79'):
        file = open_file()
    if event in ('Save (Ctrl+S)', 's:83'):
        save_file(file)
    if event in ('Save As',):
        file = save_file_as()
    if event in ('Word Count',):
        word_count()
    if event in ('About',):
        about_me()
    if event == 'Alarm/Update':
        window['_TASK_'].update(values['_BODY_'])
    if event == '+1':
        t = t + 1
    if event == '+5':
        t = t + 5
    if event == 'Set':
        while t > 0:
            for t in range(0, t*60):
                time.sleep(1)
            if t >= 0:
                subprocess.call(["afplay", "Alarm.mp3"])
                sg.popup('Alarm')
            break