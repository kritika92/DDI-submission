First of all I started with reading yaml file. It consisted of various dcitionary, nested dictionary, lists. I had to create directories, subdirectories ot of them. So used recursion for creating directories , subdirectories.

template_paths: lit of colon seperated paths of projamn templates
self.templates: a dictioanry having details of particular type of file with their respective permission

self.project_list_path: path of the yaml file created
I'm creating yaml file to store all the type of directories created with their name and path
for eg.     
houdini:
{name: hj, path: <path1>}
{name: bc, path: <path3>}
{name: ege, path: <path2>}
maya:
{name: ibwv, path: <path1>}
{name: wver, path: <path3>}
{name: vv, path: <path2>}


After creating or deleting any directory,  I'm updating my yaml file.
