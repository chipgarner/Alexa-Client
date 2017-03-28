"""This test will send a pre-generated audio file in the `tests` directory
to AVS, and saves it as `/tmp/test1.mp3`."""
from alexa_client import AlexaClient
import vlc
import os

TESTS_PATH = os.path.dirname(os.path.realpath(__file__))


def main():
    alexa = AlexaClient()
    input = '{}/sftides.wav'.format(TESTS_PATH)
    save_to = 'out/test_ask.mp3'
    alexa.ask(input, save_to=save_to)
    print("Response saved to {}".format(save_to))
    p = vlc.MediaPlayer(save_to)
    p.play()
    while True:
        pass

if __name__ == '__main__':
    main()
