__author__ = 'ajb'

import sys
import os

roboplexx_parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
sys.path.append(roboplexx_parent_dir)

import unittest

class TestCase(unittest.TestCase):

    def test_loading_demobot_from_properties(self):
        from roboplexx import loadouts

        prop_file_location = os.path.join(roboplexx_parent_dir, "roboplexx/loadout_configs/demobot.properties")
        demo_bot = loadouts.load_from_property_file(prop_file_location)

        self.assertIsNotNone(demo_bot)
        self.assertIsNotNone(demo_bot.host)
        self.assertEqual("demobot", demo_bot.host.host_id)

        self.assertIsNotNone(demo_bot.left_mc)
        self.assertIsNotNone(demo_bot.right_mc)
        self.assertIsNotNone(demo_bot.diff_drive)
        self.assertIsNotNone(demo_bot.camera)
        self.assertEqual("abc", demo_bot.left_mc.connection_string)
        self.assertEqual("xyz", demo_bot.right_mc.connection_string)
        self.assertIsNotNone(demo_bot.diff_drive.left_mc)
        self.assertIsNotNone(demo_bot.diff_drive.right_mc)
        self.assertEqual("abc", demo_bot.diff_drive.left_mc.connection_string)
        self.assertEqual("xyz", demo_bot.diff_drive.right_mc.connection_string)


    def test_saving_demobot_as_properties_file(self):
        import tempfile
        import roboplexx
        from roboplexx import loadouts

        demo_bot = roboplexx.loadouts.get_new_demo_bot()

        # create a temporary file using a context manager
        with tempfile.NamedTemporaryFile() as tf:
            tf.close()

            loadouts.save_to_property_file(demo_bot, tf.name)
            demo_bot = loadouts.load_from_property_file(tf.name)

            self.assertIsNotNone(demo_bot)
            self.assertIsNotNone(demo_bot.host)
            self.assertEqual("RpxHostDriver", demo_bot.host.__class__.__name__)
            self.assertEqual("demobot", demo_bot.host.host_id)
            self.assertEqual(True, demo_bot.host.web_app_enabled)

            self.assertIsNotNone(demo_bot.left_mc)
            self.assertIsNotNone(demo_bot.right_mc)
            self.assertIsNotNone(demo_bot.diff_drive)
            self.assertIsNotNone(demo_bot.camera)
            self.assertEqual("abc", demo_bot.left_mc.connection_string)
            self.assertEqual("xyz", demo_bot.right_mc.connection_string)
            self.assertIsNotNone(demo_bot.diff_drive.left_mc)
            self.assertIsNotNone(demo_bot.diff_drive.right_mc)
            self.assertEqual("abc", demo_bot.diff_drive.left_mc.connection_string)
            self.assertEqual("xyz", demo_bot.diff_drive.right_mc.connection_string)

            # with open(tf.name) as f:
            #     for l in f.readlines():
            #         print l





if __name__ == "__main__":
    unittest.main()
