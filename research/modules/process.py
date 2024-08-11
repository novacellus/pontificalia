import csv
import re
import os
class Text:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.src_text = []
        self.clean_text = []
        self.normalized_text = []
        self.clean_text_path = ""
        self.normalized_text_path = ""
        #self.spacy_clean = nlp()
    def readFromCsv(self, headers=["Rubric_Name", "Oration_Text"]):
        with open(self.path) as f:
            reader = csv.DictReader(f,delimiter=";")
            for row in reader:
                [self.src_text.append(t) for t 
                 in [row[col] for col in headers] 
                 if t is not None and t.strip() != ""]
    def saveCsv(self, filename):
        with open(filename, 'w') as w:
            w.writelines([line + "\n" for line in self.src_text])

    def cleanText(self):
        def _clean(line):
            line = re.sub(r'[\[\]\+]','', line)
            line = re.sub(r'\n|\s{2,}',' ', line)
            line = re.sub(r'\s*\|\s*','', line)
            return line
        clean_lines = [ _clean(line) for line in self.src_text ]
        for i, line in enumerate(clean_lines):
            if line.strip() == "-":
                clean_lines.pop(i)
            elif not line.strip().endswith("."):
                clean_lines[i] = line.strip() + ":"        
        self.clean_text = clean_lines

    def normalizeText(self):
        def _normalize(line):
            line = line.lower()
            line = re.sub('ę','ae', line)
            line = re.sub('J','I', line)
            line = re.sub('j','i', line)
            line = re.sub('V','U', line)
            line = re.sub('v','u', line)
            line = re.sub('Ih','I', line)
            return line
        if len(self.clean_text) > 0:
            normalized_lines = [ _normalize(line) for line in self.clean_text ]
        else:
            self.cleanText()
            normalized_lines = [ _normalize(line) for line in self.clean_text ]
        self.normalized_text = normalized_lines
    
    def saveText(self, dir="texts"):
        if not os.path.isdir(dir):
            os.mkdir(dir)
        # clean
        filename = self.name + "_" + "clean" + ".txt"
        filepath = os.path.join(dir, filename)
        #print(filepath)
        self.clean_text_path = filepath
        
        with open(filepath, 'w') as w:
            w.writelines([line + "\n" for line in self.clean_text if line.strip() != ("-")])
        
        filename = self.name + "_" + "normalized" + ".txt"
        filepath = os.path.join(dir, filename)
        self.normalized_text_path = filepath
        with open(filepath, 'w') as w:
            w.writelines([line + "\n" for line in self.normalized_text if line.strip() != ("-")])