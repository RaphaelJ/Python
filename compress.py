#! /usr/bin/python3

# Compress and uncompress differents files inside a directory (rar, zip, iso,
# exe, mdf, sh ...) into 7z with a high compression ratio.

import sys, os, tempfile, subprocess, shutil
import os.path as path

compression = '7z a -t7z -m0=lzma2 -mx=9 -mfb=64 -md=32m -ms=on'
extension = '7z'
min_size = 100 * 1024 * 1024 # 100Mio
min_ratio = 0.05 # min 5% of compression gain

log = None
ignore = []
total_gains = [0]

def file_extension(f):
    """ Get file's extension '"""
    _, ext = path.splitext(f)
    return ext[1:]

def file_without_ext(f):
    """ Filename without extension """
    filename, _ = path.splitext(f)
    return filename

def seven_zip(sources, dest):
    """
        Compress sources into dest using 7zip
    """

    if os.path.exists(dest):
        print("{0} exists. Press Y to erase.".format(dest))
        if not input() in ('Y', 'y'):
            raise Exception("Archive already exists.")

    command = compression.split(" ") + [dest] + sources
    subprocess.check_call(command)

def compress(sources):
    """
        Compress a file/directory using 7zip.
        If the gain is not large enough, remove the archive, otherwise remove
        the source.
    """

    dest = "{0}.{1}".format(file_without_ext(sources[0]), extension)

    seven_zip(sources, dest)

    sources_size = 0
    for s in sources:
        sources_size += path.getsize(s)
        
    dest_size = path.getsize(dest)

    gain = sources_size - dest_size

    if gain < sources_size * min_ratio: # Not enought gain
        os.unlink(dest)
        return 0
    else:
        for s in sources:
            os.unlink(s)
        return gain

def recompress_dir(uncompressor, source_archive):
    """
        Recompress an archive into an 7z archive.
        'uncompressor' is a function which returns a command to uncompress when a
        output directory is given.
        Return the gain.
    """

    tmpdir = tempfile.mkdtemp()

    # Uncompress into tmpdir
    subprocess.check_call(uncompressor(tmpdir))

    # Compress into source_archive.7z
    dest = "{0}.{1}".format(file_without_ext(source_archive), extension)
    seven_zip([path.join(tmpdir, "*")], dest)

    source_size = path.getsize(source_archive)
    dest_size = path.getsize(dest)

    shutil.rmtree(tmpdir)
    os.unlink(source_archive)
    
    return source_size - dest_size
    

def rec_compress(root):
    """ Iterate each file/directory, recursively (DFS) """

    def log_success(full_path, gain):
        log.write("{0};{1}\n".format(full_path, gain))
        print("{0}\t{1:g}Mio saved\n".format(full_path, gain/1024/1024))
        total_gains[0] += gain
    
    for f in os.listdir(root):
        full_path = path.join(root, f)
        if path.isdir(full_path):
            rec_compress(full_path)
        elif not full_path in ignore:
            ext = file_extension(full_path)
            size = path.getsize(full_path)
            if ext in targets and (targets[ext][1] or size >= min_size):
                gain = targets[ext][0](full_path)
                log_success(full_path, gain)

def process_file(f):
    """ Compress the file, remove the source is compression gain """
    return compress([f])

def process_zip(f):
    """ Unzip the file in /tmp, recompress the file, remove the source """
    return recompress_dir(lambda tmpdir: ["unzip", f, "-d", tmpdir], f)
    
def process_rar(f):
    """ Unrar the file in /tmp, recompress the dir, remove the source """
    gain = recompress_dir(lambda tmpdir: ["unrar", "x", f, tmpdir], f)

    # Remove all *.rXX
    for r in os.listdir(path.dirname(f)):
        if file_extension(r) in ("r{0:0>2}".format(i) for i in range(0, 100)):
            os.unlink(r)

    return gain

def process_associed(f, associated):
    """ Compress a file with his associated files """

    to_compress = [f]

    for ext in associated:
        assoc = "{0}.{1}".format(file_without_ext(f), ext)
        
        if path.exists(assoc):
            to_compress.append(assoc)
    
    return compress(to_compress)

targets = {
    # extension: (action, force compression (don't check size))
    "iso": (process_file, False),
    "exe": (process_file, False),
    "daa": (process_file, False),
    "nrg": (process_file, False),
    "sh": (process_file, False),
    "zip": (process_zip, True),
    "rar": (process_rar, True),
    "mdf": (lambda f: process_associed(f, ['mds']), False),
    "bin": (lambda f: process_associed(f, ['cue']), False),
}

if __name__ == '__main__':
    root = sys.argv[1]

    try:
        # Restore
        for line in open(root + '/' + 'compress.log', 'r'):
            name, gain = line.split(';')
            ignore.append(name)
            total_gains[0] += int(gain)
            
        print("{0} files already compressed from compress.log".format(
            len(ignore)
        ))
    except:
        pass

    log = open(path.join(root, 'compress.log'), 'a+')

    rec_compress(root)
    
    log.close()

    print("Finished. Gain: {0:g}Mio".format(total_gains[0] / 1024 / 1024))