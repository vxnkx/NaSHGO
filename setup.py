from setuptools import setup, find_packages

setup(
    name="NaSHGO",
    version="1.0.0",
    author="vxnkx",
    description="OSINT tool to extract GPS from social media images",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "beautifulsoup4", 
        "Pillow",
        "exifread",
        "folium",
        "geopy",
        "shodan",
        "PyYAML",
        "tqdm",
        "python-telegram-bot",
        "qrcode[pil]"
    ],
    entry_points={
        "console_scripts": ["geoharvest=run:main"]
    },
    python_requires=">=3.8",
)
