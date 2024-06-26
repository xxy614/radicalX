# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This package holds a handful of utilities for calculating digests."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib

from containerregistry.client.v2 import util



def SHA256(content, prefix='sha256:'):
  """Return 'sha256:' + hex(sha256(content))."""
  return prefix + hashlib.sha256(content).hexdigest()


def SignedManifestToSHA256(manifest):
  """Return 'sha256:' + hex(sha256(manifest - signatures))."""
  unsigned_manifest, unused_signatures = util.DetachSignatures(manifest)
  return SHA256(unsigned_manifest.encode('utf8'))
