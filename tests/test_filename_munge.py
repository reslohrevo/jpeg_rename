import os
import re
import sys
import pytest
from mock import Mock, patch
app_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_path + '/../')

from photo_rename import *
from stubs import *


class TestGetBase():
    """
    Tests for method get_base() are in this class.
    """
    @pytest.mark.skipif(RUN_TEST, reason="Work in progress")
    def test_get_base_none(self):
        """
        Test case where no base is matched.
        """
        exif_data = EXIF_DATA_VALID['exif_data']
        filemap = FileMap(OLD_FN_JPG_LOWER, IMAGE_TYPE_JPEG,
                avoid_collisions=True, metadata=exif_data)
        res = filemap.get_base("")
        assert res == None

class TestGetExtension():
    """
    Tests for method get_extension() are in this class.
    """
    @pytest.mark.skipif(RUN_TEST, reason="Work in progress")
    def test_get_base_none(self):
        """
        Test case where no extension is matched.
        """
        exif_data = EXIF_DATA_VALID['exif_data']
        filemap = FileMap(OLD_FN_JPG_LOWER, IMAGE_TYPE_JPEG,
                avoid_collisions=True, metadata=exif_data)
        res = filemap.get_extension("")
        assert res == None

