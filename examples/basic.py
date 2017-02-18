
from fstree import Tree


my_project = Tree("~/Work/my-project")
my_project.create()
my_project.child_file('README.md').write_bytes('''
# MyProject


### Installing


```bash
pip install myproject
```
''')
