import tkinter
from tkinter import ttk
import socket
import errno
import sys
import pathlib
import select
from unicodedata import numeric
import accounts_omac
from tkinter.messagebox import showinfo, askyesno, showerror

configSettings = accounts_omac.configFileTkinter()
accountData = accounts_omac.defaultConfigurations.defaultLoadingTkinter(configSettings)
if accountData == False:
  exit()
print(accountData)

allowMultipleAccounts = True
windowTitles = 'omac_LAN'

def on_closing(windowTitles = 'omac_LAN'):
  if askyesno(windowTitles, f"Your program will be terminated\nShould we proceed?", icon ='warning'):
    accounts_omac.saveAccount(accountData, configSettings)
    exit()


hostOrClientWindow = tkinter.Tk()
selected = tkinter.StringVar()

def start():
  global hostOrClient
  hostOrClient = selected.get()
  hostOrClientWindow.destroy()

def changeValue(*args):
  if selected.get() != '':
    startButton.configure(state='normal')
  else:
    startButton.configure(state='disabled')

ttk.Label(hostOrClientWindow,text='Do you want to host a server, or join a server?').grid(column=0, row=0, ipadx=20, ipady=10, sticky="EW", columnspan= 2)
host = ttk.Radiobutton(hostOrClientWindow, text='Host', value='Host', variable=selected)
client = ttk.Radiobutton(hostOrClientWindow, text='Join', value='Client', variable=selected)
startButton = ttk.Button(hostOrClientWindow,text='Continue', state='disabled', command=start)
startButton.grid(column=0, row=2, ipadx=20, ipady=10, sticky="EW", columnspan= 2)
host.grid(column=0, row=1, ipadx=20, ipady=10, sticky="EW")
client.grid(column=1, row=1, ipadx=20, ipady=10, sticky="EW")
selected.trace('w',changeValue)
hostOrClientWindow.protocol("WM_DELETE_WINDOW", on_closing)
hostOrClientWindow.mainloop()

if hostOrClient == 'Host':
  while True:
    if not askyesno(windowTitles, f"The host isn't available in tkinter. \nDo you want us to host in the console? Otherwise we will close the app", icon ='warning'):
      on_closing()
    else:
      break


  '''
  messagesList = ['Hosting....']
  def changeMessage(*args):
      message_var.set(messagesList[0])


  hostWindow = tkinter.Tk()
  ip_var = tkinter.StringVar()
  ip_var.set(f'{ip}:{port}')
  ip_entry = tkinter.Entry(hostWindow, textvariable= ip_var,state='readonly')

  ttk.Label(hostWindow,text='IP adress:').grid(column=0, row=0, ipadx=20, ipady=10, sticky="EW")
  ip_entry.grid(column=1, row=0, ipadx=20, ipady=10, sticky="EW")
  message_var = tkinter.StringVar()
  messages = ttk.Label(hostWindow, textvariable=message_var, state='readonly') #values =messagesList
  messages.grid(column=1, row=1, ipadx=20, ipady=10, sticky="EW")
  ttk.Label(hostWindow,text='Messages:').grid(column=0, row=1, ipadx=20, ipady=10, sticky="EW")
  message_var.trace('w', changeMessage)
  changeMessage()
  '''

  #standard ip and port
  ip = socket.gethostbyname(socket.gethostname())
  port = 1234

  def returnCustomMessage(message):
    sendMessage = {}
    # header
    # data
    encodedMessage = message.encode('utf-8')
    message_header = f"{len(encodedMessage):<{HEADER_LENGTH}}".encode('utf-8')
    sendMessage['data'] = encodedMessage
    sendMessage['header'] = message_header
    return sendMessage

  def wrongClientError(client_socket, error):
    print('Refused new connection from {}:{}, username: {}, not an official or outdated client.'.format(*client_address, user['data'].decode('utf-8')))
    client_socket.send(returnCustomMessage(f'{IP}:{PORT}')['header'] + returnCustomMessage(f'{IP}:{PORT}')['data'] + returnCustomMessage('Connection Refused, not an official or outdated client.')['header'] + returnCustomMessage('Connection Refused, not an official or outdated client.')['data'])
    client_socket.close()
    # print(error)

  def alreadyConnectedError(client_socket):
    print('Refused new connection from {}:{}, username: {}, can\'t connect with the same account twice.'.format(*client_address, user['data'].decode('utf-8')))
    client_socket.send(returnCustomMessage(f'{IP}:{PORT}')['header'] + returnCustomMessage(f'{IP}:{PORT}')['data'] + returnCustomMessage('Connection Refused, can\'t connect with the same account twice.')['header'] + returnCustomMessage('Connection Refused, can\'t connect with the same account twice.')['data'])
    client_socket.close()


  #get the programs path
  ownPath = pathlib.Path().resolve()


  

  # playerlist
  playerList = list()

  HEADER_LENGTH = 10

  IP = ip
  PORT = port
  # Create a socket
  # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
  # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # SO_ - socket option
  # SOL_ - socket option level
  # Sets REUSEADDR (as a socket option) to 1 on socket
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  # Bind, so server informs operating system that it's going to use given IP and port
  # For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
  server_socket.bind((IP, PORT))

  # This makes server listen to new connections
  server_socket.listen()

  # List of sockets for select.select()
  sockets_list = [server_socket]

  # List of connected clients - socket as a key, user header and name as data
  clientsBySocket = {}
  clientByID = {}

  connectionID = 0

  print(f'Listening for connections on {IP}:{PORT}...')

  # Handles message receiving
  def receive_message(client_socket):

    try:

      # Receive our "header" containing message length, it's size is defined and constant
      message_header = client_socket.recv(HEADER_LENGTH)
      # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
      if not len(message_header):
          return False

      # Convert header to int value
      message_length = int(message_header.decode('utf-8').strip())
      # Return an object of message header and message data
      return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

      # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
      # or just lost his connection
      # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
      # and that's also a cause when we receive an empty message
      return False


  while True:

    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # Iterate over notified sockets
    for notified_socket in read_sockets:

      # If notified socket is a server socket - new connection, accept it
      if notified_socket == server_socket:
        # Accept new connection
        # That gives us new socket - client socket, connected to this given client only, it's unique for that client
        # The other returned object is ip/port set
        client_socket, client_address = server_socket.accept()
        # Client should send his name right away, receive it
        user = receive_message(client_socket)
        
        # If False - client disconnected before he sent his name
        if user is False:
            continue

        # extracting the user ID from the username
        userData = user['data'].decode('utf-8')
        if '//' not in userData:
          wrongClientError(client_socket,1)
        elif 'x' not in userData.split('//', 1)[0]:
          wrongClientError(client_socket,2)
        elif not (userData.split('//', 1)[0].split('x',1)[0].isnumeric() and userData.split('//', 1)[0].split('x',1)[1].isnumeric()):
          wrongClientError(client_socket,3)
        elif userData.split('//', 1)[0] in clientByID and clientByID[userData.split('//', 1)[0]]['status'] == 'ACTIVE' and not allowMultipleAccounts:
          alreadyConnectedError(client_socket)
        else:
          
          username = userData.split('//',1)[1].encode('utf-8')
          username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
          user['data'] = username
          user['header'] = username_header

          clientsBySocket[client_socket] = {"username":user, "connectionID": connectionID, "UID": userData.split('//', 1)[0]}
          if not allowMultipleAccounts:
            clientByID[userData.split('//', 1)[0]] = {"connectionID": connectionID, "socket": client_socket, "username": user, "status": 'ACTIVE'}
          else:
            clientByID[connectionID] = {"connectionID": connectionID, "socket": client_socket, "username": user, "status": 'ACTIVE'}

          # username = my_username.encode('utf-8')
          # username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

          connectionID += 1
          
          # save user to the user list
          playerList.append(user['data'].decode('utf-8'))

          # Add accepted socket to select.select() list
          sockets_list.append(client_socket)

          # Also save username and username header
          print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))


      # Else existing socket is sending a message
      else:

          # Receive message
        message = receive_message(notified_socket)

        # If False, client disconnected, cleanup
        if message is False:
            
          print('Closed connection from: {}'.format(clientsBySocket[notified_socket]["username"]['data'].decode('utf-8')))


          # remove user from user list
          try:
              playerList.remove(clientsBySocket[notified_socket]["username"]['data'].decode('utf-8'))
          except:
              e = 0
          # Remove from list for socket.socket()
          sockets_list.remove(notified_socket)

          # Remove from our list of users
          if not allowMultipleAccounts:
            clientByID[clientsBySocket[notified_socket]['UID']]['status'] = "DISCONNECTED"
          else:
            del clientByID[clientsBySocket[notified_socket]['connectionID']]
          del clientsBySocket[notified_socket]

          continue

        # Get user by notified socket, so we will know who sent the message
        user = clientsBySocket[notified_socket]["username"]
        print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
        #define the pingcommand
        pingCommand = False
        #define username
        username = user['data'].decode('utf-8')

        # Iterate over connected clients and broadcast message
        for client_socket in clientsBySocket:

          # But don't sent it to sender unless it is a ping command
          if client_socket != notified_socket or pingCommand == True:

            # Send user and message (both with their headers)
            # We are reusing here message header sent by sender, and saved username header send by user when he connected
            # client_socket.send(returnCustomMessage(f'{IP}:{PORT}')['header'] + returnCustomMessage(f'{IP}:{PORT}')['data'] + returnCustomMessage('boo')['header'] + returnCustomMessage('boo')['data'])
            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                
                
                
                
    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

      # Remove from list for socket.socket()
      sockets_list.remove(notified_socket)

      # Remove from our list of users
      del clientsBySocket[notified_socket]

if hostOrClient == 'Client':
  #get the programs path
  ownPath = pathlib.Path().resolve()
  #create log folder if it doesn't exist
  def connect():
    global my_username
    clientConnectWindow.destroy()
    my_username = Ip_name_var.get()


  def reUse():
    Ip_name_var.set('')
    label.configure(text='Username: ')
    startButton.configure(command=connect)

  def nextStep():
    global ip, port
    ipadressAndPort = Ip_name_var.get().split(":")
    if "." in ipadressAndPort[0]:
      ip = ipadressAndPort[0]
      if len(ipadressAndPort) == 2:
        port = int(ipadressAndPort[1])
        reUse()
      else:
        if askyesno(windowTitles, f"No port found, You can fix it by putting it like this: IP:Port\nWe could also just put the default port for you but that might not work.\nShould we use the default port?", icon ='warning'):
          port = 1234
          reUse()

            
    else:
      showerror(windowTitles,'IP not valid')
  def notConnectedAnymore(message):
    try:
      clientWindow.destroy()
    except:
      pass
    showerror(windowTitles,f'{message}')
    exit()

  def connectWindow():
    global Ip_name_var, clientConnectWindow, label,startButton
    clientConnectWindow = tkinter.Tk()
    Ip_name_var = tkinter.StringVar()
    label = tkinter.Label(clientConnectWindow, text='Input the IP:PORT')
    label.grid(column=0, row=0, ipadx=20, ipady=10, sticky="EW")
    Ip_entry = tkinter.Entry(clientConnectWindow, textvariable=Ip_name_var)
    Ip_entry.grid(column=0, row=1, ipadx=20, ipady=10, sticky="EW")
    startButton = ttk.Button(clientConnectWindow,text='Continue', command=nextStep)
    startButton.grid(column=0, row=2, ipadx=20, ipady=10, sticky="EW")
    clientConnectWindow.protocol("WM_DELETE_WINDOW", on_closing)
    clientConnectWindow.mainloop()
  connectWindow()
  







  
  HEADER_LENGTH = 10
  IP = ip
  PORT = port


  def doACommand(command,message,username,my_username):
    pass
      
  # do a command you just sent
  def doACommandYourself(command,message,my_username):
    pass


  # Create a socket
  # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
  # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect to a given ip and port
  redo = False
  try:
    client_socket.connect((IP, PORT))
  except Exception as e:
    showerror(windowTitles,f'Server did not respond back.\nWe will reopen the IP input screen.\nFull error:\n{e}')
    exit()



  # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
  client_socket.setblocking(False)

  my_usernameBackup = my_username 
  my_username = f'{accountData["UserID"]}//{my_username}'

  # Prepare username and header and send them
  # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
  username = my_username.encode('utf-8')
  username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
  client_socket.send(username_header + username)

  my_username = my_usernameBackup

  def sendMessage():
    if message_var.get():
      message = message_var.get()
      message_var.set('')

      messagesList.insert(0,f'{my_username} > {message}')
      print(f'{my_username} > {message}')
      changeMessage()

      # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
      message = message.encode('utf-8')
      message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
      client_socket.send(message_header + message)

  def receive():
    try:
      # Now we want to loop over received messages (there might be more than one) and print them
      while True:
        # Receive our "header" containing username length, it's size is defined and constant
        username_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(username_header):
          message ='Connection closed by the server'
          notConnectedAnymore(message)

        # Convert header to int value
        username_length = int(username_header.decode('utf-8').strip())

        # Receive and decode username
        username = client_socket.recv(username_length).decode('utf-8')

        # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8').strip())
        message = client_socket.recv(message_length).decode('utf-8')

        # Print message
        messagesList.insert(0,f'{username} > {message}')
        changeMessage()
        print(f'{username} > {message}')

    except IOError as e:
      # This is normal on non blocking connections - when there are no incoming data error is going to be raised
      # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
      # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
      # If we got different error code - something happened
      if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:

          message = 'Reading error: {}'.format(str(e))
          notConnectedAnymore(message)


      # We just did not receive anything
      return

    except Exception as e:
      # Any other exception - something happened, exit
      message = 'Reading error: '.format(str(e))
      notConnectedAnymore(message)






  messagesList = ['Connected']
  def changeMessage(*args):
    messages_var.set(messagesList[0])
    messages.configure(values=messagesList)

  clientWindow = tkinter.Tk()
  message_var = tkinter.StringVar()
  label = tkinter.Label(clientWindow, text='Message:')
  label.grid(column=0, row=0, ipadx=20, ipady=10, sticky="EW")
  Ip_entry = tkinter.Entry(clientWindow, textvariable=message_var)
  Ip_entry.grid(column=1, row=0, ipadx=20, ipady=10, sticky="EW")
  startButton = ttk.Button(clientWindow,text='Send message', command=sendMessage)
  startButton.grid(column=0, row=1, ipadx=20, ipady=10, sticky="EW", columnspan=2)
  messages_var = tkinter.StringVar()
  messages = ttk.Combobox(clientWindow, textvariable=messages_var,values=messagesList, state='readonly') #values =messagesList
  messages.grid(column=0, row=2, ipadx=20, ipady=10, sticky="EW", columnspan=2)
  clientWindow.protocol("WM_DELETE_WINDOW", on_closing)
  message_var.trace('w', changeMessage)
  changeMessage()
  
  def tick():
    receive()
    clientWindow.after(10, tick)


  clientWindow.after(10, tick)
  clientWindow.mainloop()

accountData = accounts_omac.saveAccount(accountData, configSettings)







 


        
