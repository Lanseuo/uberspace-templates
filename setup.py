from setuptools import setup

long_description = open("README.md").read()

setup(
    name="uberspace-templates",
    version="1.0.1",
    description="Setup applications and websites in seconds using this cli with many templates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Lucas Hild",
    author_email="contact@lucas-hild.de",
    url="https://github.com/Lanseuo/uberspace-templates",
    packages=["uberspace_templates", "uberspace_templates.templates"],
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        uberspace-templates=uberspace_templates:cli
    """
)
