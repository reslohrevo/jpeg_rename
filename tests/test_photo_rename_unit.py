import os
import sys
import pytest
from mock import Mock, patch
app_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_path + '/../')

from photo_rename import *
from stubs import *


class TestReadExifData():
    """Tests for method read_exif_data() are in this class."""
    @pytest.mark.skipif(RUN_TEST, reason="Work in progress")
    @patch.object(pyexiv2, 'ImageMetadata')
    def test_read_exif_data(self, mock_img_md):
        """Tests read_exif_data() with valid EXIF data. Tests for normal
        operation. Verify expected EXIF data in instantiated object."""

        class StubExifTag(object):
            raw_value = EXIF_DATA_VALID['exif_data']['Exif.Image.DateTime']

        class TestImage(object):
            """
            ImageMetadata test stub.
            """
            def __getitem__(self, key):
                return StubExifTag()

            def read(self):
                return EXIF_DATA_VALID['exif_data']

            @property
            def exif_keys(self):
                return ['Exif.Image.DateTime']


        old_fn = OLD_FN_JPG_LOWER
        mock_img_md.return_value = TestImage()
        filemap = FileMap(old_fn, IMAGE_TYPE_JPEG)
        assert filemap.metadata == EXIF_DATA_VALID['exif_data']

    @pytest.mark.skipif(RUN_TEST, reason="Work in progress")
    @patch.object(pyexiv2, 'ImageMetadata')
    def test_read_exif_data_info_none(self, mock_img_md):
        """
        Tests read_exif_data() with no EXIF data available. Tests for raised
        Exception. Verify expected exception message.
        """

        class TestImage(object):
            """
            ImageMetadata test stub.
            """
            def read(self):
                return None

            @property
            def exif_keys(self):
                return []

        old_fn = OLD_FN_JPG_LOWER
        mock_img_md.return_value = TestImage()
        with pytest.raises(Exception) as excinfo:
            filemap = FileMap(old_fn, IMAGE_TYPE_JPEG)
        assert str(excinfo.value) == "{0} has no EXIF data.".format(old_fn)


class TestMove():
    """
    Test for method move() are in this class.
    """
    @pytest.mark.skipif(RUN_TEST, reason="Work in progress")
    @pytest.mark.parametrize("old_fn", [
        OLD_FN_JPG_LOWER, OLD_FN_JPG_UPPER])
    @patch('photo_rename.FileMap.make_new_fn_unique')
    @patch('photo_rename.os.rename')
    def test_move_orthodox(self, mock_os, mock_fn_unique, old_fn):
        """
        Rename file with mocked os.rename. Verify called with args.
        """
        mock_fn_unique.return_value = None
        exif_data = EXIF_DATA_NOT_VALID
        filemap = FileMap(old_fn, IMAGE_TYPE_JPEG,
                avoid_collisions=None, metadata=exif_data)
        new_fn = filemap.new_fn
        filemap.move()
        if old_fn == new_fn:
            mock_os.assert_not_called()
        else:
            mock_os.assert_called_with(old_fn, new_fn)

    @pytest.mark.skipif(RUN_TEST, reason="Work in progress")
    @patch('photo_rename.FileMap.make_new_fn_unique')
    @patch('photo_rename.os.rename')
    def test_move_orthodox_rename_raises_exeption(self, mock_os,
            mock_fn_unique):
        """
        Rename file with mocked os.rename. Verify called with args.
        """
        mock_fn_unique.return_value = None
        mock_os.side_effect = OSError((1, "Just testing.",))
        old_fn = OLD_FN_JPG_UPPER
        exif_data = EXIF_DATA_NOT_VALID
        filemap = FileMap(old_fn, IMAGE_TYPE_JPEG,
                avoid_collisions=None, metadata=exif_data)
        new_fn = filemap.new_fn
        filemap.move()
        mock_os.assert_called_with(old_fn, new_fn)

    @pytest.mark.skipif(RUN_TEST, reason="Work in progress")
    @patch('photo_rename.FileMap.make_new_fn_unique')
    @patch('photo_rename.os.rename')
    def test_move_orthodox_fn_unique_raises_exception(self, mock_os,
            mock_fn_unique):
        """
        Rename file with mocked os.rename. Verify called with args.
        """
        mock_fn_unique.side_effect = OSError((1, "Just testing.",))
        old_fn = OLD_FN_JPG_LOWER
        exif_data = EXIF_DATA_NOT_VALID
        filemap = FileMap(old_fn, IMAGE_TYPE_JPEG,
                avoid_collisions=None, metadata=exif_data)
        new_fn = filemap.new_fn
        with pytest.raises(OSError):
            filemap.move()

    @pytest.mark.skipif(RUN_TEST, reason="Work in progress")
    @patch('photo_rename.FileMap.make_new_fn_unique')
    @patch('photo_rename.os.path.exists')
    def test_move_collision_detected(self, mock_exists, mock_fn_unique):
        """Move file with collision_detected simulating avoid_collisions=False.
        """
        mock_fn_unique.return_value = None
        mock_exists.return_value = True
        old_fn = OLD_FN_JPG_LOWER
        exif_data = {}
        filemap = FileMap(old_fn, IMAGE_TYPE_JPEG,
                avoid_collisions=None, metadata=exif_data)
        filemap.collision_detected = True
        new_fn = filemap.new_fn
        filemap.move()
        assert new_fn == old_fn

