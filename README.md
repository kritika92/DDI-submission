# pm
Command Line to create project structure based on templates.

### Prerequisites
  Set PROJMAN_TEMPLATES env variable with colon seperated folder location of templates.
  
  Optionally set PROJMAN_LOCATION env variable to set the location of folder.

### Installing

```
git clone <this project>
cd DDI-submission
make
```

### Usage

```

usage: pm.py [-h] [-t TYPE] [-p PATH] {list,create,delete,types,describe} ...

positional arguments:
  {list,create,delete,types,describe}
                        SUBCMD
    list                List the projects which have been created, optionally
                        restricting the list to a specific type or types
    create              Create a new project in PROJECT_PATH
    delete              Delete an existing project. Optionally, restrict the
                        deletion to a particular type within the project tree
    types               List the types of projects which may be created
    describe            Pretty print the structure of a project template

optional arguments:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  The type of the project created from a specific
                        template
  -p PATH, --path PATH  The base path in which to create the project. If not
                        supplied, it uses a default project path

```
                        
### Example

**Create**
```
pm create xyz
pm -t maya create abc 
pm -t houdini -p /abc/xyz create abcd 
pm -t houdini -p /abc/xyz create abc 
```

```
pm -t maya delete abc       # will delete only maya project with name abc
pm delete abc               # will delete all available projects with name abc
```

**Other Commands**
```
pm  -t maya list
pm list
pm types
pm describe
```

### Templates: 
Can be configured by PROJMAN_TEMPLATES env variable. 
```Supported format: YAML```
#### Example:
```
- permission: "0751"
  value:
    maya:
      - value: chan
      - value: data
      - permission: "0771"
        value: images
      - value:
          renderData:
          - value: depth
          - value: iprImages
          - value:
              vray:
                - value: finalgMap
                - value: lightMap
                - value: photonMap
                - value: shadowMap
          - value: shaders
      - permission: "0771"
        value:
          scenes:
            - value: default.mb
      - value: scripts
      - value: sound
      - value:
          startup:
          - value: jobSetup.mel
      - value: textures
      - permission: "0771"
        value: workspace.mel
```
