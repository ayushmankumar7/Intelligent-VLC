
from pynput import keyboard


def on_press(key):
    print('Key {} pressed.'.format(key))


def on_release(key):
    print('Key {} released.'.format(key))
    if str(key) == 'Key.esc':
        print('Exiting...')
        return False


with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
