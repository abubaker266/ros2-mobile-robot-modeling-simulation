cmake_minimum_required(VERSION 3.8)
project(robot_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ================= Dependencies =================
find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)

# ================= Testing =================
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)

  # Skip copyright check
  set(ament_cmake_copyright_FOUND TRUE)

  # Skip cpplint
  set(ament_cmake_cpplint_FOUND TRUE)

  ament_lint_auto_find_test_dependencies()
endif()

# ================= Install URDF =================
install(
  DIRECTORY urdf rviz worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()


