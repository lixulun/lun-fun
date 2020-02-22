from setuptools import setup

setup(
    name="lun-fun",
    packages=['lun_fun'],
    entry_points={
        "console_scripts": [
            "lun = lun_fun.__main__:execute"
        ]
    },
    author="Li Xulun",
    author_email="lixulun99@hotmail.com",
)