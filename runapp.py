import os
import typer
from takehome import readFile

def main(fname, oname):
    readFile(fname,oname)

if __name__=="__main__":
    typer.run(main)
