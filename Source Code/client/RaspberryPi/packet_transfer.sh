#!/bin/bash
cd txt
packet_transfer_programs=`cat test_program.txt | awk '{print $1}'`
cd ..
cd packet_transfer_programs
sudo ./$packet_transfer_programs
cd ..
