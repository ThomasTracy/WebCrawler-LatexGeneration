import os
import random
import sys
import re


class DataWashing:
    """
    Class of datawashing, used for references ans texts
    """
    def __init__(self):
        """
        The wash_dict is a dictionary of all to-be-replaced special
        characters. Keys of this dictonary will be replaced with corresponding
        values. e.g. 'α' will be replaced by '$\\alpha$'
        """
        self.wash_dict = {
            'α': r'$\\alpha$',
            'β': r'$\\beta$',
            'γ': r'$\\gamma$',
            'δ': r'$\\delta$',
            '∆': r'$\\Delta$',
            '∈': r'$\\in$',
            'μ': r'$\\mu$',
            'τ': r'$\\tau$',
            'ω': r'$\\$omega$',
            'θ': r'$\\theta$',
            'σ': r'$\\sigma$',
            'λ': r'$\\lambda$',
            '∂': r'$\\partial$',
            'Φ': r'$\\Phi$',
            'ψ': r'$\\Psi$',
            '∀': r'$\\forall$',
            'Σ': r'$\\Sigma$',
            '∗': r'*',
            '⊆': r'$\\subseteq$',
            '∪': r'$\\bigcup$',
            '≈': r'$\\approx$ ',
            '≥': r'$\\geq$ ',
            '≤': r'$\\leq$ ',
            'ﬃ': r'ff',
            'ﬀ': r'ff',
            '≫': r'$\\gg$',
            u'\uf8eb': '',
            u'\uf8ee': '',
        }

    def data_wash_replace_http(self, matched):
        """
        Assert a spacing after every slash in a URL
        so that the URL will wrap
        """
        http = matched.group('http')
        http_list = re.split(r'([/.](?=[^/ ]))', http)
        new_http = ' '.join([''.join(i) for i in zip(http_list[0::2], http_list[1::2])])
        return new_http


    def reference_washing(self):
        """
        Wash the refereces data
        Find and replace special characters with regular expression
        or adjust the set type of some data
        """
        washed_data = []
        with open('Washed_Reference.txt', 'r', encoding='UTF-8') as f:
            datas = f.readlines()
        for data in datas:
            if re.search(r'https*.*?html', data):
                data = re.sub(r'(?P<http>http*.*?html)', self.data_wash_replace_http, data)
            if re.search(r'\D.\n', data):
                data = re.sub(r'\n', ' ', data)
            if re.match(r'\n', data):
                data = re.sub(r'\n', '', data)
            if re.search(r'[^\\]&', data):
                data = re.sub(r'&', r'\&', data)
            if re.search(r'[^\\]#', data):
                data = re.sub(r'#', r'\#', data)
            if re.search(r'<em>', data):
                data = re.sub(r'<em>', r'{\it ', data)
            if re.search(r'</em>', data):
                data = re.sub(r'</em>', r' }', data)
            if re.search(r'[^\\]_', data):
                data = re.sub(r'_', r'\\_', data)
            if re.search(r'[^\\]%', data):
                data = re.sub(r'%', r'\\%', data)
            if re.search(r'∼', data):
                data = re.sub(r'∼', r'-', data)
            washed_data.append(data)
        with open('Washed_Reference.txt', 'w', encoding='UTF-8') as f:
            f.writelines(washed_data)
        print('**************************References Washing Finished**************************')

    def text_washing(self):
        """
        Wash the texts data extracted from PDF
        Find and replace special characters with regular expression
        or adjust the set type of some data
        """
        for root, dirnames, filenames in os.walk('./text'):
            for filname in filenames:
                washed_data = []
                file = root + '/' + filname
                with open(file, encoding='UTF-8') as f:
                    datas = f.readlines()
                if datas:
                    for data in datas:
                        if len(data) < 50:
                            continue
                        for key in self.wash_dict.keys():
                            if re.search(key, data):
                                data = re.sub(key, self.wash_dict[key], data)
                        if re.search(r'https*.*?html', data):
                            data = re.sub(r'(?P<http>http*.*?html)', self.data_wash_replace_http, data)
                        if re.search(r'\(cid:.*?\)', data):
                            data = re.sub(r'\(cid:.*?\)', r'', data)
                        if re.search(r'[^\\]&', data):
                            data = re.sub(r'&', r'\\&', data)
                        if re.search(r'[^\\]_', data):
                            data = re.sub(r'_', r'\\_', data)
                        if re.search(r'[^\\]%', data):
                            data = re.sub(r'%', r'\\%', data)
                        if re.search(r'[^\\]#', data):
                            data = re.sub(r'#', r'\\#', data)
                        if re.search(r'∼', data):
                            data = re.sub(r'∼', r'-', data)
                        if re.search(r'[ \t]+', data):
                            data = re.sub(r'[ \t]+', r' ', data)
                        temp = data.split(' ')
                        for word in temp:
                            if len(word)>40:
                                temp.remove(word)
                        data = ' '.join(temp)
                        washed_data.append(data)
                    with open(file, 'w', encoding='UTF-8') as f:
                        f.writelines(washed_data)
                else:
                    os.remove(file)
                print("File %s washed seccessfully" % file)
        print('**************************Texts Washing Finished**************************')

    def equation_wash(self):
        """
        remove the too short equations
        """
        with open('equation.txt', 'r', encoding='UTF-8') as f:
            equations = f.readlines()
        print("Unwashed length", len(equations))
        equations = list(set(equations))
        for equ in equations:
            if len(equ)<30:
                equations.remove(equ)
        with open('equation1.txt', 'w', encoding='UTF-8') as f:
            f.writelines(equations)
        print("Washed length", len(equations))


if __name__ == "__main__":
    lets_wash_it = DataWashing()