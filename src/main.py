import os
import re
import subprocess
import argparse

BUILD_DIR = ".easypyc"
DEFAULT_EXECUTABLE_NAME = "a.out"

C_EXTENSIONS = [".c"] 
CPP_EXTENSIONS = [".cpp", ".cxx", ".cc"]
HEADER_EXTENSIONS = [".h", ".hpp", ".hxx", ".hh"]

def find_files(root_dir):
    source_files = []
    header_files = []

    for root, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in C_EXTENSIONS + CPP_EXTENSIONS):
                source_files.append(os.path.join(root, file))
            elif any(file.endswith(ext) for ext in HEADER_EXTENSIONS):
                header_files.append(os.path.join(root, file))

    return source_files, header_files

def find_dependencies(source_files, header_files):
    dependencies = {key: set() for key in header_files}

    for file in source_files + header_files:
        with open(file, "r") as f:
            for line in f:
                if re.match(r'#include\s+"[^"]+"', line):
                    parsed_file = line.split('"')[1]
                    included_file = os.path.abspath(os.path.join(os.path.dirname(file), parsed_file))
                    
                    if included_file in dependencies:
                        dependencies[included_file].add(file)
                    else:
                        dependencies[included_file] = {file}

    return dependencies

def needs_recompilation(source_file, dependencies, build_dir):
    relative_path = os.path.relpath(source_file, start=os.getcwd())
    object_file = os.path.join(build_dir, os.path.splitext(relative_path)[0] + ".o")

    if not os.path.exists(object_file):
        return True

    source_mtime = os.path.getmtime(source_file)
    object_mtime = os.path.getmtime(object_file)

    if source_mtime > object_mtime:
        return True
    
    for header_file in dependencies.get(source_file, []):
        if os.path.getmtime(header_file) > object_mtime:
            return True

    return False

def compile_to_object_files(source_files, dependencies, build_dir):
    for source_file in source_files:
        if needs_recompilation(source_file, dependencies, build_dir):
            relative_path = os.path.relpath(source_file, start=os.getcwd())
            object_file = os.path.join(build_dir, os.path.splitext(relative_path)[0] + ".o")

            object_file_dir = os.path.dirname(object_file)
            if not os.path.exists(object_file_dir):
                os.makedirs(object_file_dir)

            compiler = "gcc" if source_file.endswith(tuple(C_EXTENSIONS)) else "g++"
            compile_command = [compiler, "-c", source_file, "-o", object_file, "-Wall", "-Werror"]
            print(f"Recompiling {source_file}...")
            subprocess.run(compile_command, check=True)

def link_object_files(build_dir, executable_name):
    object_files = []
    for root, _, files in os.walk(build_dir):
        for file in files:
            if file.endswith(".o"):
                object_files.append(os.path.join(root, file))
    
    link_command = ["g++", "-o", executable_name] + object_files
    subprocess.run(link_command, check=True)

def run_executable(executable_name):
    subprocess.run([f"./{executable_name}"], check=True)

def main():
    parser = argparse.ArgumentParser(description="Compile and run C/C++ programs easily")
    parser.add_argument("-o", "--output", type=str, default=None, help="Specify the name of the output executable.")

    args = parser.parse_args()

    executable_name = args.output if args.output else DEFAULT_EXECUTABLE_NAME

    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)

    root_dir = os.getcwd()
    c_files, h_files = find_files(root_dir)
    dependencies = find_dependencies(c_files, h_files)
    compile_to_object_files(c_files, dependencies, BUILD_DIR)
    link_object_files(BUILD_DIR, executable_name)
    run_executable(executable_name)

    if not args.output:
        os.remove(executable_name)

if __name__ == "__main__":
    main()
