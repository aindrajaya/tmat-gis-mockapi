from setuptools import setup, find_packages

setup(
    name="tmat-gis-mockapi",
    version="1.0.0",
    description="Mock API for TMAT GIS monitoring system",
    author="aindrajaya",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "fastapi==0.109.0",
        "uvicorn[standard]==0.27.0",
        "pydantic==2.7.0",
        "pydantic-core==2.18.1",
        "python-dotenv==1.0.0",
        "httptools==0.6.1",
        "websockets==12.0",
    ],
)
