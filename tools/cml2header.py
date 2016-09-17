#!/usr/bin/python2

import os
import sys
import re
import StringIO
import getopt

class cml2header_translator:
	'''
	Translates a cml2 configuration file to a C header file
	that can be included in source code.
	'''
	def __init__(self):
		self.isnotset = re.compile("^# (.*) is not set")

	def linetrans(self, instream, outstream, trailer=None):
		'''
		Translates a stream line-by-line
		'''
		if not hasattr(instream, "readline"):
			instream = open(instream, "r")
		if not hasattr(outstream, "readline"):
			outstream = open(outstream, "w")
		while 1:
			line = instream.readline()
			if not line:
				break
			new = self.write_include(line)
			if new:
				outstream.write(new)
		instream.close()
		if trailer:
			outstream.write(trailer)
		outstream.close()

	def write_include(self, line):
		'''
		Translate a line of CML2 config file statement into
		C preprocessor #define format.
		'''
		if line.find("PRIVATE") > -1 or line[:2] == "$$":
			return ""
		match = self.isnotset.match(line)
		if match:
			return "#undef  %s\n" % match.group(1)
		if line == "#\n":
			return None
		elif line[0] == "#":
			return "/* " + line[1:].strip() + " */\n"
		eq = line.find("=")
		if eq == -1:
			return line
		else:
			line = line.split('#')[0]
			symbol = line[:eq]
			value = line[eq+1 :].strip()
		if value == 'y':
			return "#define %s 1\n" % symbol
		elif value == 'm':
			return "#undef %s\n#define %s_MODULE 1\n" % (symbol, symbol)
		elif value == 'n':
			return "#undef  %s\n" % symbol
		else:
			return "#define %s %s\n" % (symbol, value)

	def cml_configfile_exists(self, path):
		if not os.path.exists(path):
			print "CML2 configuration file not found."
			print "Given path:", path, "does not exist."
			return 0
		else:
			return 1

	def translate(self, configfile_path = None, headerfile_path = None):

		if configfile_path == None:
			configfile_path = os.getcwd() + '/' + "config.out"

		if headerfile_path == None:
			headerfile_path = os.getcwd() + '/' + "config.h"
		'''
		Takes a configuration file generated by the cml2 configurator,
		and converts it to a C header file. This header file is	then
		included by the kernel sources and the preprocessor definitions
		in it are used during the compilation of the kernel.
		'''
		if not self.cml_configfile_exists(configfile_path):
			print "Failed to translate cml configuration file", configfile_path, 'to', headerfile_path
			return -1

		self.linetrans(configfile_path, headerfile_path)
		return 0

	def usage(self):
		helpstr =	\
		'''\
    Description:
    cml2header.py takes a cml2 configuration file as input and generates
    a valid C header file to be included in C source code.

    Usage:
    cml2header.py -i inputfile -o outputfile [-h]

    Options:
	-i    The CML2 configuration file	(config.out by default)
	-o    The name of the header file	(config.h by default)
	-h    This help message
		'''
		print helpstr

def main():
	translator = cml2header_translator()
	try:
		opts, args = getopt.getopt(sys.argv[1:], "i:o:h:")
	except getopt.GetoptError:
		# print help information and exit:
		translator.usage()
		sys.exit(2)

	ofile = None
	ifile = None

	# Print help message if requested and quit
	if '-h' in opts:
		translator.usage()
		sys.exit()

	# Get the input and output filenames.
	for switch, val in opts:
        	if switch == '-i':
			ifile = val
		if switch == '-o':
			ofile = val

	# Translate
	if translator.translate(ifile, ofile) < 0:
		print "Translation of", ifile, 'to', ofile, 'failed.'

# Run the main routine only if this file is explicitly executed.
# (i.e. not referred from another module)
if __name__ == "__main__":
    main()

