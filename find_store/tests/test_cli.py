""" Base Tests for find_store cli """

import json
import logging
import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from find_store import cli

expected_address = {
  "address1": "2675 Geary Blvd",
  "address2": "San Francisco, CA 94118-3400",
}

expected_json = {
  "address": [
      "2675 Geary Blvd",
      "San Francisco, CA 94118-3400"
  ],
  "data": [
      "San Francisco West",
      "SEC Geary Blvd. and Masonic Avenue",
      "2675 Geary Blvd",
      "San Francisco",
      "CA",
      "94118-3400",
      "37.7820964",
      "-122.4464697",
      "San Francisco County"
  ],
  "distance": 1.4808982343997603,
  "units": "mi"
}

class TestFindStore(unittest.TestCase):
  
  def verify_result_data(self, result_data, expected):
    """ verify_result_data """
    self.assertEquals(type(result_data["distance"]), float)
    self.assertEqual(result_data["units"], expected.get("units"))
    self.assertIsNotNone(result_data["data"])
    self.assertEquals(result_data["address"][0], expected.get("address1"))
    self.assertEquals(result_data["address"][1], expected.get("address2"))

  def verify_result_output(self, result_output, json_format=False, units="mi"):
    """ verify_result_output """
    if json_format:
      self.assertEqual(json.loads(result_output)["address"][0], expected_json["address"][0])
      self.assertEqual(json.loads(result_output)["address"][1], expected_json["address"][1])
    else:
      # Note: distance can vary slightly via zipcodes, verify address and units exist
      self.assertTrue(expected_address["address1"] in result_output)
      self.assertTrue(expected_address["address2"] in result_output)
      self.assertTrue(units in result_output)

  def test_cli_with_address(self):
    """ test_cli_with_address """
    sys.argv = [sys.argv[0], "--address=\"1770 Union St, San Francisco, CA 94123\""]
    result_data, result_output = cli.main()
    expected_data = expected_address
    expected_data.update({ "units": "mi" })
    self.verify_result_data(result_data, expected_data)
    self.verify_result_output(result_output)
  
  def test_cli_with_address_output_and_units(self):
    """ test_cli_with_address """
    sys.argv = [sys.argv[0]]
    sys.argv.append("--address=\"1770 Union St, San Francisco, CA 94123\"")
    sys.argv.append("--output=json")
    sys.argv.append("--units=km")
    result_data, result_output = cli.main()
    expected_data = expected_address
    expected_data.update({ "units": "km" })
    self.verify_result_data(result_data, expected_data)
    self.verify_result_output(result_output, json_format=True, units="km")

  def test_cli_with_zip(self):
    """ test_cli_with_address """
    sys.argv = [sys.argv[0]]
    sys.argv.append("--zip=94123")
    result_data, result_output = cli.main()
    expected_data = expected_address
    expected_data.update({ "units": "mi" })
    self.verify_result_data(result_data, expected_data)
    self.verify_result_output(result_output)

if __name__ == "__main__":
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "TestFindStore.test_cli" ).setLevel(logging.DEBUG)
    unittest.main()