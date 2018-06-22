#!/bin/bash
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


VERSION=1.0.0

# Download latest version
mkdir -p upload && cd upload
wget "https://github.com/singularityhub/api/archive/v${VERSION}.zip"

# Shell into the container, mounting where the data is
docker run -v $HOME/.kaggle:/root/.kaggle -v $PWD:/tmp/data -it vanessa/kaggle bash
