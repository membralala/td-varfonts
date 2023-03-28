import sys

def appendDependenciesPath():
    dependencies_path = f"{project.folder}/dep/python{sys.version_info.major}.{sys.version_info.minor}"
    if not dependencies_path in sys.path: 
        sys.path.append(dependencies_path)

def onStart():
    appendDependenciesPath()
    
    
def onCreate():
    appendDependenciesPath()


