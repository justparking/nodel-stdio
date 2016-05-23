import os
import sys
from vlc import *
from nodel_stdio import *

VLC_ARGS = []

class Main:
    endReached = create_nodel_event('End Reached')
    def endReached_callback(self, event):
        self.endReached.emit()

    position = create_nodel_event('Position')
    def pos_callback(self, event, player):
        self.position.emit(event.u.new_position * 100)

    version = create_nodel_event('Version')
    def version(self):
        """Print version of this vlc.py and of the libvlc"""
        arg = {}
        try:
            arg['Build date'] = '%s (%#x)' % (build_date, hex_version())
            arg['LibVLC version'] = '%s (%#x)' % (bytes_to_str(libvlc_get_version()), libvlc_hex_version())
            arg['LibVLC compiler'] = '%s' % bytes_to_str(libvlc_get_compiler())
            if plugin_path:
                arg['Plugin path'] = '%s' % plugin_path

            emit_event('version', arg)
        except:
            print('Error: %s' % sys.exc_info()[1])

    def __init__(self):
        # movie = os.path.expanduser(sys.argv.pop())
        # if not os.access(movie, os.R_OK):
        #    print('Error: %s file not readable' % movie)
        #    sys.exit(1)

        # Need --sub-source=marq in order to use marquee below
        self.instance = Instance(["--sub-source=marq"] + VLC_ARGS)
        # try:
        #    media = instance.media_new(movie)
        # except (AttributeError, NameError) as e:
        #    print('%s: %s (%s %s vs LibVLC %s)' % (e.__class__.__name__, e,
        #                                           sys.argv[0], __version__,
        #                                           libvlc_get_version()))
        #    sys.exit(1)
        self.player = self.instance.media_player_new()

        # Some marquee examples.  Marquee requires '--sub-source marq' in the
        # Instance() call above, see <http://www.videolan.org/doc/play-howto/en/ch04.html>
        self.player.video_set_marquee_int(VideoMarqueeOption.Enable, 1)
        self.player.video_set_marquee_int(VideoMarqueeOption.Size, 24)  # pixels
        self.player.video_set_marquee_int(VideoMarqueeOption.Position, Position.Bottom)
        if False:  # only one marquee can be specified
            player.video_set_marquee_int(VideoMarqueeOption.Timeout, 5000)  # millisec, 0==forever
            t = media.get_mrl()  # movie
        else:  # update marquee text periodically
            self.player.video_set_marquee_int(VideoMarqueeOption.Timeout, 0)  # millisec, 0==forever
            self.player.video_set_marquee_int(VideoMarqueeOption.Refresh, 1000)  # millisec (or sec?)
            ##t = '$L / $D or $P at $T'
            t = '%Y-%m-%d  %H:%M:%S'
        self.player.video_set_marquee_string(VideoMarqueeOption.Text, str_to_bytes(t))

        # Some event manager examples.  Note, the callback can be any Python
        # callable and does not need to be decorated.  Optionally, specify
        # any number of positional and/or keyword arguments to be passed
        # to the callback (in addition to the first one, an Event instance).
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(EventType.MediaPlayerEndReached, self.endReached_callback)
        self.event_manager.event_attach(EventType.MediaPlayerPositionChanged, self.pos_callback, self.player)
        
    def set_media(self, filePath):
        media = self.instance.media_new(filePath)
        self.player.set_media(media)

    @nodel_action()
    def play(self):
        self.player.play()

    @nodel_action()
    def stop(self):
        self.player.stop()

    def mspf(self):
        """Milliseconds per frame"""
        return int(1000 // (self.player.get_fps() or 25))

    info = create_nodel_event('Info')
    def info(self):
        """Print information about the media"""
        try:
            self.version()
            media = player.get_media()

            arg = {'State': player.get_state(), 
                   'Media': bytes_to_str(media.get_mrl()), 
                   'Track': '%s/%s' % (player.video_get_track(), player.video_get_track_count()),
                   'Current time': '%s/%s' % (player.get_time(), media.get_duration()),
                   'Position': player.get_position(),
                   'FPS': '%s (%d ms)' % (player.get_fps(), mspf()),
                   'Rate': '%s' % player.get_rate(),
                   'Video size': '%s' % str(player.video_get_size(0)),  # num=0
                   'Scale': '%s' % player.video_get_scale(),
                   'Aspect ratio': '%s' % player.video_get_aspect_ratio()}
            info.emit(arg)
           #print('Window:' % player.get_hwnd()
        except Exception:
            print('Error: %s' % sys.exc_info()[1])

    def sec_forward(self):
        """Go forward one sec"""
        player.set_time(player.get_time() + 1000)

    def sec_backward(self):
        """Go backward one sec"""
        player.set_time(player.get_time() - 1000)

    def frame_forward(self):
        """Go forward one frame"""
        player.set_time(player.get_time() + mspf())

    def frame_backward(self):
        """Go backward one frame"""
        player.set_time(player.get_time() - mspf())

    def print_help(self):
        """Print help"""
        print('Single-character commands:')
        for k, m in sorted(keybindings.items()):
            m = (m.__doc__ or m.__name__).splitlines()[0]
            print('  %s: %s.' % (k, m.rstrip('.')))
        print('0-9: go to that fraction of the movie')

    def quit_app(self):
        """Stop and exit"""
        sys.exit(0)

    def toggle_echo_position(self):
        """Toggle echoing of media position"""
        self.echo_position = not self.echo_position

main = Main()

start_nodel_channel()


