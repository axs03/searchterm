"""
searchterm - simple command-line AI question-answering model
"""
from .config_loader import ConfigLoader

__version__ = ConfigLoader().configvalues["VERSION"]
__author__ = "axs03"