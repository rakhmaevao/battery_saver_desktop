from setuptools import setup

setup(
    name="battery_saver",
    version="0.1.0",
    py_modules=["battery_saver"],
    entry_points="""
    [console_scripts]
    battery_saver=battery_saver:main
""",
)
