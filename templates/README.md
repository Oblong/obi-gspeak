# {{project_name}}
An amazing g-speak project.


# The project.yaml file

[project.yaml](project.yaml) contains all the information for building and running your g-speak application, if you use `obi` as your project runner tool.  It lets you specify launch options such as command arguments, environment vars, etc.

When running on your own machine (`obi go`), obi uses information from the `localhost` room in [project.yaml](project.yaml).


## Run locally
```bash
obi go
```

## Build locally
```bash
obi build
```

## Run in a room enviornment
```bash
obi go <room-name>
```

Where `<room-name>` is the name of one of the keys specified in the `rooms` map in [project.yaml](project.yaml).

## Stop the app

	obi stop [<room-name>]


## IDE Integration

obi generates the compile_commands.json file
used by many tools and IDEs to understand your project
and offer information about identifiers when you mouse over them.

### Visual Studio Code

obi does not yet create the launch.json file Visual Studio Code
needs to run your program.  If you want it to, please let us know.

## Sublime Text Users

This project has a [sublime-project file]({{project_name}}.sublime-project) that comes equipped with some useful build systems:

- `obi-build`: just build the app
- `obi-go`: build and run the app
- `obi-go:my-room`: build and run the app in your custom room *NOTE:* Requires custom setup in your project.yaml

## Switching to Meson

By default, 'obi build' will use CMake, which reads CMakeLists.txt to figure out how to build your project.

CMake works, but is not beloved by all.

Meson is a simpler, more modern alternative to CMake.
If you want to try it, edit project.yaml and uncomment the definition for meson-args.
'obi build' will then use meson, which reads meson.build to figure out how to build your project.

### Change default g-speak version
obi detects the g-speak version present at the time, and sets that
as the project's default.  To switch g-speak or cef versions, you can
change the default by running ob-set-defaults (included with the g-speak
platform SDK).  For instance,
```bash
ob-set-defaults --g-speak 4.2
```
Try 'ob-set-defaults --help' for more info.

## Riding without obi

### Build
```bash
cd build
cmake -DG_SPEAK_HOME=/opt/oblong/g-speak{{g_speak_version}} ..
ninja
```

Or, to use meson,
```bash
YOBUILD={{yobuild}}
G_SPEAK_HOME=/opt/oblong/g-speak{{g_speak_version}}
export BOOST_ROOT=$YOBUILD
export PKG_CONFIG_PATH=$YOBUILD/lib/pkgconfig:$YOBUILD/lib/x86_64-linux-gnu/pkgconfig:$G_SPEAK_HOME/lib/pkgconfig
cd build
meson ..
ninja
```

### Run
```bash
build/{{project_name}} [(<screen.protein> <feld.protein>)]
```

### Rebuild
```bash
cd build
ninja
```

### Build packages (mostly Oblong-specific)
The tool bau, included with the g-speak platform SDK,
is a bit like obi, but centers around building packages
for production rather than creating and running projects.

It can build linux and mac packages given the settings in ci/* and debian/*,
and the default recipes in /usr/bin/bau-defaults.

For instance,
```bash
bau build
```
It takes the same options as ob-set-defaults.  Try 'bau --help' and 'bau help' for more info.
