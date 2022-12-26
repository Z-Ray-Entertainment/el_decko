import threading

from StreamDeck.DeviceManager import DeviceManager

stream_decks = DeviceManager().enumerate()
backends = None
action_map = {}


def initialize(edbs):
    global backends
    backends = edbs
    for index, deck in enumerate(stream_decks):
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        set_brightness(deck, 30)
        deck.set_key_callback(__key_change_callback)

        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass


# Returns a list of all available Stream Decks
def get_stream_decks():
    return stream_decks


def set_brightness(deck, brightness: int):
    deck.set_brightness(brightness)


def __key_change_callback(deck, key, state):
    print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)
    init_backend = backends['init'].load()
    init_backend()
    fire = backends['fire'].load()
    fire("SwitchScene", {"name": "S: Gaming"})