"""This test will send a pre-generated audio file in the `AlexaAks` directory
to AVS, and saves it as `/AlexaOut/test1.mp3`, and then play the mp3 file."""
from alexa_client import AlexaClient
import vlc
import os
import time

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
ask_input = '{}/AlexaAsk/fall.wav'.format(LOCAL_PATH)


def play_mp3_file(file_path):
    p = vlc.MediaPlayer(file_path)
    p.play()
    st = p.get_state()
    not_infinite = time.time()
    while st != vlc.State.Ended and st != vlc.State.Error:  # This works but shows a warning on program exit
        st = p.get_state()
        time.sleep(0.01)
        if time.time() - not_infinite > 30:
            break


def main():
    alexa = AlexaClient()
    input = ask_input
    save_to = 'AlexaOut/test_ask.mp3'
    alexa.ask(input, save_to=save_to)
    print("Response saved to {}".format(save_to))

    play_mp3_file(save_to)

if __name__ == '__main__':
    main()
