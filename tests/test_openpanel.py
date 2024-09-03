import time
import unittest
from openpanel import OpenPanel

class TestOpenPanel(unittest.TestCase):

    def setUp(self):
        self.client_id = "CLIENT_ID"
        self.client_secret = "CLIENT_SECRET"
        self.openpanel = OpenPanel(client_id=self.client_id, client_secret=self.client_secret)

    def test_sdk_methods(self):
        # Test track
        event_name = "Test Event"
        event_properties = {"key": "value"}
        self.openpanel.track(event_name, event_properties)

        time.sleep(3)

        # Test track with profile id
        self.openpanel.profile_id = "test_profile_id"
        self.openpanel.track(event_name, event_properties)
        time.sleep(3)

        # Test track with global properties
        self.openpanel.set_global_properties({"global_key": "global_value"})
        self.openpanel.track(event_name, event_properties)
        time.sleep(3)

        # Test track disabled
        self.openpanel.disabled = True
        self.openpanel.track(event_name, event_properties)
        time.sleep(3)

        # Test track filtered
        def filter_function(payload):
            return payload["payload"]["name"] != "Filtered Event"
        self.openpanel.filter = filter_function
        self.openpanel.track("Filtered Event", {"key": "value"})
        self.openpanel.track("Not Filtered Event", {"key": "value"})
        time.sleep(3)

        # Test identify
        self.openpanel.identify("test_profile_id", {"trait_key": "trait_value"})
        time.sleep(3)

        # Test alias
        self.openpanel.alias("test_profile_id", "test_alias")
        time.sleep(3)

        # Test increment
        self.openpanel.increment("test_profile_id", "test_property", 1)
        time.sleep(3)

        # Test decrement
        self.openpanel.decrement("test_profile_id", "test_property", 1)
        time.sleep(3)

        # Test increment
        self.openpanel.increment("test_profile_id", "test_property", 1)

        # Test clear
        time.sleep(3)

if __name__ == '__main__':
    unittest.main()