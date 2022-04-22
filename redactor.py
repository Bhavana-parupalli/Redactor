import argparse
from project1 import project1 as p1
import glob

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("--input", required=True, action='store', nargs='+', type=glob.glob)
    parser.add_argument("--names", action="store_true")
    parser.add_argument("--dates", action="store_true")
    parser.add_argument("--phones", action="store_true")
    parser.add_argument("--genders", action="store_true")
    parser.add_argument("--address", action="store_true")
    parser.add_argument("--concept", type=str)
    parser.add_argument("--output", required=True, type=str)
    parser.add_argument("--stats")

    args=parser.parse_args()

    f=[]
    for i in args.input:
        f.extend(i)

    for i in range(0,len(f)):
        file=f[i]
        doc=p1.inputfiles(file)
        doc_stats=doc

        if args.names==True:
            (doc,redacted_names)=p1.names(doc)
        if args.dates==True:
            (doc,redacted_dates)=p1.dates(doc)
        if args.phones==True:
            (doc,redacted_phones)=p1.phone_numbers(doc)
        if args.genders==True:
            (doc,redacted_genders)=p1.gender(doc)
        if args.address==True:
            (doc,redacted_genders)=p1.address(doc)
        if args.concept:
            w=args.concept
            (doc,redacted_concept)=p1.concept(doc,w)
        if args.output:
            path=args.output
            filename=file
            p1.output(doc,filename,path)
        if args.stats:
            stats_path=args.stats
            k=i
            k+=1
            p1.stats(doc_stats, stats_path, k, args.concept)



