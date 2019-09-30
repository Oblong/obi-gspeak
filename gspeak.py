'''
Template for creating new gspeak apps
'''
from __future__ import print_function
from subprocess import call
import errno
import jinja2
import os
import re
import subprocess

def ensure_dir(path):
    '''
    mkdir -p for python
    '''
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def get_yobuild(g_speak_version):
    '''
    Look up which yobuild this gspeak depends on
    '''
    p = re.compile(r'YOBUILD_PREFIX.*"(.*)"')
    with open("/opt/oblong/g-speak%s/include/libLoam/c/ob-vers-gen.h" % g_speak_version, 'r') as f:
        for line in f:
            m = p.search(line)
            if (m):
                return m.group(1)

    # If g-speak wasn't installed, fall back to asking obs
    # NOTE: if the following line fails, please install the Oblong obs package
    return "/opt/oblong/deps-64-" + subprocess.check_output(["obs", "yovo2yoversion", g_speak_version]).rstrip()

def get_yobuild_major(g_speak_version):
    '''
    Look up which version of yobuild this gspeak depends on
    '''
    p = re.compile(r'YOBUILD_PREFIX.*".*-(.*)"')
    with open("/opt/oblong/g-speak%s/include/libLoam/c/ob-vers-gen.h" % g_speak_version, 'r') as f:
        for line in f:
            m = p.search(line)
            if (m):
                return m.group(1)

    # If g-speak wasn't installed, fall back to asking obs
    # NOTE: if the following line fails, please install the Oblong obs package
    return subprocess.check_output(["obs", "yovo2yoversion", g_speak_version]).rstrip()

def get_cef_branch(g_speak_version):
    '''
    Look up which cef this g-speak's webthing depends on
    '''
    p = re.compile(r'cefbranch=(.*)')
    webthingpath = "/opt/oblong/g-speak%s/lib/pkgconfig/libWebThing.pc" % g_speak_version
    if (os.path.exists(webthingpath)):
        with open(webthingpath, 'r') as f:
            for line in f:
                m = p.search(line)
                if (m):
                    return "cef" + m.group(1)

    # If webthing wasn't installed, fall back to asking obs
    # NOTE: if the following line fails, please install the Oblong obs package
    return subprocess.check_output(["obs", "yovo2cefversion", g_speak_version]).rstrip()

def obi_new(**kwargs):
    '''
    obi new gspeak project_name --gspeak=g_speak_home
    '''

    # On entry, kwargs['project_path'] is the directory to create and populate
    # from the files in the templates subdirectory next to this file
    # $G_SPEAK/lib/cmake/ObGenerateProject.cmake is an alternative implementation
    # that should always use the same template syntax and parameters.
    templates_path = os.path.join(os.path.dirname(__file__), 'templates')

    project_name = kwargs['project_name']
    project_path = kwargs['project_path']
    g_speak_xy = kwargs['g_speak_version']
    kwargs['yobuild'] = get_yobuild(g_speak_xy)
    kwargs['yobuild_major'] = get_yobuild_major(g_speak_xy)
    kwargs['cef_branch'] = get_cef_branch(g_speak_xy)

    env = jinja2.Environment(loader=jinja2.PackageLoader(__name__),
                             keep_trailing_newline=True)

    for folder, subs, files in os.walk(templates_path):
        for template_name in files:
            in_path = os.path.join(folder, template_name)
            rel_path = in_path.replace(templates_path, "")
            out_path = project_path + rel_path
            # Expand filename
            out_path = out_path.replace("@PROJECT@", project_name).replace("@G_SPEAK_XY@",g_speak_xy)
            # Create the directory for this file if it doesn't exist
            ensure_dir(os.path.dirname(out_path))
            try:
                template = env.get_template(rel_path)
                with open(out_path, 'w+') as fil:
                    fil.write(template.render(kwargs))
            except jinja2.TemplateNotFound:
                print("Warning: Could not find template {0}".format(template_name))

    # git init
    os.chdir(project_path)
    call(["git", "init"])
    call(["git", "add", "--all"])
    call(["git", "commit", "-m", "initial commit from obi template gspeak"])
    call(["git", "tag", "-am", "dev-0.1", "dev-0.1"])
    return 0
