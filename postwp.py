# You may need to:
#    pip install python-wordpress-xmlrpc

RPC_URL='http://127.0.0.1/html/wordpress/xmlrpc.php'
RPC_USR='admin'
RPC_PWD='password'

""" Essay Configuration """
#   Essays are the things that prompt you to fill in a story. VIM loads for each report section.
REPORT_ESSAYS     = ['What was the most challanging part of your day?', 'Who did you shadow in support?']

import os, subprocess, tempfile # for strfromvim class.
class strfromvim():
    """ Will open up vim, and capture your string input as variable.
        Supports optional welcome screen arguement to set initial text.
        Requires: import os, subprocess, tempfile
        
        NEW: Opens you up at the end of the file.
        Example:
            vim = strfromvim()
            vim.getinput('Welcome to vim!',True)
            print vim.output            """
    def __init__(self):
        (self.fd, self.path)  = tempfile.mkstemp()   # Makes in /tmp
    def getinput(self,welcomescreen='',dashes=False):
        self.fp = os.fdopen(self.fd, 'w')
        if dashes:
            self.fp.write(welcomescreen+"\n================================================\n\n")
        else:
            self.fp.write(welcomescreen) 
        self.fp.close() 

        OS_EDITOR = os.getenv('EDITOR', 'vi')
        #print(OS_EDITOR, self.path)
        # The + symbol in %s + %s is to open vim at bottom of file. CTRL G for you.
        subprocess.call('%s + %s' % (OS_EDITOR,self.path), shell=True)

        with open(self.path, 'r') as f:
            self.output = f.read()
        
        os.unlink(self.path)
        

# Aquire report body using vim and stuff.
shiftreportbody = 'Nebops Shiftreport\n\nBEGIN;\n'      
for question in REPORT_ESSAYS:
    
    print question
    ans = raw_input('   -> Do you want to answer? [ y or n ] ')
    if ans == 'y' or ans == 'yes' or ans == 'YES' or ans == 'Y':
        vim = strfromvim()
        vim.getinput(question,True)
        shiftreportbody += vim.output + "\n"
shiftreportbody += "\nEND;"




import datetime
def return_shift_based_on_time():
    """ Unimplemented """
    currenthour = datetime.time().strftime('%H')
    return "1st"

def return_post_title():
    """ Unimplemented """
    print return_shift_based_on_time()

print "POSTED <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
print shiftreportbody
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"


from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

client = Client(RPC_URL,RPC_USR,RPC_PWD)
post = WordPressPost()
post.title = 'LOL WHAT A TITLE'
post.content = shiftreportbody
post.post_status = 'publish'
post.id = client.call(NewPost(post))

