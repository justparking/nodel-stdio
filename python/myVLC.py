import threading
import time
import nodel_stdio

@nodel_stdio.nodel_action({'group' : 'Power', 'title': 'Set power'})
def set_power(state):
    print '#SERVER Set power called! state=%s' % state

color_signal = nodel_stdio.create_nodel_event('Color')

@nodel_stdio.nodel_action({'group' : 'Colour'})
def set_color(state):
    color_signal.emit(state)
    print '#SERVER Set color called! state=%s' % state    

eof_signal = nodel_stdio.create_nodel_event('EOF', {'group': 'My group', 'schema': {'type': 'string'}})

def hello():
    while(True):
        color_signal.emit('Blue')
        time.sleep(1)

t = threading.Thread(target=hello)
t.start()

nodel_stdio.start_bridge()


