'''
This is written in python2.

I because we don't have the URL which is reacted, some of the notes here
are my best interpretation.

The imports:
subprocess - allows you to create new processes from the python script.
   subprocesses are child processes created from another process.
urllib - allows you to retrieve resources from URL.
random - generates pseudo-random numbers (i.e. not truly random numbers)
sys - imported later. Enables access to parameters and functions specific
   to the machine that is running the code.
'''

import subprocess, urllib, random
'''
    This is a custom exception class, that when raised, causes the whole script to exit.
'''
class NoBlocks(Exception): pass
'''
    This function reads from a URL which has been reacted by the courts.
    It looks like this function called to custom url which was likely
    set up by Swartz himself, which had a list of URLs linking to PDFs to
    download.

    It is likely the case that Swartz had this grab page setup and would
    control and modify it from out side of the MIT campus in order to
    direct the script to download the PDFs he wanted.

    The first line in this function calls urllib.urlopen().read and saves the
    response of this call to a variable called 'r'. The urlopen function
    reads from a URL and returns a file-like object from the contents of the
    external resource that the URL points to. The read function that is called
    on this simply reads the byte contents and returns them.

    The second line of this function checks to see if there is HTMl in the
    retrieved page. If there is then it raises a NoBlocks exception and
    exits the script. It is likely that the URL that is reacted simply
    was a text file with the PDFs Swartz wanted to download. When he
    wanted to stop the script he could simply swap this text file for a HTML
    file and the script would exit.

    The split function simply takes a string and splits it into a list and by
    default, it will split the string at every space, which is what Aaron is
    doing here.
'''
def getblocks():
    r = urllib.urlopen("http://{?REDACTED?}/grab").read()
    if '<html' in r.lower(): raise NoBlocks
    return r.split()

'''
    The next 5 lines of code are concerned with taking the arguments to the
    script from the sys.argv and if there is one present adding it to a
    variable as a list with the string --socks5 as the first string in the list.

    Note that it takes the second element in the sys.argv list as the first
    element in the sys.argv list is the name of the script.

    This prefix variable will be used in a lamda expression below.

    Basically, this prefix is used to make the script connect to JSTOR via a
    proxy or just though the computer's internet connection (which Aaron left
    a command about, suggesting this was an ethernet connection, which makes
    sense as the computer that Aaron used to run this script was in a store
    cupboard connected to the MIT network)

    This line may mean that Aaron could run this script from outside the
    MIT network, but that is just speculation.
'''
import sys
if len(sys.argv) > 1:
    prefix = ['--socks5', sys.argv[1]]
else:
    prefix = []#'-interface','eth0:1']
'''
    The next line declares a lambda function which is saved to the variable
    called line.

    This lambda expression takes a single argument, which is the name of the
    PDF that the script is going to download.

    This lambda expression will later be used as part of a subprocess call
    later in the script.

    It defines a curl request. The curl command is a command which allows you
    to transfer data to or from a URL, i.e upload or download from a url.
    The curl request is with a proxy to connect via (depending on the
    conditional above as mentioned). Next, it defines a cookie, which is simply
    the string TENACIOUS= followed by a random 3-digit number. This cookie,
    will make the server responding to this curl request think that it is coming
    from a real user as opposed to a script. The next thing this function does
    is define the output of this curl request: the pdf file name to a directory
    called pdfs. The rest of this lambda creates the url of the PDF from which
    to download the PDF with using curl.

'''
line = lambda x: ['curl'] + prefix + ['-H', "Cookie: TENACIOUS=" + str(random.random())[3:], '-o', 'pdfs/' + str(x) + '.pdf', "http://www.jstor.org/stable/pdfplus/" + str(x) + ".pdf?acceptTC=true"]

'''
    This next section of code. Defines an infinite loop, which is the part of
    the code that composes everything else.

    First it calls the getblocks from earlier and saves the resuling list of
    PDFs to a variable called blocks.

    It then iterates over these, printing them to the console and then calling
    the line lambda from earlier in a subprocess.Popen call. Subprocess Popen
    will create a new process, in this case the curl request that will
    download the current PDF. Then the script will block until this subprocess
    finishes, i.e. it will wait until the PDF is finished downloading and then
    it will move on to the next PDF.
'''
while 1:
    blocks = getblocks()
    for block in blocks:
        print block
        subprocess.Popen(line(block)).wait()
