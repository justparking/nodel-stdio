# nodel-stdio
(covers lightweight Nodel interfaces using standard input and output)

The standard Nodel-host does process management via the **Process** and **quick_process** toolkit functions.

(CPython is being used as a reference here)

# By example (all files stored in the node's folder)
* **script.py**: Nodel recipe (un-parameterised)
* **myVLC.py**: important parts are `import nodel_stdio` line, `@nodel_stdio.nodel_action` decorator and `create_nodel_event(...)` function use (NOTE: no actual vlclib integration done yet)
* **vlc.py** vlclib Python bindings (not stored in this repo)

**NOTE** Please treat all files as works in progress.

