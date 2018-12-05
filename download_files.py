from io import BytesIO as StringIO
from io import UnsupportedOperation
from urllib.request import urlopen
import tempfile
import bz2
import gzip
import optparse
import os
import shutil
import sys
import tarfile
import tempfile
import zipfile
from ftplib import FTP



CHUNK_SIZE = 2 ** 20 # 1mb

def _download_file(start, fh):
    tmp = tempfile.NamedTemporaryFile()
    tmp.write(start)
    while True:
        data = fh.read(CHUNK_SIZE)
        if data:
            tmp.write(data)
        else:
            break
    tmp.flush()
    tmp.seek(0)
    return tmp


def _get_stream_readers_for_tar(fh, tmp_dir):
    fasta_tar = tarfile.open(fileobj=fh, mode='r:*')
    return [x for x in [fasta_tar.extractfile(member) for member in fasta_tar.getmembers()] if x]


def _get_stream_readers_for_zip(fh, tmp_dir):
    """
    Unpacks all archived files in a zip file.
    Individual files will be concatenated (in _stream_fasta_to_file)
    """
    fasta_zip = zipfile.ZipFile(fh, 'r')
    rval = []
    for member in fasta_zip.namelist():
        fasta_zip.extract(member, tmp_dir)
        rval.append(open(os.path.join(tmp_dir, member), 'rb'))
    return rval


def _get_stream_readers_for_gzip(fh, tmp_dir):
    return [gzip.GzipFile(fileobj=fh, mode='rb')]


def _get_stream_readers_for_bz2(fh, tmp_dir):
    return [bz2.BZ2File(fh.name, 'rb')]

def get_stream_reader(fh, tmp_dir):
    """
    Check if file is compressed and return correct stream reader.
    If file has to be downloaded, do it now.
    """
    magic_dict = {
        b"\x1f\x8b\x08": _get_stream_readers_for_gzip,
        b"\x42\x5a\x68": _get_stream_readers_for_bz2,
        b"\x50\x4b\x03\x04": _get_stream_readers_for_zip,
    }
    start_of_file = fh.read(CHUNK_SIZE)
    try:
        fh.seek(0)
    except UnsupportedOperation:  # This happens if fh has been created by urlopen
        fh = _download_file(start_of_file, fh)
    try:  # Check if file is tar file
        if tarfile.open(fileobj=StringIO(start_of_file)):
            return _get_stream_readers_for_tar(fh, tmp_dir)
    except tarfile.ReadError:
        pass
    for k, v in magic_dict.items():
        if start_of_file.startswith(k):
            return v(fh, tmp_dir)
    return [fh]
