"""Test the base class for Pipelines."""

import unittest
import mock

from arias.pipelines import base
from arias.unittests import testutil
from arias.common import constant

class TestBasePipeline(unittest.TestCase):
    """Test Case for the BasePipeline class."""

    def setUp(self):
        """Setup the mock objects for this test case."""
        self._spider = mock.MagicMock()
        self._base_pipeline = testutil.concreter(base.BasePipeline)()

    @mock.patch('uuid.uuid4')
    def _test_get_key(self, mock_uuid, id_key=None):
        """Test the `.get_key` method."""
        mock_item = {}
        if id_key:
            mock_item["id"] = id_key

        mock_uuid.return_value = "fack-uuid4"
        self._spider.name = "fack_spader_name"

        expected = constant.KEY_FORMAT.format(
            name=self._spider.name,
            id=id_key if id_key else mock_uuid())
        
        self.assertEqual(
            expected, self._base_pipeline.get_key(mock_item, self._spider))

    def test_get_key(self):
        """Test that `.get_key` uses the id when possible."""
        self._test_get_key(id_key="fake_key")

    def test_get_key_missing_key(self):
        """Test that `.get_key` work when the id is missing."""
        self._test_get_key(id_key=None)

    def test_get_namespace(self):
        """Test the `.get_key` method."""
        self._spider.name = "fack_spader_name"

        expected = constant.NAMESPACE_FORMAT.format(self._spider.name)
        
        self.assertEqual(
            expected, self._base_pipeline.get_namespace(self._spider))

    def test_abclass(self):
        """Test that the `BasePipeline` is an abstractclass"""
        self.assertRaises(TypeError, base.BasePipeline)

    def test_abclass_dict(self):
        """Test that the `BasePipeline` is an abstractclass"""
        self.assertTrue(
            "__abstractmethods__" in base.BasePipeline.__dict__)

