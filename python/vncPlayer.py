import os
import sys
from vlc import *

VLC_ARGS = []

class Main:
    def end_callback(self, event):
        print('End of media stream (event %s)' % event.type)
        # sys.exit(0)

    echo_position = False
    def pos_callback(self, event, player):
        if self.echo_position:
            sys.stdout.write('\r%s to %.2f%% (%.2f%%)' % (event.type,
                                                          event.u.new_position * 100,
                                                          player.get_position() * 100))
            sys.stdout.flush()

    def print_version(self):
        """Print version of this vlc.py and of the libvlc"""
        try:
            print('Build date: %s (%#x)' % (build_date, hex_version()))
            print('LibVLC version: %s (%#x)' % (bytes_to_str(libvlc_get_version()), libvlc_hex_version()))
            print('LibVLC compiler: %s' % bytes_to_str(libvlc_get_compiler()))
            if plugin_path:
                print('Plugin path: %s' % plugin_path)
        except:
            print('Error: %s' % sys.exc_info()[1])

    def __init__(self):
        movie = os.path.expanduser(sys.argv.pop())
        if not os.access(movie, os.R_OK):
            print('Error: %s file not readable' % movie)
            sys.exit(1)

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
        self.event_manager.event_attach(EventType.MediaPlayerEndReached, self.end_callback)
        self.event_manager.event_attach(EventType.MediaPlayerPositionChanged, self.pos_callback, self.player)
        
    def set_media(self, filePath):
        media = self.instance.media_new(filePath)
        self.player.set_media(media)

    def play(self):
        self.player.play()

    def mspf(self):
        """Milliseconds per frame"""
        return int(1000 // (self.player.get_fps() or 25))

    def print_info(self):
        """Print information about the media"""
        try:
            print_version()
            media = player.get_media()
            print('State: %s' % player.get_state())
            print('Media: %s' % bytes_to_str(media.get_mrl()))
            print('Track: %s/%s' % (player.video_get_track(), player.video_get_track_count()))
            print('Current time: %s/%s' % (player.get_time(), media.get_duration()))
            print('Position: %s' % player.get_position())
            print('FPS: %s (%d ms)' % (player.get_fps(), mspf()))
            print('Rate: %s' % player.get_rate())
            print('Video size: %s' % str(player.video_get_size(0)))  # num=0
            print('Scale: %s' % player.video_get_scale())
            print('Aspect ratio: %s' % player.video_get_aspect_ratio())
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
