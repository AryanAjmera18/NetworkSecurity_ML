"""
the setup.py is an important file for packaging and distributing the code.
"""

from setuptools import  find_packages,setup
from typing import List

def get_requirements() -> List[str]:
    '''
    This function reads the requirements.txt file and returns a list of requirements
    '''
    requirement_lst:List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for  line in lines:
                requirement = line.strip()
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print('requirements.txt file not found')
         
    return requirement_lst

setup(
    name = 'NETWORKSECURITY_ML',
    version = '0.1',
    authour = 'Aryan Ajmera',
    authour_email = 'aryanajmera07@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements()
)
            