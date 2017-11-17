'''Usage: paml_cleaner.py <alignment> <wanted_species>'''

# Modules
import os  # Manipulating filenames
from Bio import SeqIO  # Reading in alignments


# Check if running interactively in an iPython console, or in a script from the
# command line
def in_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
# Run in a script from the command line
if in_ipython() is False:
    from docopt import docopt  # Command line argument handler
    cmdln_args = docopt(__doc__)
    alignment = cmdln_args.get('<alignment>')
    wanted_species_file = cmdln_args.get('<wanted_species>')
# Run interactively in an iPython console
if in_ipython() is True:
    alignment = '../data/At3g51820_5350_aligned.fasta'
    wanted_species_file = '../data/wanted_species.txt'


def name_truncate(record):
    record.description = ''
    record.id = record.id[:50]
    return record.id

alignment_name = os.path.splitext(alignment)[0]  # Retrieve filename
alignment_name = alignment_name.split('_aligned')[0]
alignment_format = os.path.splitext(alignment)[1]  # Retrieve filetype
alignment_format = alignment_format[1:]  # Remove '.' character from filetype


# Read in the wanted_species_file as a list of lines. Loop through each line,
# splitting it into 0:ID, 1:Genus_species, 2:#-samples-combined and retain the
# ID in the list wanted_ids.
wanted_ids = []
with open(wanted_species_file, 'r') as species_file:
    wanted_species = species_file.readlines()
    for line in wanted_species:
        ID = line.split('-')[0]
        wanted_ids.append(ID)

seqs_out = []
seqs_out_name = alignment_name + '_cleaned.' + alignment_format

for record in SeqIO.parse(alignment, format=alignment_format):
    for ID in wanted_ids:
        if ID in record.id:
            if 'merged' in record.id:
                list_of_merged_scaffolds = record.id.split('_merged_')
                number_of_merged_seqs = len(list_of_merged_scaffolds)
                scaffold = list_of_merged_scaffolds[0]
                list_of_merged_scaffolds.pop(0)
                species_code = scaffold.split('-')[0]
                species_name = scaffold.split('-')[2]
                scaffold = scaffold.split('-')[1]

                for merge in list_of_merged_scaffolds:
                    scaffold = scaffold + '-' + merge.split('-')[1]
                record.id = species_code + '-' + scaffold + '-' + species_name
                name_truncate(record)
                seqs_out.append(record)

            else:
                name_truncate(record)
                seqs_out.append(record)

SeqIO.write(seqs_out, handle=seqs_out_name, format=alignment_format)
