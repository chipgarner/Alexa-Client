import Record

# def test_notbroken():
#     rec = Record.Record()
#     rec.record_to_file('LiveRecordings/latest.wav')

def test_ends_recording_if_silent_too_long():
    rec = Record.Record()
    rec.silent_chunks = 2
    max_silent_chunks = 2

    silent = True
    result = rec.continue_recording(silent, max_silent_chunks)

    assert result is False


def test_keeps_recording_if_silent_short_time():
    rec = Record.Record()
    rec.silent_chunks = 2
    max_silent_chunks = 3

    silent = True
    result = rec.continue_recording(silent, max_silent_chunks)

    assert result is True


def test_keeps_recording_if_sound():
    rec = Record.Record()
    rec.silent_chunks = 2
    max_silent_chunks = 30

    silent = False
    result = rec.continue_recording(silent, max_silent_chunks)

    assert result is True