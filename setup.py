from setuptools import find_packages,setup
from typing import List

HYPON_E_DOT = "-e . "
def get_requirements(file_path:str)->List[str]:
    #Get requirements from a file
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPON_E_DOT in requirements:
            requirements.remove(HYPON_E_DOT)
            return requirements


setup(
    name= 'Wafer_Fault_Detection',
    version='0.0.1',
    author='Himanshu pewal',
    author_email='himanshupewal101@gmail.com',
    description = "A web application to discuss the faults in wafer",
    install_requriers=get_requirements("requirements.txt"),
    packages=find_packages()


)