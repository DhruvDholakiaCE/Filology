from tkinter import *
from  tkinter import filedialog
import os as opsys
import tkinter.ttk as ttk
from shutil import *
from tkinter.messagebox import *
import threading


root = Tk()
# root.geometry('1920x1080')
root.title('Filology')

# root.iconbitmap('C:/Users/dhruv/Desktop/Files_26987.ico')
#Global Data containers
docs = {}
videos = {}
pics = {}
audios = {}
directory = ''
type = 'All'
searchedRecords = 0
state = 'Videos'
reverseSize = False
reverseName = True

#Configuring style for treeview
style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, background = '#E8E8E8', fieldbackground = '#E8E8E8',font=('Calibri', 15), rowheight = 30) # Modify the font of the body
#,background="yellow",foreground="black", fieldbackground="yellow" #color change
style.configure("mystyle.Treeview.Heading", font=('Calibri', 20,'bold')) # Modify the font of the headings
# style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

#Copyright Frame
copyrightFrame = Frame(root, bg = 'grey')
copyrightFrame.pack(side = BOTTOM, fill = X)

copyrightNameLable = Label(copyrightFrame, text = 'Copyright @Dhruv_Dholakia', bg = 'grey', font = 'arial 13 bold', fg = 'white')
copyrightNameLable.pack(side = RIGHT)


#bottom frame
contentFrame = Frame(root, bg = 'grey')
contentFrame.pack(side = BOTTOM, expand = True, fill = BOTH)


#Nested content frame for Buttons
nestedContedFrame = Frame(contentFrame, bg = 'grey')
nestedContedFrame.pack(side = TOP, padx = 180, fill = X)

#Making TreeView in ContentFrame
treev = ttk.Treeview(contentFrame,style="mystyle.Treeview", selectmode='extended')
treev.pack( side = BOTTOM, expand = True, fill = BOTH, padx= 100, pady = 7)


# Constructing vertical scrollbar with treeview
verscrlbar = Scrollbar(treev,orient="vertical",command=treev.yview)
verscrlbar.pack(side='right', fill= Y)

#Setting Tree columns and style
treev.configure(yscrollcommand=verscrlbar.set)
treev["columns"] = ('No.','FileName', 'Size', 'Unit')

treev.column("#0", anchor='c', width = 150, stretch= NO)
treev.column("No.", anchor='c', width = 50, stretch= NO)
treev.column("FileName", width = 1370, anchor='w',stretch= NO)
treev.column("Size", anchor='e', width = 100, stretch= NO)
treev.column("Unit", anchor='w', width = 36,stretch= NO)

treev.heading("#0", text = 'Type',anchor = 'c')
treev.heading("No.", text = 'No.',anchor = 'c')
treev.heading("Unit", text = '',anchor = 'c')


#Sort By Name A-Z or Z-A
def sortItByName():
    global type, reverseName, reverseSize
    target = {}
    if state == 'Videos':
        target = videos
        showVideos(type)
    elif state == 'Audios':
        target = audios
        showAudios(type)
    elif state == 'Documents':
        target = docs
        showDocs(type)
    elif state == 'Pictures':
        target = pics
        showPics(type)
    sortedList = {}
    print('reverseName : ', reverseName)
    if reverseName:
        clearTree()
        print('code is in reverse true')
        for i in target:
            sortedList[i] = sorted(target[i], reverse= reverseName)

        if len(sortedList) == 0:
            noData()
        else:
            if type != 'All':
                cntr = 1
                lenOfType = len(sortedList[type])
                row = treev.insert("", 'end', text=type + '  (' + str(lenOfType) + ')', values=('', ''), open=True)
                for i in sortedList[type]:
                    size, unit = sizeConversion(i[1])
                    treev.insert(row, 'end', values=(str(cntr), i[0], size, unit))

                    cntr += 1
            else:
                cntr = 1
                for i in sortedList:
                    lenOfType = len(sortedList[i])
                    row = treev.insert("", "end", text=i + '  (' + str(lenOfType) + ')', values=('', ''), open=True)
                    for j in sortedList[i]:
                        size, unit = sizeConversion(j[1])
                        treev.insert(row, 'end', values=(str(cntr), j[0], size, unit))
                        cntr += 1
                    cntr = 1


    print('code is reaching here ', reverseName)
    reverseName = not reverseName
    reverseSize = False
treev.heading("FileName", text = 'File Name',anchor = 'c', command=sortItByName)



#Soting the elements by size KB - GB or GB - KB

def sortItBySize():
    global reverseSize, reverseName
    target = {}
    if state == 'Videos':
        target = videos
    elif state == 'Audios':
        target = audios
    elif state == 'Documents':
        target = docs
        print('docs')
    elif state == 'Pictures':
        target = pics
    print(target, docs, state)
    clearTree()
    sortedList = {}

    for i in target:
        sortedList[i] = sorted(target[i], key = lambda j : j[1], reverse= reverseSize)
        print(sortedList)
    reverseSize = not reverseSize
    print(sortedList)
    if len(sortedList) == 0:
        noData()
    else:
        if type != 'All':
            cntr = 1
            lenOfType = len(sortedList[type])
            row = treev.insert("", 'end', text=type + '  (' + str(lenOfType) + ')', values=('',''), open=True)
            for i in sortedList[type]:
                size,unit = sizeConversion(i[1])
                treev.insert(row,'end', values = (str(cntr) ,i[0], size, unit ))

                cntr+=1
        else:
            cntr = 1
            for i in sortedList:
                lenOfType = len(sortedList[i])
                row = treev.insert("", "end", text=i+'  (' + str(lenOfType) + ')', values = ('',''), open=True)
                for j in sortedList[i]:
                    size, unit = sizeConversion(j[1])
                    treev.insert(row,'end', values = (str(cntr) ,j[0], size,unit))
                    cntr+=1
                cntr =1
            print('Executed......')

    reverseName = False      #maintain the other column state to its default
treev.heading("Size", text = 'Size',anchor = 'c', command= sortItBySize)




#Playing A Selected File WIth Double click event
def play(event):
    item = treev.identify('item', event.x, event.y)
    opsys.startfile(directory + treev.item(item, "value")[1])

treev.bind("<Double-1>", play)

#converting size
def sizeConversion(size):
    if size/1024 < 1024:
        return "{:.2f}".format(size/(1024)), 'KB'
    elif size in range(1024, (1024 * 1024 * 1024) + 1):
        return "{:.2f}".format(size/(1024 * 1024)) , 'MB'
    elif size >= 1024 * 1024 * 1024:
        return "{:.2f}".format(size/(1024*1024*1024)) , 'GB'

#reverse Size Conversion
def revSizeConversion(size, unit):
    size = size
    unit = unit
    if unit == 'KB':
        return size * 1024
    elif unit == 'MB':
        return size * 1024 * 1024
    elif unit == 'GB':
        return size * 1024 * 1024 * 1024

#Clear the components of treeview
def clearTree():
    x = treev.get_children()
    for item in x:
        treev.delete(item)


#display NODATA if data is not available
def noData():
    clearTree()
    for i in range(3):
        treev.insert('', 'end', values=('', ''))
    treev.insert('', 'end', values=('', 'NO DATA AVAILABLE'))
noData()


#Focusing on current type
def updateFocus(button):
    global state, reverseSize, reverseName, type
    bList = [audioButton,videoButton,docsButton,picsButton]
    for i in bList:
        if button in i['text']:
            i['bg'] = 'skyblue'
            state = i['text'].split(' : ')[0]

        else:
            i['bg'] = 'white'

    type = 'All'


#Compopnents (BUTTON) of SubContentFrame

def showVideos(type = 'All'):
    global directory
    clearTree()
    updateFocus('Video')
    if len(videos) == 0:
        noData()
    else:
        if type != 'All':
            cntr = 1
            lenOfType = len(videos[type])
            row = treev.insert("", 'end', text=type + '  (' + str(lenOfType) + ')', values=('',''), open = True)
            for i in videos[type]:
                size,unit = sizeConversion(i[1])
                treev.insert(row,'end', values = (str(cntr) ,i[0], size, unit ))

                cntr+=1
        else:
            cntr = 1
            for i in videos:
                lenOfType = len(videos[i])
                row = treev.insert("", "end", text=i+'  (' + str(lenOfType) + ')', values = ('',''), open = True)
                for j in videos[i]:
                    size, unit = sizeConversion(j[1])
                    treev.insert(row,'end', values = (str(cntr) ,j[0], size,unit))
                    cntr+=1
                cntr =1

videoButton = Button(nestedContedFrame, text = 'Videos : ' + str(len(videos)), command = showVideos, font = 'times 15 bold')
videoButton.pack(side = LEFT, padx = 30, pady = 10)



def showAudios(type = 'All'):
    clearTree()
    updateFocus('Audio')
    if len(audios) == 0:
        noData()
    else:
        if type != 'All':
            cntr = 1
            lenOfType = len(audios[type])
            row = treev.insert("", 'end', text=type + '  (' + str(lenOfType) + ')', values=('', ''), open = True)
            for i in audios[type]:
                size, unit = sizeConversion(i[1])
                treev.insert(row, 'end', values=(str(cntr), i[0], size,unit))
                cntr += 1
        else:
            cntr = 1
            for i in audios:
                lenOfType = len(audios[i])
                row = treev.insert("", "end", text=i + '  (' + str(lenOfType) + ')', values=('', ''), open = True)
                for j in audios[i]:
                    size, unit = sizeConversion(j[1])
                    treev.insert(row, 'end', values=(str(cntr), j[0], size,unit))
                    cntr += 1
                cntr = 1

audioButton = Button(nestedContedFrame, text = 'Audios : ' + str(len(audios)), command = showAudios,font = 'times 15 bold')
audioButton.pack(side = LEFT, padx = 30,pady = 10)



def showDocs(type = 'All'):
    clearTree()
    updateFocus('Doc')
    if len(docs) == 0:
        noData()
    else:
        if type != 'All':
            cntr = 1
            lenOfType = len(docs[type])
            row = treev.insert("", 'end', text=type + '  (' + str(lenOfType) + ')', values=('', ''), open = True)
            for i in docs[type]:
                size, unit = sizeConversion(i[1])
                treev.insert(row, 'end', values=(str(cntr), i[0], size,unit))

                cntr += 1
        else:
            cntr = 1
            for i in docs:
                lenOfType = len(docs[i])
                row = treev.insert("", "end", text=i + '  (' + str(lenOfType) + ')', values=('', ''), open = True)
                for j in docs[i]:
                    size, unit = sizeConversion(j[1])
                    treev.insert(row, 'end', values=(str(cntr), j[0], size,unit))
                    cntr += 1
                cntr = 1

docsButton = Button(nestedContedFrame, text = 'Documents : ' + str(len(docs)), command = showDocs,font = 'times 15 bold')
docsButton.pack(side = LEFT, padx= 30,pady = 10)



def showPics(type = 'All'):
    clearTree()
    updateFocus('Pic')
    if len(pics) == 0:
        noData()
    else:
        if type != 'All':
            cntr = 1
            lenOfType = len(pics[type])
            row = treev.insert("", 'end', text=type + '  (' + str(lenOfType) + ')', values=('', ''), open = True)
            for i in pics[type]:
                size, unit = sizeConversion(i[1])
                treev.insert(row, 'end', values=(str(cntr), i[0], size,unit))
                cntr += 1
        else:
            cntr = 1
            for i in pics:
                lenOfType = len(pics[i])
                row = treev.insert("", "end", text=i + '  (' + str(lenOfType) + ')', values=('', ''), open = True)
                for j in pics[i]:
                    size, unit = sizeConversion(j[1])
                    treev.insert(row, 'end', values=(str(cntr), j[0], size,unit))
                    cntr += 1
                cntr = 1

picsButton = Button(nestedContedFrame, text = 'Pictures : ' + str(len(pics)), command = showPics,font = 'times 15 bold')
picsButton.pack(side = LEFT, padx= 30,pady = 10)




topFrame = Frame(root)
topFrame.pack(side = LEFT,padx = 200)
#entry dir with label

entry_lable = Label(topFrame,text = 'Directory : ', font = 'times 15 bold')
entry_lable.pack(side = LEFT, padx = 10, pady = 10)
entry_box = Entry(topFrame, width = 20, font = 'times 13 bold' )
entry_box.pack(side = LEFT)


#Selecting File Directory and updating entry box

def selectDirectory():
    filedirectory = filedialog.askdirectory()
    entry_box.delete(0,END)
    entry_box.insert(0,filedirectory)
    print(filedirectory)

fileDirButton = Button(topFrame, text = 'Browse', font = 'times 12 bold', command = selectDirectory)
fileDirButton.pack(side = LEFT, pady = 15, padx = 5)


#Setting Default Types
videoTypes = ['mkv','mp4']
documentTypes = ['pdf','xls','txt']
audioTypes = ['mp3','wav','aac', 'wma']
picTypes = ['jpg','png', 'JPG', 'PDF']

#Combobox for file types
listTypes = ['All']
listTypes.extend(videoTypes)
listTypes.extend(audioTypes)
listTypes.extend(documentTypes)
listTypes.extend(picTypes)

#Entry Type With Combobox
entry_type_lable = Label(topFrame,text = 'Type : ', font = 'times 15 bold')
entry_type_lable.pack(side = LEFT, padx = 10, pady = 10)
comboExample = ttk.Combobox(topFrame, values= listTypes, font = 'times 13 bold')
comboExample.current(0)
comboExample.pack(side = LEFT, padx = 10, pady = 10)



#Getting Information acc to Input with ShowInfo Button
def getInfo():

    global videos, docs, audios, pics, directory, type
    videos,docs,audios,pics ={},{},{},{}
    directory = entry_box.get()
    if not directory.endswith('\\') and not directory.endswith('/') and not directory.endswith('\\'):
        directory += '\\'
    # type = entry_type_box.get()
    type = comboExample.get()
    for i in opsys.listdir(directory):

        checkForTypes = i.split('.')
        if len(checkForTypes) > 1:
            if checkForTypes[-1] in videoTypes:
                size = opsys.stat(directory + i)[6]

                if checkForTypes[-1] not in videos:
                    videos[checkForTypes[-1]] = [(i, size)]
                else:
                    videos[checkForTypes[-1]].append((i, size))


            elif checkForTypes[-1] in documentTypes:
                size = opsys.stat(directory + i)[6]

                if checkForTypes[-1] not in docs:
                    docs[checkForTypes[-1]] = [(i, size)]
                else:
                    docs[checkForTypes[-1]].append((i, size))

            elif checkForTypes[-1] in audioTypes:
                size = opsys.stat(directory + i)[6]

                if checkForTypes[-1] not in audios:
                    audios[checkForTypes[-1]] = [(i, size)]
                else:
                    audios[checkForTypes[-1]].append((i, size))

            elif checkForTypes[-1] in picTypes:
                size = opsys.stat(directory + i)[6]

                if checkForTypes[-1] not in pics:
                    pics[checkForTypes[-1]] = [(i, size)]
                else:
                    pics[checkForTypes[-1]].append((i, size))

    videoButton['text'] = 'Videos : ' + str(len(videos))
    docsButton['text'] = 'Documents : ' + str(len(docs))
    audioButton['text'] = 'Audios : ' + str(len(audios))
    picsButton['text'] = 'Pictures : ' + str(len(pics))

    if type != 'All':
        if type in videoTypes:
            showVideos(type)
        elif type in audioTypes:
            showAudios(type)
        elif type in documentTypes:
            showDocs(type)
        elif type in picTypes:
            showPics(type)
    else:
        showVideos(type)


button = Button(topFrame, text="Get Info!", command = getInfo, font = 'times 12 bold')
button.pack(side = LEFT, padx = 10)



#Reset Components Function
def resetComponents():
    global directory, type
    directory =''
    type = 'All'
    entry_box.delete(0,END)
    comboExample.current(0)
    clearTree()
    bList = [audioButton, videoButton, docsButton, picsButton]
    for i in bList:
        text = i['text'].split()
        text[-1] = '0'
        i['text']= ' '.join(text)
        print()
        i['bg'] = 'white'
    audios.clear()
    videos.clear()
    docs.clear()
    pics.clear()
    noData()

# Reset Button for every entry box
resetButton = Button(topFrame, text = 'Reset', font = 'times 12 bold', command = resetComponents)
resetButton.pack(side = LEFT, pady = 15, padx = 5)



#Searching record
val = 0
def searchRecord(event, item=''):
    global val
    searchCount = 0    #to get row number of each element
    offset = [0,0]     #to store the value of first searched item

    if len(treev.selection()) > 0:
        for i in range(len(treev.selection())):
            treev.selection_remove(treev.selection()[0])

    selectedRecords = []              #storing the found items
    itemToFind = searchEntry.get()

    if len(itemToFind)== 0:
        print('its here at 0', itemToFind)
        matchFoundLable['text'] = ''
        treev.yview_moveto(0.0)
        val = 0
        print('nothing is there')
    else:
        children = treev.get_children(item)

        for child in children:
            for subChild in treev.get_children(child):
                searchCount += 1    #increment for each element
                infoTuple = treev.item(subChild, 'values')
                text = infoTuple[1].lower()
                if itemToFind.lower() in text:
                    selectedRecords.append(subChild)
                    print('FOund it ', text, itemToFind.lower())

                    if offset[1] == 0:
                        offset[0] = int(searchCount)
                        offset[1] = 1   #setting the flag for choose only first element of search
            searchCount += 1

    if len(selectedRecords) != 0:
        tupleSelectedRecords = tuple(selectedRecords)
        treev.selection_set(tupleSelectedRecords)
        matchFoundLable['text'] = '[ ' + str(len(tupleSelectedRecords)) + ' ]'
        treev.yview_scroll(offset[0] - val, 'units')   #you cans take abs value for showing selection at the top
        val = offset[0]
    else:
        print('EXECUTED')
        matchFoundLable['text'] = ''
        treev.yview_moveto(0.0)
        val = 0


searchLabel = Label(nestedContedFrame, text = "Search : ", font = "times 20 bold", bg = 'grey', fg= 'white')
searchLabel.pack(side = LEFT, pady = 10)
searchEntry = Entry(nestedContedFrame, width = 30, font = "times 13 bold")
searchEntry.bind('<KeyRelease>', searchRecord)
searchEntry.pack(side = LEFT, padx = 5, pady = 10)

matchFoundLable = Label(nestedContedFrame, text='', font = "times 15 bold", bg = 'grey', fg= 'white')
matchFoundLable.pack(side = LEFT, padx = 5, pady = 10)



########________ CUSTOM DIALOGUE BOX FOR COPY ______ ########
askYesNoWindow = ''

#command for executing copy or not
def copyOrNot(content, moveIntoDir, answer, answerFrame, MoveOrCopy):
    global askYesNoWindow
    # askYesNoWindow.destroy()
    if answer == 'Yes' :
        width = (100/len(content))

        for widget in answerFrame.winfo_children():
            widget.destroy()

        #status message acc to move or copy
        statusMessage = ''
        successStatus = ''
        if MoveOrCopy == 'Copy':
            statusMessage = 'Copy Status : '
            successStatus = 'Copying....'
        elif MoveOrCopy == 'Move':
            statusMessage = 'Move Status : '
            successStatus = 'Moving....'

        progressLable = Label(answerFrame, text = statusMessage, font = 'times 12 bold')
        progressLable.pack(padx = 5, pady = 5, side = LEFT)

        progressBar = ttk.Progressbar(answerFrame, orient=HORIZONTAL, length=100, mode='determinate')
        progressBar.pack(side=LEFT, padx=5, pady=5)

        percentageLable= Label(answerFrame, text = '0%', font = 'times 12 bold')
        percentageLable.pack(padx = 5, pady = 5, side = LEFT)

        fileCompleteLable = Label(answerFrame, text='Processed : ', font='times 12 bold')
        fileCompleteLable.pack( pady=5, side=LEFT)

        fileCountLable = Label(answerFrame, text='0/'+ str(len(content)), font='times 12 bold')
        fileCountLable.pack(pady=5, side=LEFT)

        successMessageLable = Label(answerFrame, text=successStatus, font='times 12 bold', fg = 'Orange')
        successMessageLable.pack(padx=5, pady=5, side=LEFT)

        def probar(width, fileCountLable, successMessageLable, MoveOrCopy):

            cntr = 0
            # curTime = time.clock()
            for i in content:
                print(directory+i[1] + ' will be moved into ' + moveIntoDir)
                print('Filed Copy Start', )
                if MoveOrCopy == 'Copy':
                    copy(directory+i[1], moveIntoDir)
                elif MoveOrCopy == 'Move':
                    move(directory+i[1], moveIntoDir)
                progressBar['value'] += width
                fileCountLable['text'] = str(cntr) + '/' + str(len(content))
                percentageLable['text'] = str(int(progressBar['value'])) + '%'
                if progressBar['value'] >= 100:
                    percentageLable['text'] = '100%'
                    fileCountLable['text'] = str(len(content))+'/'+ str(len(content))
                    successMessageLable['fg'] = 'green'
                    successMessageLable['text'] = 'Successful!'

                root.update_idletasks()
                cntr+=1
            return
        threading.Thread(target=lambda : probar(width, fileCountLable, successMessageLable, MoveOrCopy)).start()

    else:
        askokcancel(title = "Selection Cancelled", message="Please select the files again!")

    root.attributes('-disabled', False)


#making Custom Dialoguebox for view Selection during copy or move files
def askYesNoForCopyFiles(content, moveIntoDir, MoveOrCopy):
    global askYesNoWindow
    askYesNoWindow = Toplevel()

    title = ''  #changing title acc to action move or copy
    if MoveOrCopy == 'Copy':
        title = 'Copy Current Selection?'
    elif MoveOrCopy == 'Move':
        title = 'Move Current Selection?'

    askYesNoWindow.title(title)
    askYesNoWindow.geometry('500x300')
    askYesNoWindow.resizable(0,0)
    root.attributes('-disabled', True)  #Keeping user from using root window's toolbar until new window closes

    #Counting total Size of the selected files
    totalSize = 0
    for i in content:
        print(revSizeConversion(float(i[2]), i[3]))
        totalSize += revSizeConversion(float(i[2]), i[3])

    size,unit = sizeConversion(int(totalSize))
    totalSize = size + ' ' + unit

    #maing bottom frame for buttons ok and cancel to return answers from this window
    answerFrame = Frame(askYesNoWindow, bd= 2, relief = SUNKEN)
    answerFrame.pack(side = BOTTOM, fill = X)

    yesButton = Button(answerFrame, text='OK', font = 'times 12 bold', command = lambda : copyOrNot(content, moveIntoDir,'Yes', answerFrame, MoveOrCopy))
    yesButton.pack(side = LEFT, padx = 50, pady = 5)    #sending answer frame for progressbar to get updated when it is copying

    noButton = Button(answerFrame, text='Cancel',font =  'times 12 bold', command =  lambda : copyOrNot(content, moveIntoDir,'No', '', ''))
    noButton.pack(side = LEFT, pady = 5)


    #making Treeview for view selected content
    contentTreeView = ttk.Treeview(askYesNoWindow, selectmode='extended')
    contentTreeView.pack(side = BOTTOM, expand = True, fill = BOTH, pady = 5)

    #From To Frame
    topFrame = Frame(askYesNoWindow, bd= 2, relief = SUNKEN)
    topFrame.pack(side = TOP, fill = X)

    # From and To label
    fromLabel = Label(topFrame, text='From : ' + directory, font='times 12 bold')
    fromLabel.grid(row = 0, column = 0, sticky = W, ipadx = 50)


    toLabel = Label(topFrame, text='To     : ' + moveIntoDir, font='times 12 bold')
    toLabel.grid(row = 1, column = 0, ipadx = 50)

    #making labels for selected files count and its whole size
    selectedFilesLabel = Label(askYesNoWindow, text = 'Selected Files : ' + str(len(content)), font = 'times 12 bold')
    selectedFilesLabel.pack(side = LEFT, padx = 50)

    fileSizeLabel = Label(askYesNoWindow, text='Total Size : ' + totalSize , font = 'times 12 bold')
    fileSizeLabel.pack(side = LEFT, padx = 50)


    # Constructing vertical scrollbar with treeview
    verscrlbarforctv = Scrollbar(contentTreeView, orient="vertical", command=contentTreeView.yview)
    verscrlbarforctv.pack(side='right', fill=Y)

    # Setting Tree columns and style
    contentTreeView.configure(yscrollcommand=verscrlbarforctv.set)
    contentTreeView["columns"] = ('File Name','Size', 'Unit')

    contentTreeView.column("#0", width=35, anchor='w', stretch=NO)
    contentTreeView.column("File Name", width=350, anchor='w', stretch=NO)
    contentTreeView.column("Size", anchor='e', width=70, stretch=NO)
    contentTreeView.column("Unit", anchor='w', width=50, stretch=NO)

    contentTreeView.heading("#0", text='NO.', anchor='c')
    contentTreeView.heading("File Name", text= 'File Name', anchor = 'c')
    contentTreeView.heading("Size", text='Size', anchor='c')
    contentTreeView.heading("Unit", text='', anchor='c')
    cnt = 1
    for i in content:
        contentTreeView.insert('', 'end', text = str(cnt), values=(i[1],i[2],i[3]))
        cnt += 1


def moveSelectionTO(MoveOrCopy):
    print('Came Here')
    global directory
    moveIntoDir = filedialog.askdirectory()
    print('this is the directory to move into : ', moveIntoDir)
    curItems = treev.selection()
    selectedItems= [treev.item(i)['values'] for i in curItems]

    if len(selectedItems) != 0:

        askYesNoForCopyFiles(selectedItems, moveIntoDir, MoveOrCopy)


def moveSelectionThreadStart(MoveOrCopy):

    moveSelectionThread = threading.Thread(target= lambda : moveSelectionTO(MoveOrCopy))
    moveSelectionThread.start()

copyToButton = Button(nestedContedFrame, text = 'Copy To =>', font = "times 12 bold", command = lambda : moveSelectionThreadStart('Copy'))
copyToButton.pack(side = LEFT, pady = 10, padx = 5)

moveToButton = Button(nestedContedFrame, text = 'Move To =>', font = "times 12 bold", command = lambda : moveSelectionThreadStart('Move'))
moveToButton.pack(side = LEFT, pady = 10, padx = 5)

# gameButton = Button(nestedContedFrame, text = 'Game', font = "times 12 bold", command = threading.Thread(target=sliderGame.startTheGame).start)
# gameButton.pack(side = LEFT, pady = 10, padx = 5)


root.mainloop()
