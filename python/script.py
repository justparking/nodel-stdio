'''Simple single instance Nodel channel using stdio.'''

# (NOTE, the '-u' flag (unbuffered) is important)
command = ['C:\\Python27\\python.exe', '-u', 'myVLC.py']


def handle_stdout(line):
  print '(got line %s)' % line
  
  json_message = line.strip()
  if json_message.startswith('#'):
    # ignore comments
    return
  
  if not json_message.startswith('{'):
    return
  
  message = json_decode(json_message)
  handle_message(message)


def handle_message(message):
  # lazily examine arguments (events most likely)
  
  event = message.get('event')
  if event:
      handle_event(event, message.get('arg'))
      return
  
  
  # next is metadata
  actions = message.get('actions')
  metadata = message.get('metadata')
  events = message.get('events')
  
  if actions:
    process_actions_reflection(actions, metadata)
    
  elif events:
    process_events_reflection(events, metadata)
    
  # (reserved for future processing)


def process_actions_reflection(actions, metadata):
  for i in range(len(actions)):
    process_action_reflection(actions[i], metadata[i])
    
def process_action_reflection(name, metadata):
  def handler(arg):
    message_json = json_encode({'action': name, 'arg': arg})
    print 'sending %s' % message_json
    process.sendNow(message_json)
    
  Action(name, handler, metadata)

  
def process_events_reflection(events, metadata):
  for i in range(len(events)):
    process_event_reflection(events[i], metadata[i])
  
def process_event_reflection(name, metadata):
  Event(name, metadata)
  
def handle_event(name, arg):
  event = lookup_local_event(name)
  if event:
    event.emit(arg)

    
    
process = Process(command,
                  started=lambda: console.info('Process started'),
                  stdout=handle_stdout,
                  stdin=None,
                  stderr=lambda data: console.info('got stderr "%s"' % arg), # stderr handler
                  stopped=lambda exitCode: console.info('Process stopped (exit code %s)' % exitCode), # when the process is stops / stopped
                  timeout=lambda: console.warn('Request timeout'))  

def main(arg = None):
  print 'Nodel script started.'

