# Plan: Understand Zotero Connector PDF Attachment Mechanism

## Goal
Understand exactly how the Zotero Connector browser extension attaches PDFs to items, then replicate it in Python.

## Research Tasks

### 1. Find session creation/registration
- **Search:** `grep -rn "sessionID" /tmp/zotero-connectors/src/common/*.js`
- **Find:** Where is `sessionID` first created/generated?
- **Verify:** Find the line that does `sessionID = Zotero.Utilities.randomString()` or similar
- **Output:** File path and line number where sessionID is created

### 2. Find how session is registered with Zotero desktop
- **Search:** Look for any API call that happens BEFORE saveAttachment
- **Find:** Is there a `createSession`, `registerSession`, or similar endpoint call?
- **Verify:** Check what HTTP request is made to localhost:23119 before attachments are saved
- **Output:** The endpoint URL and request format for session registration

### 3. Find the complete saveItems → saveAttachment flow
- **Search:** `grep -rn "saveItems\|saveAttachment" /tmp/zotero-connectors/src/common/itemSaver*.js`
- **Find:** The exact sequence: saveItems called → ??? → saveAttachment called
- **Verify:** What happens between saveItems and saveAttachment? Is sessionID passed?
- **Output:** Complete flow diagram with all function calls

### 4. Find how Zotero desktop validates sessionID
- **Search:** This is in Zotero DESKTOP code, not connector
- **Find:** Need to clone zotero/zotero repo and search for sessionID validation
- **Verify:** What endpoint validates sessionID and how?
- **Output:** The desktop-side session validation mechanism

### 5. Alternative: Find if there's a simpler attachment method
- **Search:** `grep -rn "attachment" /tmp/zotero-connectors/src/common/itemSaver*.js | grep -v "saveAttachment"`
- **Find:** Are there other attachment methods that don't require sessions?
- **Verify:** Check if saveItems can include attachments that Zotero downloads automatically
- **Output:** List of all attachment-related endpoints and their requirements

## Done When
- [ ] Can answer: "How does the connector register a session with Zotero desktop?"
- [ ] Can answer: "What is the minimum required to attach a PDF to an existing item?"
- [ ] Have EITHER:
  - Session registration mechanism documented, OR
  - Alternative attachment method that doesn't require sessions

## Notes
- The connector source is at `/tmp/zotero-connectors/`
- Zotero desktop source may need to be cloned from github.com/zotero/zotero
- Focus on finding EXACT code paths, not guessing
