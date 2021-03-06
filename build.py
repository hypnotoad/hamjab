import glob
import json
import os
import shutil
import sys

root = os.path.dirname(os.path.realpath(__file__))

def usage():
    print "Usage: {file} <server|client|eg|kodi>".format(file=os.path.basename(__file__))
    exit()

if len(sys.argv) < 2:
    usage()

build_type = sys.argv[1]

out_path = os.path.join(root, 'out', build_type)

def ignore(dir, files):
    result = filter(lambda x: x in ('.git') or x.endswith('.pyc'), files)
    return result

def make_build(file_list):
    # make the out dir
    if os.path.isdir(out_path):
        shutil.rmtree(out_path)
    os.makedirs(out_path)
    
    for cur_file in file_list:
        if type(cur_file) is tuple:
            source_file = cur_file[0]
            dest_file_path = os.path.join(out_path, *cur_file[1:])
        else:
            source_file = dest_file = cur_file
            dest_file_path = os.path.join(out_path, dest_file)

        source_file_path = os.path.join(root, source_file)
        
        if not os.path.exists(source_file_path):
            print "Unable to find file", source_file_path, "resulting build may be incomplete"
            continue
        
        dest_dir_path = os.path.dirname(dest_file_path)
        if not os.path.isdir(dest_dir_path):
            os.makedirs(dest_dir_path)

        print 'Copying', source_file

        if os.path.isdir(source_file_path):
            shutil.copytree(source_file_path, dest_file_path, ignore=ignore)
        else:
            shutil.copy(source_file_path, dest_file_path)

if build_type == 'server':
    print 'Building server...'
    
    server_files = [
        'server.py',
        'hamjab/lib.py',
        'hamjab/web.py',
        'hamjab/resources',
    ]

    make_build(server_files)
elif build_type == 'client':
    print 'Building device client...'

    client_files = [
        'deviceClient.py',
        'hamjab/lib.py',
        'hamjab/devices',
    ]

    make_build(client_files)
elif build_type == 'eg':
    print 'Building EventGhost plugin...'
    
    eg_files = [
        'controlClient.py',
        ('eg_plugin/__init__.py', '__init__.py'),
    ]
    
    for file_path in glob.glob('hamjab/resources/devices/*/device.json'):
        with open(file_path) as file_obj:
            text = file_obj.read() 
            data = json.loads(text)
        eg_files.append((file_path, 'devices', data['id'], 'device.json'))
    
    make_build(eg_files)
elif build_type == 'kodi':
    print 'Building Kodi addon...'
    
    kodi_files = [
        ('kodi', 'service.xbmc.hamjab'),
        ('hamjab/lib.py', 'service.xbmc.hamjab/resources/lib/lib.py'),
    ]
    
    make_build(kodi_files)
else:
    usage()