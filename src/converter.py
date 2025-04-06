'''
MIT License

Copyright (c) 2025 Jayaraman rp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import os
import re

def replace_uvm_imports(uvm_code):
    """
    Replaces UVM imports and includes with PyUVM imports.
    """
    pyuvm_imports = """import cocotb
from cocotb.triggers import *
from cocotb.clock import Clock
from cocotb_coverage.crv import *
from pyuvm import *
import queue
import pyuvm
import logging
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
"""
    return re.sub(r'`include "uvm_macros.svh"\r?\nimport uvm_pkg::\*', pyuvm_imports, uvm_code)

def convert_uvm_to_pyu(uvm_code):
    """
    Converts UVM SystemVerilog code to PyUVM Python code.
    """
    # Replace UVM imports first
    uvm_code = replace_uvm_imports(uvm_code)
    
    # Replace UVM macros and syntax with PyUVM equivalents
    pyuvm_code = re.sub(r'`uvm_component_utils\((\w+)\)', r'class \1(UVMComponent):', uvm_code)
    pyuvm_code = re.sub(r'`uvm_object_utils\((\w+)\)', r'class \1(UVMObject):', pyuvm_code)
    pyuvm_code = re.sub(r'`uvm_do\((\w+)\)', r'self.do(\1)', pyuvm_code)
    pyuvm_code = re.sub(r'`uvm_info\((.+?),(.+?),(.+?)\)', r'self.logger.info(\2)', pyuvm_code)
    pyuvm_code = re.sub(r'function void build_phase\(.*?\);', r'def build_phase(self):', pyuvm_code)
    pyuvm_code = re.sub(r'function void connect_phase\(.*?\);', r'def connect_phase(self):', pyuvm_code)
    pyuvm_code = re.sub(r'function void run_phase\(.*?\);', r'def run_phase(self):', pyuvm_code)
    pyuvm_code = re.sub(r'endfunction', r'', pyuvm_code)
    pyuvm_code = pyuvm_code.replace(';', '')
    pyuvm_code = re.sub(r'`uvm_(.+?)', r'# Unsupported: \1', pyuvm_code)
    
    # Comment out "class ... extends uvm_test" lines
    pyuvm_code = re.sub(r'(class\s+\w+\s+extends\s+uvm_test)', r'# \1  # Cannot replace this line', pyuvm_code)
    
    # Add comments for unconverted lines
    lines = pyuvm_code.split('\n')
    for i, line in enumerate(lines):
        if '`uvm_' in line or 'extends uvm_test' in line:
            lines[i] = f'# {line}  # Cannot replace this line'
    pyuvm_code = '\n'.join(lines)
    
    return pyuvm_code

def generate_makefile(output_folder, top_level, module_name):
    """
    Generates a Makefile for running the converted PyUVM Python testbench.
    """
    makefile_content = f"""TOPLEVEL_LANG ?= verilog
SIM ?= questa
PWD=$(shell pwd)

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(PWD)/RTL/*.sv
else ifeq ($(TOPLEVEL_LANG),vhdl)
    VHDL_SOURCES = $(PWD)/ALU.vhdl
else
    $(error A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG))
endif

TOPLEVEL := {top_level}              # Module name
MODULE   := {module_name}            # Python testbench file name (without .py)

include $(shell cocotb-config --makefiles)/Makefile.sim
"""
    makefile_path = os.path.join(output_folder, "Makefile")
    with open(makefile_path, 'w') as makefile:
        makefile.write(makefile_content)

def process_sv_files(input_folder, output_folder):
    """
    Processes all .sv files in the input folder, converts them to PyUVM, and saves them in the output folder.
    Also generates a Makefile for running the converted Python testbench.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.sv'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as file:
                uvm_code = file.read()
            pyuvm_code = convert_uvm_to_pyu(uvm_code)
            output_file_path = os.path.join(output_folder, filename.replace('.sv', '.py'))
            with open(output_file_path, 'w') as output_file:
                output_file.write(pyuvm_code)
    
    # Generate Makefile
    top_level = "dut"  # Replace with your top-level module name
    module_name = "tb"     # Replace with your Python testbench file name (without .py)
    generate_makefile(output_folder, top_level, module_name)

if __name__ == "__main__":
    input_folder = 'input'
    output_folder = 'output'
    process_sv_files(input_folder, output_folder)
