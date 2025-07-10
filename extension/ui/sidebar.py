"""
Sidebar UI construction using UNO API.
"""


# Real Sidebar UI implementation using UNO API
import uno
from com.sun.star.awt import XActionListener
from com.sun.star.awt.PosSize import POS, SIZE

class SidebarActionListener(unohelper.Base, XActionListener):
    def __init__(self, callback):
        self.callback = callback
    def actionPerformed(self, action_event):
        self.callback(action_event)

def create_sidebar():
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    doc = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx).getCurrentComponent()
    parent_win = doc.CurrentController.Frame.ContainerWindow
    toolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)

    # Main dialog window (sidebar panel)
    width, height = 350, 600
    sidebar = toolkit.createWindow({
        'Type': uno.getConstantByName('com.sun.star.awt.WindowClass.TOP'),
        'Parent': parent_win,
        'Bounds': (0, 0, width, height),
        'WindowAttributes': 0x10 | 0x20  # SIZEABLE | MOVEABLE
    })
    sidebar.setVisible(True)

    # Conversation area (scrollable)
    conversation_area = toolkit.createTextArea()
    conversation_area.setPosSize(10, 10, width-20, 350, POS | SIZE)
    conversation_area.setReadOnly(True)
    sidebar.addChild(conversation_area)

    # User input box
    input_box = toolkit.createTextField()
    input_box.setPosSize(10, 370, width-90, 30, POS | SIZE)
    input_box.setText("")
    sidebar.addChild(input_box)

    # Send button
    send_button = toolkit.createButton()
    send_button.setPosSize(width-70, 370, 60, 30, POS | SIZE)
    send_button.setLabel("Send")
    sidebar.addChild(send_button)


    # Status label
    status_label = toolkit.createLabel()
    status_label.setPosSize(10, 410, width-120, 20, POS | SIZE)
    status_label.setText("")
    sidebar.addChild(status_label)

    # Spinner/progress bar for AI response
    progress_bar = toolkit.createProgressBar()
    progress_bar.setPosSize(width-100, 410, 90, 20, POS | SIZE)
    progress_bar.setRange(0, 100)
    progress_bar.setValue(0)
    progress_bar.setVisible(False)
    sidebar.addChild(progress_bar)

    # Clear conversation button
    clear_button = toolkit.createButton()
    clear_button.setPosSize(10, 440, width-20, 30, POS | SIZE)
    clear_button.setLabel("Clear Conversation")
    sidebar.addChild(clear_button)

    # Message history in memory
    message_history = []


def update_conversation():
    conversation_area.setText("")
    for idx, msg in enumerate(message_history):
        if msg['role'] == 'user':
            # User message: right-aligned, light background
            conversation_area.append("[User] ")
            conversation_area.append(msg['content'] + "\n")
        else:
            # AI message: left-aligned, shaded background
            conversation_area.append("[AI]   ")
            conversation_area.append(msg['content'] + "\n")
            # Add actionable buttons (Copy, Retry)
            # (In real UNO, would add buttons to the UI; here, show as text for demo)
            conversation_area.append("   [Copy] [Retry/Regenerate]\n")
    conversation_area.setCaretPosition(len(conversation_area.getText()))



    def send_message(_):
        user_text = input_box.getText().strip()
        if not user_text:
            return
        message_history.append({'role': 'user', 'content': user_text})
        update_conversation()
        input_box.setText("")
        status_label.setText("Thinking...")
        progress_bar.setVisible(True)
        progress_bar.setValue(10)
        # Simulate progress for long AI response
        import threading, time
        def ai_task():
            for v in range(10, 90, 10):
                progress_bar.setValue(v)
                time.sleep(0.1)
            from extension.orchestrator import Orchestrator
            orchestrator = Orchestrator()
            result = orchestrator.handle_user_request(user_text)
            ai_response = result.get('summary', 'AI did not respond.')
            message_history.append({'role': 'ai', 'content': ai_response, 'user_prompt': user_text})
            update_conversation()
            status_label.setText("")
            progress_bar.setValue(100)
            time.sleep(0.2)
            progress_bar.setVisible(False)
        threading.Thread(target=ai_task).start()

    def handle_action(action, idx):
        if action == 'copy':
            # Copy AI message to clipboard
            ai_msg = message_history[idx]['content']
            toolkit.getSystemClipboard().setContents(ai_msg, None)
            status_label.setText("Copied to clipboard.")
        elif action == 'retry':
            # Retry last user prompt
            user_prompt = message_history[idx].get('user_prompt', '')
            if user_prompt:
                input_box.setText(user_prompt)
                send_message(None)
                status_label.setText("Regenerated response.")

    def clear_conversation(_):
        message_history.clear()
        update_conversation()
        status_label.setText("Conversation cleared.")


    send_button.addActionListener(SidebarActionListener(send_message))
    clear_button.addActionListener(SidebarActionListener(clear_conversation))

    # Accessibility: tooltips
    send_button.setToolTipText("Send your message (Enter)")
    clear_button.setToolTipText("Clear the conversation history")
    input_box.setToolTipText("Type your prompt here")
    conversation_area.setToolTipText("Conversation history")

    # Keyboard shortcut: Enter to send
    # (UNO API for key events can be added here if needed)
