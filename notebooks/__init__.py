"""Python code for Jupyter notebooks."""

__author__ = "Tom Goetz"
__copyright__ = "Copyright Tom Goetz"
__license__ = "GPL"

# flake8: noqa

try:
    from .jupyter_funcs import format_number
except Exception:
    def format_number(x):
        return x
