from conans import ConanFile, CMake, tools
import os


class JsonRpcCppConan(ConanFile):
    name = "jsonrpc-cpp"
    version = "0.5"
    description = "JsonRpc-Cpp project is an implementation of JSON-RPC protocol in C++"
    homepage = "http://jsonrpc-cpp.sourceforge.net/"
    url = "https://github.com/bincrafters/conan-jsonrpc-cpp"
    license = "LGPL-3"
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "with_curl":[True, False]}
    default_options = {'shared': False, 'fPIC': True, 'with_curl': False}
    _source_subfolder = "source_subfolder"
    requires = "jsoncpp/1.9.2"
    generators = "cmake"
    autotools = None

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def requirements(self):
        if self.options.with_curl:
            self.requires.add("libcurl/7.67.0")

    def source(self):
        source_url = "https://cfhcable.dl.sourceforge.net/project/jsonrpc-cpp/jsonrpc-cpp"
        tools.get("{0}/jsonrpc-cpp-{1}.tar.bz2".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["WITH_CURL"] = self.options.with_curl
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="COPYING.*", dst="licenses", src=self._source_subfolder)
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        elif self.settings.os == "Windows":
            self.cpp_info.libs.append("ws2_32")
        if self.options.with_curl:
            self.cpp_info.defines = ["CURL_ENABLED"]
