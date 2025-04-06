// uvm_file.sv
`include "uvm_macros.svh"
import uvm_pkg::*;

class my_uvm_test extends uvm_test;
    `uvm_component_utils(my_uvm_test)

    function new(string name = "my_uvm_test", uvm_component parent = null);
        super.new(name, parent);
    endfunction

    task run_phase(uvm_phase phase);
        `uvm_info("MY_UVM_TEST", "Starting run phase", UVM_LOW)
        `uvm_info("MY_UVM_TEST", "Ending run phase", UVM_LOW)
    endtask
endclass