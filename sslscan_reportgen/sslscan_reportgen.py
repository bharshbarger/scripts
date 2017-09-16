#!/usr/bin/env python

#todo: automatically sort IP addresses

try:
    import argparse, os, re, sys
    import docx
    from docx.shared import Pt
    from docx.shared import RGBColor
    from docx.shared import Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.shared import OxmlElement, qn
except Exception as e:
    print('\n[!] Import(s) failed!: ' + str(e))

class sslscan_beautifier():

    def __init__(self, args):

        #defaults
        #pass in args. this is messy
        self.args = args
        #verbosity explicitly off
        self.verbose = False
        #version
        self.version ='beta.09_15_2017'
        self.client=None
        #file to read
        self.ssl_file = None
        self.rc4_dict = {}
        self.sslv3_dict = {}
        self.des_dict = {}
        self.tls10_dict = {}
        self.weakbits_dict = {}
        self.result_dictionary = {}
        self.heartbleed_dict = {}

        #dump reports here
        self.report_dir = './reports/'
        
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

        print('\n**** SSLScan ReportGen ****\n')

    #attempts to validate user supplied args
    def check_args(self, parser):
        #print version and supplied args if verbose
        if self.args.verbose is True: print(\
            '[i] Version: {}\n[i] Options: {}'.format(self.version,parser.parse_args()))

        if self.args.file:
            self.file=self.args.file
        else:
            print ('No file supplied')
            sys.exit(0)

        if self.args.client is None:
            print ('Please provide a client name')
            sys.exit(0)

        #clean up client name, remove spaces and stuff
        self.args.client = ''.join(e for e in self.args.client if e.isalnum())

    def read_file(self):
        #open targets file
        with open(self.file) as f:
            #use a regex to split the file into sections, delimited by the word Testing
            for i, result in enumerate(re.findall('Testing(.*?)Testing', f.read(), re.S)):
                
                
                #look for the first line from the Testing
                # BUG for some reason the regex removes testing from the result
                if 'SSL server' in result:

                    #set up a dictionary key of ip val of the result
                    self.result_dictionary[re.findall(r'(?:\d{1,3}\.)+(?:\d{1,3})', result)[0]] = result

                    '''for key,val in self.result_dictionary.items():
                        print(key, val[0:10])'''


    def parse_dict(self):

        #run through the dictonary containing IPs and the scan results as keys
        for key,val in self.result_dictionary.items():
            #for each line of the scan output
            #print(key)
            for line in val.splitlines():

                #look for RC4
                if 'RC4' in line:
                    self.rc4_dict[key]=line
        
                if 'SSLv3' in line:
                    self.sslv3_dict[key]=line
                
                if 'DES' in line:
                    self.des_dict[key]=line
                
                if 'TLSv1.0' in line:
                    self.tls10_dict[key]=line
                
                if 'bits' in line:
                    bits=line.split()[2]
                    if int(bits) < 128:
                        self.weakbits_dict[key]=line

                if 'to heartbleed' in line:
                    if not 'not' in line:
                        self.heartbleed_dict[key]=line

    def gen_report(self):
        #create a document 
        document = docx.Document()

        print ('\n**** Generating Report ****\n')
        #optional header
        '''heading = document.add_heading(level=3)
        runHeading = heading.add_run('weak ssl stuff')
        font=runHeading.font
        font.name = 'Arial'
        font.color.rgb = RGBColor(0xe9,0x58,0x23)'''
        

        paragraph = document.add_paragraph()
        #start by printing the ip address in 20pt arial

        for key,val in self.result_dictionary.items():

            runParagraph = paragraph.add_run(key)
            font=runParagraph.font
            font.name = 'Arial'
            font.size = Pt(20)
            runParagraph = paragraph.add_run('\n')
            if self.args.verbose is True:print('Added naughty host: {}'.format(key))
            
            
            #if this host had RC4, print the header
            runParagraph = paragraph.add_run('RC4 Support\n')
            font=runParagraph.font
            font.name = 'Arial'
            font.size = Pt(16)
            #enumerate the lines were rc4 was found
            for i,r, in self.rc4_dict.items():
                runParagraph = paragraph.add_run(r)
                font=runParagraph.font
                font.name = 'Arial'
                font.size = Pt(11)
                runParagraph = paragraph.add_run('\n')

            #if this host had sslv3, print the header
            runParagraph = paragraph.add_run('SSLv3 Support\n')
            font=runParagraph.font
            font.name = 'Arial'
            font.size = Pt(16)
            #enumerate the lines were rc4 was found
            for i,r, in self.sslv3_dict.items():
                runParagraph = paragraph.add_run(r)
                font=runParagraph.font
                font.name = 'Arial'
                font.size = Pt(11)
                runParagraph = paragraph.add_run('\n')
        

            runParagraph = paragraph.add_run('DES Support\n')
            font=runParagraph.font
            font.name = 'Arial'
            font.size = Pt(16)
            #enumerate the lines were rc4 was found
            for i,r, in self.des_dict.items():
                runParagraph = paragraph.add_run(r)
                font=runParagraph.font
                font.name = 'Arial'
                font.size = Pt(11)
                runParagraph = paragraph.add_run('\n')


            runParagraph = paragraph.add_run('TLS v1.0\n')
            font=runParagraph.font
            font.name = 'Arial'
            font.size = Pt(16)
            #enumerate the lines were rc4 was found
            for i,r, in self.tls10_dict.items():
                runParagraph = paragraph.add_run(r)
                font=runParagraph.font
                font.name = 'Arial'
                font.size = Pt(11)
                runParagraph = paragraph.add_run('\n')


            runParagraph = paragraph.add_run('Weak key size \n')
            font=runParagraph.font
            font.name = 'Arial'
            font.size = Pt(16)
            #enumerate the lines were rc4 was found
            for i,r, in self.weakbits_dict.items():
                runParagraph = paragraph.add_run(r)
                font=runParagraph.font
                font.name = 'Arial'
                font.size = Pt(11)
                runParagraph = paragraph.add_run('\n')

            runParagraph = paragraph.add_run('Heartbleed \n')
            font=runParagraph.font
            font.name = 'Arial'
            font.size = Pt(16)
            #enumerate the lines were rc4 was found
            for i,r, in self.heartbleed_dict.items():
                runParagraph = paragraph.add_run(r)
                font=runParagraph.font
                font.name = 'Arial'
                font.size = Pt(11)
                runParagraph = paragraph.add_run('\n')

        
        
        document.save('{}sslscan_{}.docx'.format(self.report_dir, self.args.client))


    def print_summary(self):
        print('********RC4 Hosts********')
        for k,v in self.rc4_dict.items():
            print('{}'.format(k))
        print('********SSLv3 Hosts********')
        for k,v in self.sslv3_dict.items():
            print('{}'.format(k))
        print('********DES Hosts********')
        for k,v in self.des_dict.items():
            print('{}'.format(k))
        print('********TLS v1.0 Hosts********')
        for k,v in self.tls10_dict.items():
            print('{}'.format(k))
        print('********Weak Key Size********')
        for k,v in self.weakbits_dict.items():
            print('{}'.format(k))


def main():
    #gather options
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client', metavar='<client>', help='client name')
    parser.add_argument('-f', '--file', metavar='<file>', help='file to read')
    parser.add_argument('-v', '--verbose', help='Optionally enable verbosity', action = 'store_true')
    args = parser.parse_args()
    run = sslscan_beautifier(args)
    run.check_args(parser)
    run.read_file()
    run.parse_dict()
    run.print_summary()
    run.gen_report()



if __name__ == '__main__':
    main()
