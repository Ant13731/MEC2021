import csv
import tkinter as tk
#from tabulate import tabulate #doesnt work in vscode for some reason, only IDLE

HEIGHT = 1000
WIDTH = 1200

def readVotesFromFile():
    '''Takes in a csv file of all the voters and then sorts them into a dictionary for convenience.'''
    #Replace filepath with MEC Competition Voting Data.csv
    with open("C:\\Users\\Ant13731\\Desktop\\Anthony McMaster Main\\Fall 2021\\MEC\\MEC Competition Voting Data.csv", "r") as myFile:
        read = csv.reader(myFile)
        dataTable = []
        for row in read:
            dataTable += [row]

    dataTable = dataTable[1:]

    myDictionary = dict()
    for r in dataTable:
        name = r[0] + ' ' + r[1]
        vote = r[2]
        if name not in myDictionary:
            if ',' not in vote:
                myDictionary[name] = vote
    return myDictionary

def getNameFromID():
    return []

voterDatabase = readVotesFromFile()
authenticatedNames = getNameFromID()

class Voter():
    name = ""
    votingParty = ""
    authenticated = False
    def voterName(self, s):
        self.name = s
    def vote(self, party):
        self.votingParty = party
    def checkAuthentication(self):
        if self.name in authenticatedNames:
            self.authenticated = True
        else:
            self.authenticated = True #TODO make this false

def initializeUser(name, party):
    '''Initialize a voter given the voters name and party'''
    user = Voter()
    user.voterName(name)
    user.vote(party)
    #print(name + ' voted for ' + party)
    return user

def authenticateAndVote(name, party, d):
    '''Only cast vote if user is authenticated. Otherwise, do nothing'''
    user = initializeUser(name, party)
    user.checkAuthentication()
    if user.authenticated:
        if user.name not in d:
            if ',' not in user.votingParty:
                d[user.name] = user.votingParty

def voteCount(d):
    '''Returns a dictionary with the parties and how many votes each party received'''
    partyD = dict()
    for entry in d:
        if d[entry] in partyD:
            partyD[d[entry]] += 1
        else:
            partyD[d[entry]] = 1
    return partyD

def orderVotes(d):
    '''Turns a dictionary of votes into a list sorted by most popular vote'''
    return sorted(d.items(), key=lambda x: x[1])[::-1]

def orderVotesWithHeader(d):
    '''Prepend column titles to the list of parties and their votes'''
    return [("Party", "Number of Votes")] + orderVotes(d)

def displayVoteCount(d):
    '''Display votes in a table'''
    l = orderVotesWithHeader(d)
    # change this back in the end
    # formatVotes = tabulate(l, headers="firstrow")
    # and comment this out too when the change is made

    #Uncomment if tabulate is not installed (not as nice of a format, but will always work)
    formatVotes = ''
    for entry in l:
        formatVotes += entry[0] + " | " + str(entry[1]) + '\n'
    return formatVotes

    
root = tk.Tk()

canvas = tk.Canvas(root,height= HEIGHT, width=WIDTH,bg='#a5f0f0')
canvas.pack()

background = tk.Frame(root,bg='#a5f0f0')
background.place(relx = 0.5, rely = 0, relwidth=1, relheight=1, anchor='n')

lower_frame = tk.Frame(root, bg='#a5f0f0', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

mainBox = tk.Label(lower_frame, font = ('Courier', 20),bg = '#c4f9ff')
mainBox.place(relwidth=1, relheight=1)

def updateVote(d):
    '''Update the main text box with vote counts'''
    mainBox['text'] = displayVoteCount(voteCount(d))
    
updateButtonFrame = tk.Frame(root, bg='#a5f0f0', bd=5)
updateButtonFrame.place(relx=1.1, rely=0.05, relwidth=1, relheight=0.1, anchor='n')

updateButton = tk.Button(updateButtonFrame, text= "Get Voting Results", bg='#5390D9', fg='black', font=('Courier',20), command=lambda : updateVote(voterDatabase))
updateButton.place(relheight=1, relwidth=0.3)

inputBoxUsername = tk.Frame(root, bg='#a5f0f0', bd=5)
inputBoxUsername.place(relx=0.3, rely = 0.05, relwidth=0.4, relheight=0.05, anchor='n')

username = tk.Entry(inputBoxUsername, font=('Courier',40),bg='#73B0F9')
username.place(relwidth=1, relheight=1)

inputBoxVote = tk.Frame(root, bg='#a5f0f0', bd=5)
inputBoxVote.place(relx=0.3, rely = 0.1, relwidth=0.4, relheight=0.05, anchor='n')

voteParty = tk.Entry(inputBoxVote, font=('Courier',40),bg='#73B0F9')
voteParty.place(relwidth=1, relheight=1)

votePartyLabelBox = tk.Frame(root, bg='#a5f0f0', bd=5)
votePartyLabelBox.place(relx=0.05, rely = 0.11, relwidth=0.1, relheight=0.05, anchor='n')

votePartyLabel = tk.Label(votePartyLabelBox, font = ('Courier', 10), bg = '#a5f0f0')
votePartyLabel.place(relwidth = 1, relx = 0)
votePartyLabel['text'] = "Party Name:"

usernameLabelBox = tk.Frame(root, bg='#a5f0f0', bd=5)
usernameLabelBox.place(relx=0.05, rely = 0.06, relwidth=0.1, relheight=0.05, anchor='n')

usernameLabel = tk.Label(usernameLabelBox, font = ('Courier', 10), bg = '#a5f0f0')
usernameLabel.place(relwidth = 1, relx = 0)
usernameLabel['text'] = "Name:"

titleFrame = tk.Frame(root, bg='#a5f0f0', bd=5)
titleFrame.place(relx=0.3, rely = 0, relwidth=0.25, relheight=0.05, anchor='n')

titleLabel = tk.Label(titleFrame, font = ('Courier', 14), bg = '#a5f0f0')
titleLabel.place(relwidth = 1, relx = 0)
titleLabel['text'] = "Vote For a Candidate!"

inputButtonFrame = tk.Frame(root, bg='#a5f0f0', bd=5)
inputButtonFrame.place(relx=0.3, rely=0.175, relwidth=0.35, relheight=0.05, anchor='n')

#TODO authenticate too
loginButton = tk.Button(inputButtonFrame, text= "Authenticate and Vote!", bg='#5390D9', fg='black', font=('Courier',20), command=lambda : authenticateAndVote(username.get(), voteParty.get(), voterDatabase))
loginButton.place(relheight=1, relwidth=1)

lower_frame = tk.Frame(root, bg='#a5f0f0', bd=10)
lower_frame.place(relx=0.5,rely=0.85,relwidth=1,relheight=0.15,anchor='n')

prompt = tk.Label(lower_frame, font = ('Courier', 20), bg='#48BFE3')
prompt.place(relwidth=1,relheight=1,rely = -0.05)
prompt['text'] = "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nPlease enter your name and the party you want to vote for\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

root.mainloop()
