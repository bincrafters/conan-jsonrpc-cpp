#include <cstdlib>
#include "test_rpc.h"

int main() {
    Json::Value response;
    Json::Value value;
    TestRpc test_rpc;

    value["foobar"] = 42;
    value["cppstd"] = "c++17";
    value["package_manager"] = "conan.io";

    test_rpc.Print(value, response);
    test_rpc.Notify(value, response);

    return EXIT_SUCCESS;
}
