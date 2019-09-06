import importlib
import json
import os
import random
import sys
import re

importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, PDFTextExtractionNotAllowed
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams


def pdfs_to_texts():
    """
    Extract texts from given PDFs and save them to txt
    """
    file = './pdf'
    for root, dirnames, filenames in os.walk(file):
        for name in filenames:
            pdf_to_text(root, name)
        print("file %s is ready"%name)


def pdf_to_text(root, name):
    file_name = re.sub('.pdf', '', name)
    print(root + '/' + name)
    fullname = root + '/' + name
    fp = open(fullname, 'rb')
    praser = PDFParser(fp)
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()
    if doc.is_extractable:
        manager = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(manager, laparams=laparams)
        intepreter = PDFPageInterpreter(manager, device)
        for page in doc.get_pages():
            intepreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if(isinstance(x, LTTextBoxHorizontal)):
                    text = x.get_text()
                    text = re.sub(r'\n', '', text)
                    with open('./text1/%s.txt' % file_name, 'a+', encoding='utf-8') as f:
                        f.writelines(text + '\n')
    else:
        raise PDFTextExtractionNotAllowed


if __name__ == "__main__":
    pdfs_to_texts()


