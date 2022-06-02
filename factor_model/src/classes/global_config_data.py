#!/usr/bin/env python3
"""
    Global config data
"""
# Import necessary packages
from classes.window import Window

# Create GlobalConfigData class


class GlobalConfigData:
    """
    This is used to save the project name and the window information 
    for that project, because those parameters are required in most other 
    objects
    """
    # Initialize  parameters for GlobalConfigData

    def __init__(self, project: str, window: Window):
        self.project = project
        self.window = window
