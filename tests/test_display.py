"""Tests for the display module."""
import pytest
from psb import display


def test_image_display_no_file():
    """Test that a FileNotFoundError is raised when image does not exist.
    """
    test_display = display.EinkDisplay()
    with pytest.raises(FileNotFoundError):
        test_display.image(path='tests/resources/images', status='no-status')


def test_image_display():
    """Test to check that the _eink_display function is run, this does not check that the image was displayed.
    """
    test_display = display.EinkDisplay()
    with pytest.raises(RuntimeError):
        test_display.image(path='tests/resources/images', status='available')


def test_process_message_two_lines_under_20():
    """
    Test for a message with new lines each under 20 characters.
    Lines should return as two parts.
    """
    expected_return = ['Hello', 'There']
    test_display = display.EinkDisplay()
    message = "Hello\nThere"
    return_data = test_display.process_message(message)
    assert return_data == expected_return


def test_process_message_long_message():
    """Test for a long message to make sure it is processed properly.
    """
    expected_return = ['Hello There', 'Long Test Message To', 'Split']
    test_display = display.EinkDisplay()
    message = "Hello There\nLong Test Message To Split"
    return_data = test_display.process_message(message)
    print(return_data)
    assert return_data == expected_return
