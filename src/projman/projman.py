import os
import yaml
import shutil
import exception
import glob

class Projman():

    """
    Constructor:
    1.  Reads Templates from folder/folders specified in PROJMAN_TEMPLATES env var.
        Format:  {'maya': {'value': [{'value': 'chan'}, {...}], 'permission': '0771'}, 'houdin': {...}}

    2.  Reads project_path as specified in env var PROJMAN_LOCATION.
    
    3.  Creates a project_list_path which will be used to store the information about projects. We will save this in YAML format 
        at location '~/projman/projects'.
        Format: 
            houdini:
            - {name: hj, path: <path1>}
            - {name: bc, path: <path3>}
            maya:
             - {name: ibwv, path: <path1>}
             - {name: vv, path: <path2>}

    """
    def __init__(self):
        self.templates = {}
        try:
            template_paths = os.getenv('PROJMAN_TEMPLATES')
            for template_path in template_paths.split(':'):
                for filename in glob.glob(os.path.join(template_path, '*.yaml')):
                    templates = yaml.load(open(filename))
                    for template in templates:
                        name = template['value'].keys()[0]
                        permission = template['permission']
                        self.templates[name] = {'value': template['value'][name], 'permission': permission}
        except Exception as e:
            raise exception.TemplateError("Template error: " + e.message)

        self.default_path = os.getenv('PROJMAN_LOCATION', os.path.expanduser('~/projman/projects'))
        self.project_list_path = os.path.expanduser('~/project_list.yaml')
        if not os.path.exists(self.project_list_path):
            yaml.dump({}, open(self.project_list_path, "w"))
    
    """
    Create a project at <path> location with a particular type and name
    <name>: mandatory:  name of the project
    <project_type>: mandatory:  type of the project to be created. Eg: maya|houdini . Note: templates will be loaded from 
                                PROJMAN_TEMPLATES env variable.
    <project_path>: Optional:   Can override the default value presented by PROJMAN_LOCATION env variable or '~/projman/projects'
    
    Raises an exception:    If the type is not valid.
                            If the folder is already present.
    """

    def create(self, name, project_type, project_path=None):
        # Raise an exception id type is not valid
        if not self.__is_valid_type(project_type):
            raise Exception(str("Type %s is not available" % project_type))

        if not project_path:
            project_path = self.default_path
        folder_path = project_path + '/' + name

        #Raise an exception if already a project with the same name exists.
        if os.path.exists(folder_path):
            raise Exception(str("%s already exists" % folder_path))
        self.__create_project(project_type, folder_path)

        # Update the information of type, name and path in project list.
        project_list = yaml.load(open(self.project_list_path))
        if project_type in project_list:
            project_list[project_type].append({'name' : name , 'path': folder_path})
        else:
            project_list[project_type] = []
            project_list[project_type].append({'name' : name , 'path': folder_path})
        yaml.dump(project_list, open(self.project_list_path, "w"))

    """
    List the projects which have been created, optionally restricting the list to a specific type or types.
    <types>:    Optional:   Comma seperated types:  maya,houdini : Will not give any value for not existing type.
    
    Returns a string of \n seperated project names.
    """
    def list(self, types=None):
        project_list = yaml.load(open(self.project_list_path))
        project_names = []
        if  not types:
            types = project_list.keys()
            for typ in types:
                projects = project_list[typ]
                for p in projects:
                    project_names.append(p['name'])
        else:
            for typ in types.split(','):
                if typ in project_list:
                    projects = project_list[typ]
                    for p in projects:
                        project_names.append(p['name'])
        
        print('\n'.join(project_names))

    
    """
    Delete an existing project.
    <name>: Mandatory:  Name of the project.
    <project_type>: Optional:  To restrict the deletion to a particular type within the project tree.

    Raises Exception if the type is not valid . 
    """
    def delete(self, name, project_type=None):
        project_list = yaml.load(open(self.project_list_path))
        # delete project with given name and type
        if project_type:
            if not self.__is_valid_type(project_type):
                raise Exception(str("Type %s is not available" % project_type))
            if not project_list[project_type]:
                return
            self.__delete(project_list[project_type], name)
        # delete project with given name only
        else:          
            for project_type in project_list:
                self.__delete(project_list[project_type], name)
        yaml.dump(project_list, open(self.project_list_path, "w"))

    
    """
    List the types of projects which may be created.

    """
    def types(self):
        if not self.templates:
            print("No templates are present")
        else:
            print('\n'.join(self.templates.keys()))

    
    """
    Pretty print the structure of a project template.
    <type> : Mandatory

    Raises Exception if the type is not valid.
    """
    def describe(self, type):
        if type not in self.templates:
            raise Exception(str("Template: %s not available" % type))
        directories = self.templates[type]['value']
        for directory in directories:
            self.__pretty_print(directory, 0)

    

    def __create_project(self, project_type, path):
        project_template = self.templates[project_type]['value']
        project_permission = self.templates[project_type]['permission']
        for directory in project_template:
            self.__create_directory(directory, project_permission, path)

    def __create_directory(self, directory, permission, parent_path):
        if isinstance(directory['value'], str):
            if 'permission' in directory:
                print("creating %s with %s", directory['value'], directory['permission'])
                self.__createFolderorFile(parent_path, directory['value'], directory['permission'])
            else:
                self.__createFolderorFile(parent_path, directory['value'], permission)
        elif isinstance(directory['value'], dict):
            if 'permission' in directory:
                permission = directory['permission']
                print("creating %s with %s", directory['value'].keys()[0], directory['permission'])

            parent_dir_name = directory['value'].keys()[0]
            self.__createFolderorFile(parent_path, parent_dir_name, permission)
            for child_directory in directory['value'][parent_dir_name]:
                current_parent_path = parent_path + '/' + parent_dir_name
                self.__create_directory(child_directory, permission, current_parent_path)

    def __createFolderorFile(self, parent, dir_or_file, permission):
        try:
            complete_path = parent + '/' + dir_or_file
            if '.' in dir_or_file:
                with open(complete_path, 'w'):
                    pass
            else:
                if not os.path.exists(complete_path):
                    os.makedirs(complete_path)
            os.chmod(complete_path, int(permission, 8))
            print(complete_path)
        except OSError as e:
            raise Exception(str("Error in creating file or directory: %s" % e))

    
    def __pretty_print(self, directory, level):
        if isinstance(directory['value'], str):
            line = "|" + "   |"*level + "---" + directory['value']
            print(line)
        elif isinstance(directory['value'], dict):
            p_dir = directory['value'].keys()[0]
            line = "|" + "   |"*level + "---"  + p_dir
            print(line)
            for directory in directory['value'][p_dir]:
                self.__pretty_print(directory, level+1)

    def __delete(self, project_list, project_name):
        #Will iterate on the copy of list as we will be deleting the elems during iteration.
        project_list_iter = project_list[:]
        for project in project_list_iter:
            if project['name'] == project_name:
                delete_path = project['path']
                print("removing " + delete_path)
                shutil.rmtree(delete_path, ignore_errors=True)
                project_list.remove(project)

    def __is_valid_type(self, ptype):
        if ptype in self.templates.keys():
            return True
        else:
            return False
