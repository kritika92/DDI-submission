# -*- coding: utf-8 -*-

import os
import yaml
import shutil
class Projman():
             
#    houdini:
# - {name: hj, path: <path1>}
# - {name: bc, path: <path3>}
# - {name: ege, path: <path2>}
#    maya:
#   - {name: ibwv, path: <path1>}
#   - {name: wver, path: <path3>}
#   - {name: vv, path: <path2>}

    def __init__(self):
        self.templates = {}
        template_paths = os.getenv('PROJMAN_TEMPLATES')
        for template_path in template_paths.split(':'):
            templates = yaml.load(open(template_path))
            for template in templates:
                name = template['value'].keys()[0]
                permission = template['permission']
                self.templates[name] = {'value': template['value'][name], 'permission': permission}

        self.default_path = os.getenv('PROJMAN_LOCATION', os.path.expanduser('~/projman/projects'))
        self.project_list_path = os.path.expanduser('~/project_list.yaml')
        if not os.path.exists(self.project_list_path):
            yaml.dump({}, open(self.project_list_path, "w"))


    def create(self, name, ptype, path=None):
        project_type = ptype
        if path:
            project_path = path + '/' + name
        else:
            project_path = self.default_path + '/' + name
        self.create_project(project_type, project_path)
        project_list = yaml.load(open(self.project_list_path))
        if project_type in project_list:
            project_list[project_type].append({'name' : name , 'path': project_path})
        else:
            project_list[project_type] = []
            project_list[project_type].append({'name' : name , 'path': project_path})
        yaml.dump(project_list, open(self.project_list_path, "w"))


    def list(self, types=None):
        project_list = yaml.load(open(self.project_list_path))
        project_names = []
        if  not types:
            types = project_list.keys()
            projects = project_list[types]
            for p in projects:
                project_names.append(p['name'])
        else:
            if types in project_list:
                projects = project_list[types]
                for p in projects:
                    project_names.append(p['name'])
            
        
        print('\n'.join(project_names))


    def delete(self, name=None, ptype=None):
        project_type = ptype
        project_list = yaml.load(open(self.project_list_path))
        print(project_list)
        if name:
            for project_type in project_list:
                for project in project_list[project_type]:
                    if project['name'] == name:
                        delete_path = project['path']
                        print("removing " + delete_path)
                        shutil.rmtree(delete_path)
                        project_list[project_type].remove(project)

        elif project_type:
            for project in project_list[project_type]:
                delete_path = project['path']
                shutil.rmtree(delete_path, ignore_errors=True)
            del project_list[project_type]

        yaml.dump(project_list, open(self.project_list_path, "w"))


    def types(self):
        return self.templates.keys()

    def create_project(self, project_type, path):
        project_template = self.templates[project_type]['value']
        project_permission = self.templates[project_type]['permission']
        project_path = self.default_path
        if path:
            project_path = path

        for directory in project_template:
            self.create_directory(directory, project_permission, path)

    def create_directory(self, template, permission, parent_path):
        if isinstance(template['value'], str):
            if 'permission' in template:
                self.createFolderorFile(parent_path, template['value'], template['permission'])
            else:
                self.createFolderorFile(parent_path, template['value'], permission)
        elif isinstance(template['value'], dict):
            if 'permission' in template:
                permission = template['permission']
            p_dir = template['value'].keys()[0]
            self.createFolderorFile(parent_path, p_dir, permission)
            for directory in template['value'][p_dir]:
                directory_path = parent_path + '/' + p_dir
                self.create_directory(directory, permission, directory_path)

    def createFolderorFile(self, parent, dir_or_file, permission):
        try:
            directory = parent + '/' + dir_or_file
            if '.' in dir_or_file:
                with open(os.path.join(parent, dir_or_file), 'w'):
                    pass
                os.chmod(directory, int(permission, 8))
            else:
                print("creating: " + str(directory))
                if not os.path.exists(directory):
                    os.makedirs(directory, int(permission, 8))
        except OSError:
            print ('Error: Creating directory ot file. ' + directory)


    
    def prettyPrint(self, path):
        for path, dirs, files in os.walk(path):
            print path
            for f in files:
                print f
