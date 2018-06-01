#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_template_default

if __name__ == "__main__":

    # TODO (uilianries): Remove after to integrate jsoncpp/1.0.0 on theirix repository
    os.environ["CONAN_REMOTES"] = os.getenv("CONAN_REMOTE", "https://api.bintray.com/conan/uilianries/conan")

    builder = build_template_default.get_builder(pure_c=False)
    builder.run()
