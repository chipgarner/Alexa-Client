"""This test will send a pre-generated audio file in the `tests` directory
to AVS, and saves it as `/tmp/test1.mp3`."""
from alexa_client import AlexaClient
import vlc
import os
import time

TESTS_PATH = os.path.dirname(os.path.realpath(__file__))


def play_mp3_file(file_path):
    p = vlc.MediaPlayer(file_path)
    p.play()
    st = p.get_state()
    while st != vlc.State.Ended:  # This works but shows a warning on program exit
        st = p.get_state()
        time.sleep(0.01)


def main():
    alexa = AlexaClient()
    input = '{}/sfweather.wav'.format(TESTS_PATH)
    save_to = 'out/test_ask.mp3'
    alexa.ask(input, save_to=save_to)
    print("Response saved to {}".format(save_to))

    play_mp3_file(save_to)

if __name__ == '__main__':
    main()
