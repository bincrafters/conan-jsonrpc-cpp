#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class JsonRpcCppConan(ConanFile):
    name = "jsonrpc-cpp"
    version = "0.5"
    description = "JsonRpc-Cpp project is an implementation of JSON-RPC protocol in C++"
    homepage = "http://jsonrpc-cpp.sourceforge.net/"
    url = "https://github.com/bincrafters/conan-jsonrpc-cpp"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "LGPL-3"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    source_subfolder = "source_subfolder"
    requires = "jsoncpp/1.0.0@theirix/stable"
    autotools = None

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://cfhcable.dl.sourceforge.net/project/jsonrpc-cpp/jsonrpc-cpp"
        tools.get("{0}/jsonrpc-cpp-{1}.tar.bz2".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        configure_ac = os.path.join(self.source_subfolder, "configure.ac")
        tools.replace_in_file(configure_ac, "examples='yes'", "examples='no'")
        tools.replace_in_file(configure_ac, "doc='yes'", "doc='no'")

    def configure_autotools(self):
        if not self.autotools:
            with tools.chdir(self.source_subfolder):
                self.run("./autogen.sh")
                self.autotools = AutoToolsBuildEnvironment(self)
                configure_args = ['--disable-static' if self.options.shared else '--disable-shared']
                self.autotools.configure(args=configure_args)
        return self.autotools

    def build(self):
        autotools = self.configure_autotools()
        with tools.chdir(self.source_subfolder):
            autotools.make()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="COPYING.*", dst="licenses", src=self.source_subfolder)
        autotools = self.configure_autotools()
        with tools.chdir(self.source_subfolder):
            autotools.make(["install"])

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
