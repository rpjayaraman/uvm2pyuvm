// uvm_file.sv
import cocotb
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


# class my_uvm_test extends uvm_test
    class my_uvm_test(UVMComponent):

    function new(string name = "my_uvm_test", uvm_component parent = null)
        super.new(name, parent)
    

    task run_phase(uvm_phase phase)
        self.logger.info( "Starting run phase")
        // Add test logic here
        self.logger.info( "Ending run phase")
    endtask
endclass