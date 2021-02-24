#!/usr/bin/env python

import random
import os
import argparse
import shutil

# import arguments from command line
def get_args():
    parser = argparse.ArgumentParser(description='down samples fastq file randomly')
    parser.add_argument("-i", "--file_in", type=str, help='specifies input file.')

    return parser.parse_args()

parseArgs = get_args()

input_file_name = parseArgs.file_in

output_file_name = input_file_name.split(".fa")[0] + "_ds.fastq"

class FASTQ_READ:

    def __init__(self, fastq_read):

        self.fastq_read = fastq_read
        self.hole      = self.get_hole()
    
    def get_hole(self):

        hole = self.fastq_read.split("\n")[0].split("/")[1]

        return hole

def shuffle_file(input_file, input_file_name):

    # shuffle files into 100 sub files
    os.system("mkdir database")
    cpp_comand = "./shuffle_fastq " + input_file_name
    os.system(cpp_comand) # call c++ file to shuffle fastq file


    # get list of filenames  
    read_files = ["./database/" + str(i) + ".fastq" for i in range(1,100)]

    # merge all files 
    with open("./database/shuffled.fastq", "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                shutil.copyfileobj(infile, outfile)



def consider_read(fastq_obj, hole_dic, out_file, out_file_name, in_file_size):

    # if the ZMW has already been written out, write all others
    if fastq_obj.hole in hole_dic:
        out_file.write(fastq_obj.fastq_read)

    # if the file is not at capacity
    elif os.path.getsize(out_file_name) <= (.75*in_file_size):
        out_file.write(fastq_obj.fastq_read)
        hole_dic[fastq_obj.hole] = 0

    else:
        pass


def main():

    # hole dic
    hole_dic = {}

    # open input
    input_file = open(input_file_name, "r")

    # shuffle file
    shuffle_file(input_file, input_file_name)

    shuffled_file = open("./database/shuffled.fastq")
    output_file = open(output_file_name, "w")
    in_file_size = os.path.getsize(input_file_name)

    for line in shuffled_file:

        # get fastq read
        fastq_read = line + "".join([shuffled_file.readline() for i in range(3)])

        # make fastq read object
        fastq_obj = FASTQ_READ(fastq_read)

        # consider and write out read
        consider_read(fastq_obj, hole_dic, output_file, output_file_name, in_file_size)
        
    # close files
    input_file.close()
    output_file.close()


    # delete database
    shutil.rmtree("./database")

main()






        



        

