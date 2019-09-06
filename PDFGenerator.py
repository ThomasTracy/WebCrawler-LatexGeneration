import os
import random
from pylatex.utils import NoEscape
from pylatex.package import Package
from pylatex.base_classes import Environment, Options
from pylatex.section import Paragraph
from pylatex import Document, Figure, config, Command, UnsafeCommand, Section, Subsection


class THEBIBLIOGRAPHY(Environment):
    """A class to generate a thebibliography environment."""
    escape = False
    content_separator = "\n"


class SPACING(Environment):
    """A class to generate a spacing environment."""
    packages = [Package('setspace')]
    escape = False
    content_separator = "\n"

class MyFigure(Environment):
    """
    A class to generate a figure environment across two rows
    will also be used for asserting equations
    """
    _latex_name = 'figure*'
    packages = [Package('stfloats')]
    escape = False
    content_separator = "\n"

class EQUATION(Environment):
    """A class to generate a equation environment."""
    packages = [Package('amsmath'), Package('amsfonts')]
    escape = False
    content_separator = "\n"

class MULTICOLS(Environment):
    packages = [Package('multicol')]
    escape = False
    content_separator = "\n"


class PDFGenerator:
    """
    A class to generate a thesis-like PDF
    with texts, images, equations and references
    """
    def __init__(self):
        with config.active.change(indent=True):
            self.doc = Document(documentclass='journal', document_options='twocolumn', geometry_options={"top":"2cm", "bottom":"2cm", "left":"2cm", "right":"2cm"})
        self.doc.preamble.append(Command('DeclareUnicodeCharacter', 'FB00', extra_arguments='ff'))
        self.doc.preamble.append(Command('DeclareUnicodeCharacter', 'FB01', extra_arguments='fi'))
        self.doc.preamble.append(Command('DeclareUnicodeCharacter', 'FB02', extra_arguments='fl'))
        self.doc.preamble.append(Command('DeclareUnicodeCharacter', 'FF1A', extra_arguments=':'))
        self.doc.preamble.append(Command('DeclareUnicodeCharacter', '2212', extra_arguments='-'))
        self.doc.preamble.append(Command('DeclareUnicodeCharacter', '1', extra_arguments=' '))
        self.doc.preamble.append(Command('DeclareUnicodeCharacter', 'F8EF', extra_arguments=' '))
        self.doc.append(UnsafeCommand('newcommand', '\myfont', extra_arguments=r'\textit{\textbf{\textsf{Fancy Text}}}'))
        self.doc.append(Command('pagestyle', 'plain'))

    def getReferences(self, font):
        """
        This function is to choose a batch of texts from dataset
        """
        new_refs = []
        # font = random.choice(['rmfamily', 'sffamily', 'ttfamily'])
        with open('Washed_Reference.txt', 'r', encoding='UTF-8') as file:
            reference_data = file.readlines()
        num = random.randint(50, 100)
        refs = random.choices(reference_data, k=num)
        for ref in refs:
            ref = '{\\' + font + ' ' + ref + '}' + '\\newline'
            new_refs.append(ref)
        return new_refs

    def addPic(self):
        """
        This function can randomly insert an image
        with random size
        The image can be either single-row or across two rows
        The caption of an image will be a lorem-ipsum sentence
        """
        mod = random.choice([0, 1])
        scale_width = random.choice([0.5, 0.75, 1])
        scale_height = random.choice([0.5, 0.75, 1, 1.5, 2])
        with open('./lorem-ipsum-caption.txt', 'r', encoding='UTF-8') as f:
            all = f.readlines()
            caption_name = random.choice(all)
        for root, dirnames, filenames in os.walk('./img'):
            img = os.path.join(root + '/', random.choice(filenames))
        if mod == 0:
            with self.doc.create(Figure(position='htbp')) as fig:
                fig.add_image(img, width=NoEscape(r'%f\linewidth'%scale_width))
                fig.add_caption(caption=caption_name)
        else:
            img_name = '{.' + img.split('.')[1] + '}.' + img.split('.')[2]
            with self.doc.create(MyFigure(options='hb')):
                self.doc.append(Command('centering'))
                self.doc.append(Command('includegraphics', options=Options(NoEscape(r'width=%f\textwidth, height=%f\textwidth'%(scale_width,scale_height*0.3))), arguments=NoEscape(img_name)))
                self.doc.append(Command('caption', caption_name))

    def addText(self, font, spacing, size):
        """
        This function can randomly insert several paragraphes of texts
        with randomly choiced font, size and line spacing
        """
        with open('./lorem-ipsum-title1.txt', 'r', encoding='UTF-8') as f:
            all = f.readlines()
            all = [word.strip() for word in all]
            title = ' '.join(random.choices(all, k=random.randint(2,8)))
        for root, dirnames, filenames in os.walk('./text1'):
            file = root + '/' + random.choice(filenames)
        with open(file, 'r', encoding='UTF-8') as f:
            texts = f.readlines()
        text = random.choices(texts, k=4)
        with self.doc.create(SPACING(arguments=spacing)):
            self.doc.append(Command(size))
            with self.doc.create(Section(title, numbering=False)):
                for t in text:
                    if t:
                        t = '{\\' + font + ' \\hspace*{2pt} ' + t + '}' + '\\newline'
                        self.doc.append(NoEscape(t))

    def addReferences(self, font, spacing, size, item_spacing):
        """
        This function can randomly insert a batch of references
        with randomly choiced font, size and line spacing
        """
        self.doc.append(UnsafeCommand('balance', packages=[Package('balance')]))
        item_spacing = str(spacing*float(item_spacing))
        item_spacing = item_spacing+'ex'
        refs = self.getReferences(font)
        mode = random.choice([1,2])
        with self.doc.create(SPACING(arguments=spacing)):
            self.doc.append(Command(size))
            if mode==1:
                with self.doc.create(THEBIBLIOGRAPHY(arguments='99')):
                    self.doc.append(UnsafeCommand('addtolength', '\itemsep', extra_arguments=item_spacing))
                    for ref in refs:
                        ref = '\\bibitem{ref}' + ref
                        self.doc.append(ref)
            else:
                i = 0
                with self.doc.create(Section('References', numbering=False)):
                    for ref in refs:
                        i += 1
                        ref = '{[}'+str(i)+'{]}'+ref
                        self.doc.append(NoEscape(ref))
        self.doc.append(Command('clearpage'))

    def addEquation(self):
        """
        This function is to insert a either single-row or two-rows equation
        """
        # mode=0, single-row. Mode=1, two-row
        mode = 0
        choosed_equations = []
        num = random.randint(1, 3)
        with open('./equation.txt', 'r', encoding='UTF-8') as f:
            equations = f.readlines()
        choosed_equations.extend(random.choices(equations, k=num))
        for equation in choosed_equations:
            if len(equation) > 100:
                mode = 1
                break
        if mode == 1:
            with self.doc.create(MyFigure(options='ht')):
                for equation in choosed_equations:
                    with self.doc.create(EQUATION()):
                        self.doc.append(NoEscape(equation.strip()))
        else:
            for equation in choosed_equations:
                with self.doc.create(EQUATION()):
                    self.doc.append(NoEscape(equation.strip()))

    def generatePDF(self, name):
        """
        This function generate a reasult PDF with randomly calling
        the functions of inserting img, references, or equations.
        To avoid layout problems, every insterted element will be
        wrapped up with texts. So that text does not need to be specific
        inserted
        """
        # control the length of PDF with circulation times
        for i in range(10):
            # the spacing, font, size of text will randomly changed by every iteration
            font = random.choice(['rmfamily', 'sffamily', 'ttfamily'])
            spacing = random.choice([0.5, 1, 1.5, 2])
            opt = random.choice(['footnotesize -3.25', 'small -3.25', 'normalsize -3.5'])
            [size, item_spacing] = opt.split()
            inserted_element = ['text']#['pic', 'ref', 'equation']
            random.shuffle(inserted_element)

            for element in inserted_element:
                if element == 'pic':
                    self.addText(font, spacing, size)
                    self.addPic()
                    self.addText(font, spacing, size)
                if element == 'text':
                    self.addText(font, spacing, size)
                if element == 'equation':
                    self.addText(font, spacing, size)
                    self.addEquation()
                    self.addText(font, spacing, size)
                if element == 'ref':
                    self.addText(font, spacing, size)
                    self.addReferences(font, spacing, size, item_spacing)
                    self.addText(font, spacing, size)

             #self.doc.append(Command('clearpage'))
            print("Finished block: ", i)
        self.doc.generate_pdf(name, clean_tex=False, compiler='pdflatex')
        print("******** Successfully generated PDF! ********")


if __name__ == "__main__":
    pdfGenerator = PDFGenerator()
    pdfGenerator.generatePDF('schlecht')
