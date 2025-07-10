# Conversation UI Design for LibreOffice AI Extension

## Purpose
This document details the design for a simple, user-friendly, and programmatically constructed conversation UI for the LibreOffice Writer AI extension. The UI is implemented as a sidebar panel and enables seamless interaction between the user and the AI assistant, supporting clear conversation flow, actionable responses, and robust feedback.

---

## 1. UI Components Overview

### 1.1 Conversation Display Area
- **Type:** Read-only, multiline text area (message list)
- **Features:**
  - Displays the ongoing conversation between the user and the AI.
  - Distinct visual styling for user and AI messages:
    - Different background colors (e.g., light for user, shaded for AI)
    - Alignment (e.g., right for user, left for AI)
    - Optional icons (user/avatar for user, robot for AI)
  - Scrollable when conversation is long.
  - Supports clickable links or buttons in AI responses for actions such as:
    - "Copy" (copies the AI response to clipboard)
    - "Retry / Regenerate" (resends the last user prompt)

### 1.2 User Input Box
- **Type:** Single-line or expandable multiline text box
- **Features:**
  - Where the user types their prompt or instruction.
  - Placeholder text (e.g., "Ask the AI to edit your document...").
  - Supports pressing Enter to send (Shift+Enter for newline if multiline).

### 1.3 Send Button
- **Type:** Button
- **Features:**
  - Submits the user’s input to the AI.
  - Clearly labeled (e.g., “Send” or with a paper plane icon).
  - Disabled when input is empty.

### 1.4 Status / Progress Indicator
- **Type:** Label, spinner, or progress bar
- **Features:**
  - Shows when the AI is processing a request (e.g., "Thinking...", spinner).
  - Displays error messages if something goes wrong.

### 1.5 Clear / New Conversation Button
- **Type:** Button
- **Features:**
  - Clears the conversation history from the UI and resets the state.
  - Confirmation dialog to prevent accidental clearing.

---

## 2. Layout (Sidebar Panel)

```
+-----------------------------------------------+
| Conversation Display Area (scrollable)        |
|  [User]  How do I make this bold?             |
|  [AI]    Select the text and click 'Bold'.    |
|  [AI]    [Copy] [Retry/Regenerate]            |
|  ...                                         |
+-----------------------------------------------+
| [ ] Ask the AI to edit your document...       |
| [Send]                                       |
+-----------------------------------------------+
| [Thinking...]                                |
| [Clear Conversation]                         |
+-----------------------------------------------+
```

---

## 3. Programmatic Construction (UNO API)

### 3.1 Controls and Containers
- Use LibreOffice UNO API to create the sidebar panel and add controls programmatically.
- **Main container:** Vertical box layout (VBox) to stack components.
- **Conversation area:**
  - Scrollable container (ScrollPane or similar UNO control).
  - For each message, add a horizontal box (HBox) containing:
    - Icon (optional)
    - Styled label or text area for message content
    - For AI messages, add action buttons ("Copy", "Retry/Regenerate") as needed
- **User input area:**
  - Multiline text box (TextField or TextArea control)
  - Send button
- **Status area:**
  - Label or spinner control
- **Clear conversation:**
  - Button at the bottom

### 3.2 Styling and Interaction
- Apply background colors and alignment to distinguish user and AI messages.
- Attach event listeners to:
  - Send button (send message)
  - Enter key in input box (send message)
  - Action buttons in AI messages (copy to clipboard, retry prompt)
  - Clear conversation button (clear message list with confirmation)
- Ensure conversation area scrolls to the latest message on update.
- Disable send button when input is empty or AI is processing.
- Show/hide status indicator as appropriate.

### 3.3 Actionable AI Responses
- Parse AI responses for actionable content (e.g., suggested actions, links).
- Dynamically add "Copy" and "Retry/Regenerate" buttons to AI messages.
- Implement clipboard copy functionality via UNO API.
- On "Retry/Regenerate", resend the last user prompt and update the conversation area.

---

## 4. Accessibility and Usability
- Ensure all controls are keyboard accessible.
- Use clear labels and tooltips for all buttons.
- Provide visual feedback for active/inactive states (e.g., disabled send button).
- Ensure the UI is responsive to resizing of the sidebar.

---

## 5. Implementation Guidance
- Structure code for easy addition of new message types or actions in the future.
- Maintain a message history data structure in memory to drive the conversation display.
- Separate UI logic from AI interaction logic for maintainability.
- Handle errors gracefully and provide clear feedback to the user.

---

This design provides a clean, intuitive, and robust conversation interface for the LibreOffice AI extension, supporting actionable AI responses and efficient user interaction, all constructed programmatically using the UNO API.