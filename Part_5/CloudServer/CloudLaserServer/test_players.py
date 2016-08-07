# Raspberry Pi Cat Laser 2.0 - Cloud Laser Server Players Tests
# Unit tests for the Players class.  Ensures basic functionality and scenarios
# like multiple users in line will work as expected.
# Author: Tony DiCola
import unittest
import unittest.mock

import players


class TestPlayers(unittest.TestCase):

    def test_add_players_wait_in_order(self):
        # Setup, add some players to waiting list.
        laser_players = players.Players(1)
        laser_players.add_player('192.168.0.1')
        laser_players.add_player('192.168.0.2')
        laser_players.add_player('192.168.0.3')
        # Verify users are in expected order.
        self.assertEqual(0, laser_players.wait_position('192.168.0.1'))
        self.assertEqual(1, laser_players.wait_position('192.168.0.2'))
        self.assertEqual(2, laser_players.wait_position('192.168.0.3'))

    def test_add_players_same_ip_are_combined(self):
        # Setup, add some players to waiting list (including a duplicate).
        laser_players = players.Players(1)
        laser_players.add_player('192.168.0.1')
        laser_players.add_player('192.168.0.1')
        laser_players.add_player('192.168.0.2')
        # Verify users are in expected order.
        self.assertEqual(0, laser_players.wait_position('192.168.0.1'))
        self.assertEqual(1, laser_players.wait_position('192.168.0.2'))

    def test_remove_players_adjusts_order(self):
        # Setup, add some players to waiting list.
        laser_players = players.Players(1)
        laser_players.add_player('192.168.0.1')
        laser_players.add_player('192.168.0.2')
        laser_players.add_player('192.168.0.3')
        # Remove middle player, verify expected waiting list order.
        laser_players.remove_player('192.168.0.2')
        self.assertEqual(0, laser_players.wait_position('192.168.0.1'))
        self.assertEqual(1, laser_players.wait_position('192.168.0.3'))
        self.assertEqual(None, laser_players.wait_position('192.168.0.2'))

    def test_enumerate_players(self):
        # Setup, add some players to waiting list.
        laser_players = players.Players(1)
        laser_players.add_player('192.168.0.1')
        laser_players.add_player('192.168.0.2')
        laser_players.add_player('192.168.0.3')
        # Enumerate players and expect them in the order added.
        waiting = list(laser_players.enumerate_players())
        self.assertListEqual(['192.168.0.1', '192.168.0.2', '192.168.0.3'], waiting)

    def test_update_no_active_player_makes_next_active(self):
        # Setup, add some players to waiting list.
        laser_players = players.Players(1)
        laser_players.add_player('192.168.0.1')
        # Check none are yet active.
        self.assertEqual(None, laser_players.active_player())
        # Setup, create mock callbacks that will remember how they were called.
        start_active = unittest.mock.Mock()
        end_active = unittest.mock.Mock()
        # Call update with 1 second of time elapsed.
        laser_players.update(0.5, start_active, end_active)
        # Check start active was called with the first in line IP, and that the
        # currently active player is the first one added (with 1 second of playtime
        # left).
        start_active.assert_called_once_with('192.168.0.1')
        end_active.assert_not_called()
        self.assertEqual(('192.168.0.1', 1), laser_players.active_player())

    def test_update_decreases_playtime(self):
        # Setup, add a player and make them active.
        laser_players = players.Players(1)
        laser_players.add_player('192.168.0.1')
        start_active = unittest.mock.Mock()
        end_active = unittest.mock.Mock()
        laser_players.update(1, start_active, end_active)
        # Update with half second of time, then check current player is active
        # with half seconf of time left.
        laser_players.update(0.5, start_active, end_active)
        self.assertEqual(('192.168.0.1', 0.5), laser_players.active_player())

    def test_update_moves_to_next_after_playetime_elapsed(self):
        # Setup, add two players and make the first active.
        laser_players = players.Players(1)
        laser_players.add_player('192.168.0.1')
        laser_players.add_player('192.168.0.2')
        start_active = unittest.mock.Mock()
        end_active = unittest.mock.Mock()
        laser_players.update(1, start_active, end_active)
        start_active.reset_mock()
        end_active.reset_mock()
        # Update with two seconds of time so the first player time is up, then
        # check next player is active.
        laser_players.update(2, start_active, end_active)
        end_active.assert_called_once_with('192.168.0.1')
        start_active.assert_called_once_with('192.168.0.2')
        self.assertEqual(('192.168.0.2', 1), laser_players.active_player())
