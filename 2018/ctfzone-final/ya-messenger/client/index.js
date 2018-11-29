#!/usr/bin/env node --no-warnings

const blessed = require('blessed')
const grpc = require('grpc')
const messages = require('./grpc_pb')
const service = require('./grpc_grpc_pb')

// ==========
// = Screen =
// ==========

const screen = blessed.screen({
  title: 'Messenger',
  smartCSR: true,
  autoPadding: true,
  dockBorders: true,
  keys: true,
})

screen.key(['C-c', 'q'], () => {
  process.exit(0)
})

// =========
// = Start =
// =========

// TODO: arvg
if (process.argv.length !== 3) {
  console.log('Usage: PROGRAM <node-addr>')
  process.exit(1)
}

const serverAddr = process.argv[2]

const connectingMessage = blessed.text({
  parent: screen,
  tags: true,
  top: 'center',
  left: 'center',
  content: `{blue-fg}{bold}Connecting to ${serverAddr}{/}`,
  border: {
    type: 'line',
    fg: 'blue'
  },
  padding: 1,
})

screen.render()

// GRPC connect

const client = new service.NodeClient(
  serverAddr,
  grpc.credentials.createInsecure())

let deadline = new Date();
deadline.setSeconds(deadline.getSeconds() + 3);

grpc.waitForClientReady(client, deadline, (err) => {

  connectingMessage.hide()

  if (err) {
    blessed.text({
      parent: screen,
      content: `{red-fg}{bold}Fail to connect to the server ${serverAddr}{/}`,
      left: 'center',
      top: 'center',
      tags: true,
      border: {
        type: 'line',
        fg: 'red',
      },
      padding: 1,
    })
  } else {
    loginFormItems.loginField.focus()
    loginForm.show()
  }

  screen.render()
})

let authToken = null
let currentUser = ''
let meta = new grpc.Metadata()

// =================
// = Error message =
// =================

errorMsg = blessed.message({
  parent: screen,
  left: 'center',
  top: 1,
  width: 40,
  height: 3,
  style: {
    bold: true,
    fg: 'red',
  },
  hidden: true,
})

successMsg = blessed.message({
  parent: screen,
  left: 'center',
  top: 1,
  width: 40,
  height: 3,
  style: {
    bold: true,
    fg: 'green',
  },
  hidden: true,
})

infoMsg = blessed.message({
  parent: screen,
  left: 'center',
  top: 1,
  width: 40,
  height: 3,
  style: {
    bold: true,
    fg: 'blue',
  },
  hidden: true,
})

// ==============
// = Login form =
// ==============

const loginForm = blessed.form({
  parent: screen,
  width: 60,
  height: 14,
  left: 'center',
  top: 'center',
  hidden: true,
  tags: true,
  keys: true,
  border: {
    type: 'line',
  },
  label: '{blue-fg}{bold}Login{/}',
})

let loginFormItems = {}

loginFormItems.loginField = blessed.textbox({
  parent: loginForm,
  tags: true,
  keys: true,
  input: true,
  label: 'login',
  name: 'login',
  top: 1,
  left: 15,
  width: 30,
  height: 3,
  border: {
    type: 'line',
  },
  style: {
    focus: {
      border: {
        fg: 'red'
      }
    }
  }
})

loginFormItems.passwordField = blessed.textbox({
  parent: loginForm,
  tags: true,
  keys: true,
  input: true,
  label: 'password',
  name: 'password',
  top: 5,
  left: 15,
  width: 30,
  height: 3,
  content: 'first',
  border: {
    type: 'line',
  },
  style: {
    focus: {
      border: {
        fg: 'red'
      }
    }
  }
})

loginFormItems.submitButton = blessed.button({
  parent: loginForm,
  keys: true,
  shrink: true,
  padding: {
    left: 1,
    right: 1,
  },
  left: 16,
  bottom: 1,
  name: 'submit',
  content: 'submit',
  style: {
    bg: 'green',
    bold: true,
    focus: {
      bg: 'red'
    },
    hover: {
      bg: 'red'
    }
  }
})

loginFormItems.goToRegisterButton = blessed.button({
  parent: loginForm,
  keys: true,
  shrink: true,
  padding: {
    left: 1,
    right: 1,
  },
  right: 16,
  bottom: 1,
  name: 'register',
  content: 'register',
  style: {
    bg: 'blue',
    bold: true,
    focus: {
      bg: 'red'
    },
    hover: {
      bg: 'red'
    }
  }
})

loginFormItems.submitButton.on('press', () => {
  loginForm.submit()
})

loginFormItems.goToRegisterButton.on('press', () => {
  loginForm.hide()
  registerForm.show()
  registerFormItems.loginField.focus()
  screen.render()
})

loginForm.on('submit', (data) => {

  const req = new messages.RequestNodeLogin()

  req.setName(data.login)
  req.setPassword(data.password)

  client.login(req, (err, res) => {
    if (err) {
      errorMsg.display(`{center}${err.details}{/}`)
      return
    }

    // Add auth token to metadata
    currentUser = data.login
    authToken = res.getToken()
    meta.add('auth', authToken)

    loginForm.hide()
    main.show()
    chats.select(0)
    chats.focus()
    screen.render()
  })

})

// =================
// = Register form =
// =================

const registerForm = blessed.form({
  parent: screen,
  width: 60,
  height: 14,
  left: 'center',
  top: 'center',
  keys: true,
  vi: true,
  tags: true,
  hidden: true,
  border: {
    type: 'line',
  },
  label: '{blue-fg}{bold}Register{/}',
})

let registerFormItems = {}

registerFormItems.loginField = blessed.textbox({
  parent: registerForm,
  tags: true,
  label: 'login',
  name: 'login',
  top: 1,
  left: 15,
  width: 30,
  height: 3,
  keys: true,
  input: true,
  content: 'first',
  border: {
    type: 'line',
  },
  style: {
    focus: {
      border: {
        fg: 'red'
      }
    }
  }
})

registerFormItems.passwordField = blessed.textbox({
  parent: registerForm,
  tags: true,
  label: 'password',
  name: 'password',
  top: 5,
  left: 15,
  width: 30,
  height: 3,
  input: true,
  keys: true,
  content: 'first',
  border: {
    type: 'line',
  },
  style: {
    focus: {
      border: {
        fg: 'red'
      }
    }
  }
})

registerFormItems.submitButton = blessed.button({
  parent: registerForm,
  keys: true,
  shrink: true,
  padding: {
    left: 1,
    right: 1,
  },
  left: 16,
  bottom: 1,
  name: 'submit',
  content: 'submit',
  style: {
    bg: 'green',
    bold: true,
    focus: {
      bg: 'red'
    },
    hover: {
      bg: 'red'
    }
  }
})

registerFormItems.goToLoginButton = blessed.button({
  parent: registerForm,
  keys: true,
  shrink: true,
  padding: {
    left: 1,
    right: 1,
  },
  right: 16,
  bottom: 1,
  name: 'login',
  content: 'login',
  style: {
    bg: 'blue',
    bold: true,
    focus: {
      bg: 'red'
    },
    hover: {
      bg: 'red'
    }
  }
})

registerFormItems.submitButton.on('press', () => {
  registerForm.submit()
})

registerFormItems.goToLoginButton.on('press', () => {
  registerForm.hide()
  loginForm.show()
  loginFormItems.loginField.focus()
  screen.render()
})

registerForm.on('submit', (data) => {
  req = new messages.RequestNodeRegister()
  req.setName(data.login)
  req.setPassword(data.password)

  client.register(req, (err, res) => {
    if (err) {
      errorMsg.display(`{center}${err.details}{/}`)
      return
    }

    // Show success message
    successMsg.display(`{center}User was successfully registered{/}`)

    // Switch to login
    registerForm.hide()
    loginForm.show()
    loginFormItems.loginField.focus()
    screen.render()
  })
})

// ===============
// = Main window =
// ===============

const main = blessed.form({
  parent: screen,
  hidden: true,
  keys: true,
  tags: true,
  width: '90%',
  height: '90%',
  top: 'center',
  left: 'center',
  border: {
    type: 'line',
  },
})

const chatsTitle = blessed.box({
  parent: main,
  width: '30%',
  height: 3,
  top: 1,
  left: 0,
  tags: true,
  content: '{center}{bold}Chats{/}',
})

const chatsDelimer = blessed.line({
  parent: main,
  orientation: 'horizontal',
  top: 3,
})

const chats = blessed.list({
  parent: main,
  keys: true,
  vi: true,
  width: '30%+3',
  height: '100%-4',
  top: 3,
  left: -1,
  style: {
    selected: {
      fg: 'white',
      bg: 'blue',
      bold: true,
    },
    focus: {
      selected: {
        bg: 'red',
      },
    },
  },
  border: {
    type: 'line',
  }
})

chats.on('select', () => {
  const userName = chats.value
  chatTitle.setContent(`{center}{bold}${userName}{/}`)
  updateMessages()
  screen.render()
})

// ============
// = Add chat =
// ============

const addChat = blessed.button({
  parent: main,
  keys: true,
  shrink: true,
  bottom: 0,
  left: 1,
  content: 'add',
  padding: {
    left: 1,
    right: 1,
  },
  style: {
    bg: 'blue',
    bold: true,
    focus: {
      bg: 'red'
    },
    hover: {
      bg: 'red'
    }
  }
})

const addChatForm = blessed.form({
  parent: screen,
  width: 60,
  height: 10,
  left: 'center',
  top: 'center',
  keys: true,
  tags: true,
  hidden: true,
  border: {
    type: 'line',
  },
  label: '{blue-fg}{bold}Add chat{/}',
})

let addChatFormItems = {}

addChatFormItems.userNameField = blessed.textbox({
  parent: addChatForm,
  tags: true,
  keys: true,
  shrink: true,
  label: 'name',
  name: 'name',
  top: 1,
  left: 15,
  width: 30,
  height: 3,
  input: true,
  keys: true,
  content: 'first',
  border: {
    type: 'line',
  },
  style: {
    focus: {
      border: {
        fg: 'red'
      }
    }
  }
})

addChatFormItems.submitButton = blessed.button({
  parent: addChatForm,
  keys: true,
  shrink: true,
  padding: {
    left: 1,
    right: 1,
  },
  left: 16,
  bottom: 1,
  name: 'submit',
  content: 'add',
  style: {
    bg: 'green',
    bold: true,
    focus: {
      bg: 'red'
    },
    hover: {
      bg: 'red'
    }
  }
})

addChatFormItems.cancelButton = blessed.button({
  parent: addChatForm,
  keys: true,
  shrink: true,
  padding: {
    left: 1,
    right: 1,
  },
  left: 24,
  bottom: 1,
  name: 'cancel',
  content: 'cancel',
  style: {
    bg: 'green',
    bold: true,
    focus: {
      bg: 'red'
    },
    hover: {
      bg: 'red'
    }
  }
})

addChat.on('press', () => {
  addChatForm.show()
  addChatFormItems.userNameField.focus()

  screen.render()
})

addChatFormItems.submitButton.on('press', () => {
  addChatForm.submit()
})

addChatFormItems.cancelButton.on('press', () => {
  addChatForm.hide()
  main.focus()
})

addChatForm.on('submit', (values) => {

  const req = new messages.RequestNodeAddContact()
  req.setUserName(values.name)

  client.addContact(req, meta, (err, res) => {
    if (err) {
      errorMsg.display(`{center}${err.details}{/}`)
      return
    }

    successMsg.display(`{center}Contact "${values.name}" added{/}`)
    addChatForm.hide()
    updateUserChatsList()
    chats.focus()
    screen.render()
  })
})

// ========
// = Chat =
// ========

const delimer = blessed.line({
  parent: main,
  orientation: 'vertical',
  left: '30%+1',
})

const chatTitle = blessed.box({
  parent: main,
  width: '70%-3',
  height: 3,
  top: 1,
  left: '30%+2',
  tags: true,
})

const chatDelimer = blessed.line({
  parent: main,
  orientation: 'horizontal',
  top: 3,
})

const chat = blessed.list({
  parent: main,
  keys: true,
  vi: true,
  width: '70%-1',
  height: '100%-6',
  top: 3,
  left: '30%+1',
  tags: true,
  scrollable: true,
  invertSelected: true,
  scrollbar: {
    style: {
      bg: 'blue',
    },
  },
  border: {
    type: 'line',
  },
  style: {
    focus: {
      border: {
        fg: 'red',
      }
    },
  }
})

// ================
// = Send message =
// ================

const messageField = blessed.textbox({
  parent: main,
  tags: true,
  keys: true,
  input: true,
  scrollable: true,
  name: 'message',
  height: 3,
  left: '30%+1',
  bottom: -1,
  width: '70%-1',
  content: 'first',
  border: {
    type: 'line',
  },
  style: {
    focus: {
      border: {
        fg: 'red'
      }
    }
  }
})

const sendMessage = blessed.button({
  parent: main,
  keys: true,
  shrink: true,
  padding: {
    left: 1,
    right: 1,
  },
  right: 1,
  bottom: 0,
  name: 'submit',
  content: 'send',
  style: {
    bg: 'blue',
    bold: true,
    focus: {
      bg: 'red'
    },
    hover: {
      bg: 'red'
    }
  }
})

sendMessage.on('press', () => {
  const message = messageField.value

  if (message.length === 0) {
    errorMsg.display('Empty message')
    return
  }

  const userName = chats.value

  if (!userName) {
    errorMsg.display('User is not selected')
    return
  }

  const req = new messages.RequestNodeSendMessage()
  req.setUserToName(userName)
  req.setData(message)

  client.sendMessage(req, meta, (err, res) => {
    if (err) {
      errorMsg.display(`{center}${err.details}{/}`)
      return
    }

    messageField.clearValue()

    updateMessages()
  })
})

// ========
// = Help =
// ========

const helpBox = blessed.box({
  parent: screen,
  width: '100%',
  height: 1,
  bottom: 0,
  left: 0,
  style: {
    bg: 'blue',
  }
})

const helpLine = blessed.box({
  parent: helpBox,
  left: 0,
  shrink: true,
  fg: 'white',
  bold: true,
  bg: 'blue',
  content: 'tab: next | shift + tab: prev | enter: select | q: quit',
})

// ========
// = Main =
// ========

main.on('show', () => {

  // Load user contacts
  updateUserChatsList(() => {
    chats.select(0)
    const userName = chats.value
    chatTitle.setContent(`{center}{bold}${userName}{/}`)
    updateMessages()
  })

  processEvents()

  screen.render()
})

// ===========
// = Helpers =
// ===========

const processEvents = () => {
  call = client.getUpdates(new messages.Empty(), meta)
  call.on('data', (res) => {
    switch (res.getPayloadCase()) {
      case messages.Event.PayloadCase.EVENT_MESSAGE:
        const message = res.getEventMessage().getMessage()
        const userFrom = message.getUserFrom().getName()
        if (!chats.items.includes(userFrom) && userFrom !== currentUser) {
          updateUserChatsList()
          infoMsg.display(`{center}New message from "${userFrom}"{/}`)
        }
        if (message.getUserFrom().getName() !== chats.value) {
          return
        }
        chat.add(formatMessage(message))
        chat.setScrollPerc(100)
        chat.select(chat.items.length - 1)
        screen.render()
        break;
      case messages.Event.PayloadCase.EVENT_MESSAGE_STATUS:
        const messageId = res.getEventMessageStatus().getMessageId()
        for (let i = chat.items.length - 1; i >= 0; i--) {
          let item = chat.getItem(i)
          if (item.content.indexOf(`§${messageId}§`)) {
            chat.setItem(item, item.content.replace('⧖', '{green-fg}✓{/}'))
            screen.render()
            break;
          }
        }
        break;
    }
  })
  call.on('error', (err) => {
    process.exit(1)
  })
}

const updateUserChatsList = (cb) => {
  client.getContacts(new messages.Empty(), meta, (err, res) => {
    if (err) {
      errorMsg.display(`{center}${err.details}{/}`)
      return
    }

    // Update chats list
    const items = res.getUserNamesList()
    chats.setItems(items)
    if (cb) {
      cb()
    }
    screen.render()
  })
}

const formatMessage = (message) => {
  const userFrom = message.getUserFrom()
  const userTo = message.getUserTo()

  let line = ''

  const isCurrent = userFrom.getName() === currentUser

  line += isCurrent
    ? '{red-fg}'
    : '{blue-fg}'

  line += `{bold}[${userFrom.getName()}]{/} `
  line += `{bold}{grey-fg}[${message.getCreatedAt()}]{/} `

  if (isCurrent) {
    line += '['
    switch (message.getStatus()) {
      case messages.MessageStatus.PENDING:
        line += '?'
        break;
      case messages.MessageStatus.DELIVERED:
        line += '{green-fg}o{/}'
        break;
      case messages.MessageStatus.ERROR:
        line += '{red-fg}x{/}'
        break;
      default:
        break;
    }
    line += '] '
  } else {
    line += '   '
  }

  line += new TextDecoder('utf-8').decode(message.getData())

  line += ' '.repeat(100) + `{/}{black-fg}§${message.getId()}§{/}`

  return line
}

const updateMessages = () => {
  const userName = chats.value

  if (!userName) {
    return
  }

  const req = new messages.RequestNodeGetMessages()
  req.setUserName(userName)

  client.getMessages(req, meta, (err, res) => {
    if (err) {
      errorMsg.display(`{center}${err.details}{/}`)
      return
    }

    const messages = res.getMessagesList()

    let items = []
    messages.forEach((message) => {
      items.push(formatMessage(message))
    })

    chat.setItems(items)
    chat.setScrollPerc(100)
    chat.select(chat.items.length - 1)
    screen.render()
  })
}
