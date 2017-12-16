# BinBashCord
BinBash for the Discord age

**BinBash** is Discord (formerly IRC) quote bot specializing in seperate textual quote files 
for different purposes. In its original incarnation on *irc.slashnet.org*
channel *#mzx*, it replaced !<nick>bash scripts that were used to chronicle funny 
quotes from mostly former community members.

## Usage:

Edit the binbash.py script, putting in the token, channel ids, authorized roles
for adding quotes, etc that your bot will use. Place text files containing quotes in the 
bashes folder, see the examples in that folder. Run the bot with python 
binbash.py. The script will automatically split messages at 2000
characters if needbe.

Enjoy.

## Commands:

!bashes - Shows a listing of files in the bashes/ folder
!foobash n - n is a line number. If n is specified, show the nth line from foo.txt, if it is not specified, show a random line from foo.txt
!addquote foo This is a quote - Add the line "This is a quote" to the end of foo.txt, creating foo.txt if necessary.
