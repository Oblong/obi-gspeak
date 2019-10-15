project('{{project_name}}', 'cpp',
  version : '1.0.0',
  license : 'proprietary',
  default_options : [
    'werror=true',
    'warning_level=2',
    'cpp_std=c++11',
    'buildtype=debug',
    'b_ndebug=if-release',
  ]
)

maybe_cpp_flags = [
      #---- Turn on ALL THE WARNINGS! by default----
      '-Wall',
      '-Wempty-body',
      '-Wpointer-arith',
      '-Wshadow',
      '-Wtype-limits',
      '-Wvla',
      '-Wwrite-strings',
      '-fdiagnostics-show-option',
      #---- OK, but not the annoying ones ------
      #'-Wno-error=overloaded-virtual',
      '-Wno-error=suggest-override',    # boost/smart_ptr/detail/local_counted_base.hpp... meson doesn't use -isystem :-(
]
cpp_compiler = meson.get_compiler('cpp')
cpp_flags = cpp_compiler.get_supported_arguments(maybe_cpp_flags)

# Find system libraries this project depends on.
libs = [
   'libAfferent',
   'libNoodoo',
   'libTwillig',
]
project_deps = []
foreach lib : libs
   project_deps += dependency(lib, required : true)
endforeach

# Build the project, and install it if asked (via 'ninja install').
executable(
   '{{project_name}}',
   'src/{{project_name}}.cpp',
   cpp_args : cpp_flags,
   dependencies : project_deps,
   install : true)
