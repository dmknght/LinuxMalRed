# Post exploitation and Lateral movement

- what's post exploitation and (or) lateral movement
- What's the ideas, purpose, mindsets or tactics

# Gold-mining on Linux system (mindset, tactic, common resources to gather)
- Credential hunting: files, history, commandline, 
- Possible privilege escalation: misconfig, weak default permissions, suid binary, ...
- Persistence tactics
- Discovery other machines (TODO pivoting?)

# Example
- Credential gathering:
 + Find interesting files like git setting that contains credential, ssh key, password, backup
 + Example of checking bash history and find password in it
 + Check all commandlines from running processes. Find possible password
 + List all login users on current system
 + TODO brute force password, generate password from charset with itertool
- Priv Esc:
 + Find weak default permissions: find writable folder or file that's not belong to current user
 + find suid program
- Persistence: Write a program to add persistence entry to bashrc
- Discovery: simple network scanning

# Remote module execution
- C&C frameworks are execute modules remotely (from server, does not give all code on client side until needed). Explain why, pros and cons
- Example of remote module execution with Python. 
- Mindsets or ideas or algorithms to to remote module execution on some different language. Example code if possible
