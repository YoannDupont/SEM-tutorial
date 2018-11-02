#-*- coding: utf-8 -*-

import os.path
import sys
import codecs

from sem.importers import brat_file
from sem.storage import Document, SEMCorpus, Annotation


def main(filenames, outfilename):
    outfilename = os.path.splitext(outfilename)[0]
    txtfilename = outfilename + ".txt"
    annfilename = outfilename + ".ann"
    shift = 0
    cur_id = 1
    NUM_NEWLINES = 4
    with codecs.open(txtfilename, "w", "utf-8") as txt, codecs.open(annfilename, "w", "utf-8") as ann:
        for filename in filenames:
            document = brat_file(filename, encoding="utf-8")
            txt.write(document.content)
            txt.write("\n" * NUM_NEWLINES)
            for annotation in document.annotation("NER").get_reference_annotations():
                ann.write(u"T{ident}\t{value} {lb} {ub}\t{txt}\n"
                    .format(
                        ident=cur_id,
                        value=annotation.value,
                        lb=annotation.lb+shift,
                        ub=annotation.ub+shift,
                        txt=document.content[annotation.lb : annotation.ub].replace(u"\r",u"").replace(u"\n",u" ")
                    )
                )
            shift += len(document.content) + NUM_NEWLINES
            cur_id += 1

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser("Concatenate various BRAT files to create a single BRAT file.")
    parser.add_argument("filenames", nargs="+",
                        help="the input files")
    parser.add_argument("--outfilename", "-o", default="out",
                        help='the output file name (default="out")')
    
    args = parser.parse_args()
    main(args.filenames, args.outfilename)
    sys.exit(0)
