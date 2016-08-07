# Raspberry Pi Cat Laser 2.0 - Cloud Laser Server Players
# This players class encapsulates the majority of the game logic.  It allows
# players to be added and removed from a waiting list (based on their IP address),
# and will allow the top of the list to become the active player.  Each active
# player has a limited amount of time to play and then they are removed and the
# next waiting player is made active.  It's expected the code that creates and
# users the players class will continually call its updated method to move the
# game logic along.
# Author: Tony DiCola
import collections
import threading


class Players(object):
    """Class to represent the main game logic and player state.  Allows Players
    to connect and disconnect and keeps an ordered list of them (identified by
    their IP) so they can wait in line for a chance to play (i.e. become the
    active player).
    """

    def __init__(self, playtime_seconds):
        """Initialize the players list with the specified amount of play time
        for any active player.
        """
        self._players = collections.OrderedDict()
        self._lock = threading.Lock()
        self._active = None
        self._playtime = playtime_seconds

    def _is_active(self, ip):
        """Check if the specified player is active (i.e. currently playing).
        """
        return self._active is not None and self._active['ip'] == ip

    def add_player(self, ip):
        """Add a player (identified by IP address) to the waiting list.  Will
        ensure each player is only in the waiting list once (i.e. calling multiple
        times for the same IP will not add multiple entries).
        """
        with self._lock:
            if self._is_active(ip):
                # If the player is currently active then just increment their
                # session count.
                self._active['sessions'] += 1
            else:
                # If the player isn't active then increment their session count
                # in the player waiting list (adding them if necessary).
                self._players[ip] = self._players.get(ip, 0) + 1

    def remove_player(self, ip):
        """Remove the specified player (identified by IP address) from the waiting
        list.  If the player has multiple sessions with the same IP then they
        will only be removed once all their sessions have been removed.
        """
        with self._lock:
            if self._is_active(ip):
                # If the player is currently active decrement their session
                # count and remove them from active play if no sessions are still
                # connected.
                self._active['sessions'] -= 1
                if self._active['sessions'] <= 0:
                    self._active = None
            else:
                # If the player isn't active then decrement their session count
                # and remove them from the player waiting list when no sessions
                # are left.
                if ip in self._players:
                    self._players[ip] -= 1
                    if self._players[ip] <= 0:
                        del self._players[ip]

    def enumerate_players(self):
        """Enumerate all the waiting players.  Returns an ordered list of all the
        player IP addresses waiting to play.
        """
        with self._lock:
            return self._players.keys()

    def update(self, elapsed_seconds, start_active, end_active):
        """Update the active player state.  Allows the active player to be
        active for a period of time, after which they are removed and the next
        waiting player is made active.  Will fire callbacks when appropriate for
        user code to take these actions:
          - start_active(ip): called when a player becomes active and will be
            passed the IP address of the now active player.
          - stop_active(ip): called when a player stops being active and will
            be passed the IP address of the now inactive player.
        """
        # Keep track of an ending player IP and starting player IP so the
        # callbacks can be fired outside the lock (don't fire inside lock
        # because the callbacks might call back into player and try to take
        # the lock again--deadlock!).
        end_ip = None
        start_ip = None
        with self._lock:
            # First check if there is an active player and test if their playtime
            # has elapsed.
            if self._active is not None:
                self._active['remaining'] -= elapsed_seconds
                if self._active['remaining'] <= 0.0:
                    # Active player has finished playing, remember their IP so
                    # the end active callback can be fired outside the lock.
                    end_ip = self._active['ip']
                    self._active = None
            # Now check if there isn't an active player and select the next
            # waiting one.  The ordered dictionary is great because it remembers
            # the order of players so we just need to pop off the first player
            # who will always be the oldest/next in line.
            if self._active is None and len(self._players) > 0:
                ip, sessions = self._players.popitem(last=False)  # last = False means FIFO, first in first out.
                self._active = {'ip': ip, 'sessions': sessions, 'remaining': self._playtime}
                # Remember the new active player IP so the start_active callback
                # can fire outside the lock.
                start_ip = ip
        # Now outside the lock fire any start and end callbacks.  Do this outside
        # the lock because these callbacks might call back into Players class
        # functions that try to take the lock again and would deadlock!
        if end_ip is not None:
            end_active(end_ip)
        if start_ip is not None:
            start_active(start_ip)

    def active_player(self):
        """Return the active player IP and their remaining playtime (in seconds)
        as a tuple.  If no player is active then None is returned.
        """
        with self._lock:
            if self._active is None:
                return None
            else:
                return (self._active['ip'], self._active['remaining'])

    def wait_position(self, ip):
        """Return the current position in line for the provided player IP.  If
        the player is actively playing or not waiting in line then None is
        returned.
        """
        with self._lock:
            if ip not in self._players:
                return None
            else:
                return list(self._players.keys()).index(ip)
