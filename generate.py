#!/usr/bin/env python
#
# Copyright (C) 2018 Vanessa Sochat.
#
# This is a basic python script that will use the storage API to compare the
# current metadata API (mapped at data) to the updated one on Google Cloud
# storage. It is intended to run instide the container vanessa/container-api
# with Google Cloud credentials and a GOOGLE_STORAGE_BUCKET environment
# variables exported.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from google.cloud import storage
from spython.main import Client
from spython.utils import run_command

import subprocess
import shutil
import os
import sys
import re

# Sanity Checks ################################################################
# Make sure we have environment variables, exit if not

analyze = os.environ.get('ANALYZE_SINGULARITY', 'analyze-singularity.sh')
data = os.environ.get('API_DATABASE', '/data')
bucket_name = os.environ.get('GOOGLE_STORAGE_BUCKET')

if not bucket_name:
    print('Please export bucket name as GOOGLE_STORAGE_BUCKET')
    sys.exit(1)

credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS','')
if not credentials_file or not os.path.exists(credentials_file):
    print('Export GOOGLE_APPLICATION_CREDENTIALS')
    sys.exit(1)



# Helper #######################################################################

def run_analyze(container, dest, files=True):
    ''' a wrapper to run the command to generate the json object, calling
        analyze-singularity.sh that should be on the path, and renaming
        to the file wanted by the calling script.
    '''

    cmd = [analyze, container ]
    if files is True:
        cmd.append('--type=file')

    stdout, stderr = Client._run_command(cmd)

    files = [x for x in stdout.split('\n') if x]
    output_file = files[-1]
    if os.path.exists(output_file):
        shutil.move(output_file, dest)
    return dest



# Client #######################################################################

client = storage.Client()

# Get the bucket. It already exists.
bucket = client.get_bucket(bucket_name)
print('Bucket {} connected.'.format(bucket.name))

# List files (will do okay since we are in thousands of containers)
blobs = bucket.list_blobs()

for blob in blobs:

    # parse it's name to get the main path
    bucket, repo, user, repo, commit, hashy, filename = blob.name.split('/')

    # We want to organize based on the same path!
    path = os.path.join(data, bucket, repo, user, commit, hashy)
    uri = os.path.join(user, repo)

    # Create a folder for the metadata to extract
    if not os.path.exists(path):
        print('Found new container repository %s' %uri)
        os.makedirs(path)

    # We found an inspect
    if filename.endswith('inspect.json'):
        output_inspect = os.path.join(path, 'inspect.json')
        if not os.path.exists(output_inspect):
            blob.download_to_filename(output_inspect)

    # We found an image file!
    elif re.search('[.]img$|[.]simg$', filename):
        
        # Do we already have the commit / hash?
        output_packages = os.path.join(path, 'packages.json')
        output_files = os.path.join(path, 'files.json')

        # If not, we do the analysis with analysis-singularity.sh
        if not os.path.exists(output_files):

            print('Found new container version %s --> %s' %(uri, hashy))
            container = Client.pull('shub://%s' %uri, pull_folder='/tmp')

            # Run the analyze-singularity.sh for each of files and packages
            run_analyze(container, dest=output_files)
            run_analyze(container, files=False, dest=output_packages)

            os.remove(container)
