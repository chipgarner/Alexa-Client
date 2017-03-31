
from alexa_client import AlexaClient
import vlc
import os
import time
import Record

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
ask_input = '{}/AlexaAsk/fall.wav'.format(LOCAL_PATH)
live_input = '{}/LiveRecordings/latest.wav'.format(LOCAL_PATH)


def play_mp3_file(file_path):
    p = vlc.MediaPlayer(file_path)
    p.play()
    st = p.get_state()
    not_infinite = time.time()
    while st != vlc.State.Ended:  # This works but shows a warning on program exit
        st = p.get_state()
        time.sleep(0.01)
        if time.time() - not_infinite > 10:
            break


def main():
    alexa = AlexaClient()
    input = ask_input
    save_to = 'AlexaOut/test_ask.mp3'
    alexa.ask(input, save_to=save_to)
    print("Response saved to {}".format(save_to))

    play_mp3_file(save_to)

    print('Begin recording')
    Record.record_to_file('LiveRecordings/latest.wav')
    print('Recorded if synchronous')

    input = live_input
    save_to = 'AlexaOut/test_ask2.mp3'
    alexa.ask(input, save_to=save_to)
    print("Response saved to {}".format(save_to))

    play_mp3_file(save_to)

if __name__ == '__main__':
    main()
