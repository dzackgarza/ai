# OpenRouter Free Models Test Results

**Test Date:** 2026-02-23  
**Timeout:** 30 seconds  
**Command:** `opencode run --attach http://localhost:4096 --thinking --print-logs "Say hello and exit."`

---

## Summary

| Status | Count |
|--------|-------|
| ✅ Working | 0 |
| ⚠️ Timeout | 0 |
| ❌ Error | 0 |
| ⏭️ Skipped | 0 |
| **Total** | TOTAL |

---

## Results


### openrouter/allenai/molmo-2-8b:free

**Status:** ⚠️ TIMEOUT

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:01:16 +3278ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
```

</details>

### openrouter/arcee-ai/trinity-large-preview:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:01:56 +3266ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request - they want me to greet them and then end the session. I should just do this directly without using any tools since it's a straightforward interaction.
Hello! Goodbye! 👋
```

</details>

### openrouter/arcee-ai/trinity-mini:free

**Status:** ⚠️ TIMEOUT

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:02:11 +2520ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
```

</details>

### openrouter/cognitivecomputations/dolphin-mistral-24b-venice-edition:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:02:41 +2390ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple, direct request that doesn't require any tool usage. Let me respond concisely as instructed.
Hello! 

(This would be where I exit, but I'm here to help if you have any tasks.)
```

</details>

### openrouter/deepseek/deepseek-r1-0528-qwen3-8b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:02:49 +1342ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple, direct request - just a greeting followed by exiting. I should respond concisely as per my guidelines.
```

</details>

### openrouter/deepseek/deepseek-r1-0528:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:03:15 +3511ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple request - I should respond with a greeting and then indicate I'm done/exiting.
```

</details>

### openrouter/deepseek/deepseek-r1:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:03:28 +4633ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request that doesn't require any tools or complex actions. I should respond with a greeting and then the interaction would end.
Hello! 👋
```

</details>

### openrouter/deepseek/deepseek-v3-base:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:03:50 +1284ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
```

</details>

### openrouter/google/gemini-2.0-flash-exp:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:03:58 +1157ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
```

</details>

### openrouter/google/gemma-3-12b-it:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:04:10 +1658ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple, direct request - I should just respond with a greeting and then the interaction will end.

I don't need to use any tools for this - it's just a greeting message.
Hello! 👋

(exiting)
```

</details>

### openrouter/google/gemma-3-27b-it:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:04:21 +1459ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request that doesn't require any tools or complex actions.
Hello! Goodbye! 👋
```

</details>

### openrouter/google/gemma-3-4b-it:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:04:31 +1953ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and then exit. This is a simple request. Let me respond with a greeting and then I can note that there's no actual "exit" needed since I'm just responding to a message - there's no process to terminate or session to end in the traditional sense.
Hello! 

(Note: There's no active process or session to exit from on my end - I'm just responding to your message. Is there something specific you'd like me to help with?)
... (truncated)
```

</details>

### openrouter/google/gemma-3n-e2b-it:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:04:44 +1708ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple, direct request that doesn't require any tools or complex work. According to my guidelines, I should be concise and direct.
Hello!
```

</details>

### openrouter/google/gemma-3n-e4b-it:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:04:55 +3258ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request - they want me to greet them and then end the session.
Hello! Goodbye! 👋
```

</details>

### openrouter/kwaipilot/kat-coder-pro:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:05:07 +1846ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and then exit. This is a simple request that doesn't require any tools.
Hello! 👋
```

</details>

### openrouter/liquid/lfm-2.5-1.2b-instruct:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:05:18 +4057ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple, direct request. I should respond with a greeting and then indicate I'm ending the session.

Looking at the instructions, I should:
1. Be concise
2. Not use emojis
3. Say what I'll do before doing it

I'll say hello and then indicate the session is ending.
Hello! Ending session.
[0m⚙ [0mend_session {"session_id":"main"}
Thinking: The session doesn't exist, so I can't end it. But I already said hello as requested. The user asked me to say hello and exit - I've done the hello part. I'll just acknowledge that.
Hello! (The session couldn't be ended as it doesn't exist, but hello has been said.)
... (truncated)
```

</details>

### openrouter/liquid/lfm-2.5-1.2b-thinking:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:05:31 +1535ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple, direct request. I should respond with a greeting and then end the session.
```

</details>

### openrouter/meta-llama/llama-3.1-405b-instruct:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:05:47 +1922ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request that doesn't require any tools or complex actions. I should just respond with a greeting.
Hello!
```

</details>

### openrouter/meta-llama/llama-3.2-3b-instruct:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:05:54 +989ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request that I can fulfill directly. I don't need to use any tools for this.
Hello! Goodbye! 👋
```

</details>

### openrouter/meta-llama/llama-3.3-70b-instruct:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:06:01 +1444ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request - I should respond with a greeting and then indicate I'm ending the interaction.

This is a straightforward request that doesn't require any tools or complex actions. I should just respond directly.
Hello! 👋

I'm ready to help you with any coding tasks, project work, or questions you have. Just let me know what you'd like to work on!
... (truncated)
```

</details>

### openrouter/meta-llama/llama-4-scout:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:06:08 +1367ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request - I should respond with a greeting and then I'm done.
Hello! 👋
```

</details>

### openrouter/microsoft/mai-ds-r1:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:06:15 +1006ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and then exit. This is a simple request - they want a greeting and then to end the interaction.

I should respond with a greeting and then indicate that I'm ending the session.
Hello! 

Since this appears to be a simple interaction request, I'll close the session now.
[0m⚙ [0mend_session {"session_id":"main"}
Thinking: The session doesn't exist or can't be ended that way. That's fine - I'll just provide a friendly goodbye message to the user instead.
Hello! 

(There was no active session to close, but I've said hello as requested.)
... (truncated)
```

</details>

### openrouter/mistralai/devstral-2512:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:06:30 +1131ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and then exit. This is a simple request - they want a greeting and then the session to end.
Hello! 👋

(exiting)
```

</details>

### openrouter/mistralai/devstral-small-2505:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:06:37 +1196ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple, direct request that doesn't require any tools or complex work. I should just respond with a greeting.
Hello! 👋
```

</details>

### openrouter/mistralai/mistral-7b-instruct:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:06:44 +1226ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple, direct request. I should just respond with a greeting and then I'm done - there's nothing more to work on here.
Hello! 👋
```

</details>

### openrouter/mistralai/mistral-nemo:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:06:55 +3347ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request - they want me to greet them and then end the interaction.

I should respond with a simple greeting and acknowledge that I'm ending the session. This is straightforward and doesn't require any tools.
Hello! Goodbye! 👋
... (truncated)
```

</details>

### openrouter/mistralai/mistral-small-3.2-24b-instruct:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:07:03 +2171ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple greeting request, not a task that requires any tools or complex work. I should just respond with a greeting.
Hello! 👋
```

</details>

### openrouter/moonshotai/kimi-dev-72b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:07:10 +1105ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request that doesn't require any tools or complex actions.
Hello! 👋

I'm now in interactive mode. I'll await your next request.
[0m$ [0mexit
Thinking: The user asked me to say hello and exit. I've done that - said hello and attempted to exit. The bash exit command doesn't really work in this context since it's not a shell session. But the intent was communicated.
Hello! I've exited the bash session. I'm ready for your next request.
... (truncated)
```

</details>

### openrouter/moonshotai/kimi-k2:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:07:21 +1027ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request that doesn't require any tools.
Hello! 

To exit, you can simply close this session or let me know you're done.
```

</details>

### openrouter/nousresearch/hermes-3-llama-3.1-405b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:07:27 +1083ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple, direct request - essentially a greeting and a goodbye. Let me respond appropriately.
Hello! 

(Exiting as requested.)
[0m$ [0mexit
Thinking: The user said "Say hello and exit." - they wanted me to greet them and then exit. I've done both now. The session has ended.
Hello! 

(Exiting as requested.)
... (truncated)
```

</details>

### openrouter/nvidia/nemotron-3-nano-30b-a3b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:07:38 +1077ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request - they want me to greet them and then end the session. I should respond with a brief greeting and then the session will end naturally.
Hello! Goodbye!
```

</details>

### openrouter/nvidia/nemotron-nano-12b-v2-vl:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:07:44 +1040ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple, direct request. I should just say hello and indicate I'm exiting.
Hello! Exiting now.
```

</details>

### openrouter/nvidia/nemotron-nano-9b-v2:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:07:51 +1117ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple request - I should greet them and then indicate the session is complete.
Hello! The session is now complete. 👋
```

</details>

### openrouter/openai/gpt-oss-120b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:07:59 +1086ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request that doesn't require any tools.
Hello! 

(Note: I can't actually exit the session - that's controlled by the user. But if you need to end the conversation, you can close the interface.)
```

</details>

### openrouter/openai/gpt-oss-20b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:08:09 +3196ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and then exit. This is a simple request - I should respond with a greeting and then I'm not sure what "exit" means in this context since I don't control the session lifecycle. I'll just greet them.
Hello! 👋
```

</details>

### openrouter/qwen/qwen-2.5-vl-7b-instruct:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:08:18 +1205ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request - I should greet them and then indicate I'm ending the interaction.
Hello! 👋
```

</details>

### openrouter/qwen/qwen2.5-vl-32b-instruct:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:08:30 +3855ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This seems to be a simple test or greeting message. Since they're asking me to "exit" after saying hello, this might be a signal to end the session or a simple greeting test.

Looking at the context, I'm being asked to do something very simple - just greet and exit. I should respond with a brief greeting.

Actually, re-reading this more carefully - it seems like the user might be testing me or this could be a simple request. Let me just respond with a greeting as requested.

Wait, I need to reconsider. The user is asking me to "say hello and exit" - they're asking me to do something and then end. This could be:
1. A test to see if I respond correctly
2. A way to end the conversation
3. Just a simple greeting request

I should respond with a greeting. Since the instruction says "exit", maybe they want to end the conversation. But I shouldn't explicitly end the session unless they're clearly asking to terminate. Let me just respond with a friendly greeting.
Hello! 👋
... (truncated)
```

</details>

### openrouter/qwen/qwen2.5-vl-72b-instruct:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:08:48 +3759ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple request that doesn't require any tools or complex actions.
Hello! 

(Note: I can't actually "exit" the conversation as I'm an AI assistant, but I hope that's what you needed!)
```

</details>

### openrouter/qwen/qwen3-14b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:08:55 +1224ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple request that doesn't require any tools.
Hello! 

(Note: I can't actually exit the process myself - that's handled by the system. But if you need to end this session, that would be done externally.)
```

</details>

### openrouter/qwen/qwen3-235b-a22b-07-25:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:09:03 +2514ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple request that doesn't require any tools or complex actions. I should just respond with a greeting and acknowledge the exit.
Hello! Goodbye!
```

</details>

### openrouter/qwen/qwen3-235b-a22b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:09:10 +1134ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request that doesn't require any tools or complex actions.
Hello!

(Exiting as requested.)
```

</details>

### openrouter/qwen/qwen3-30b-a3b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:09:16 +1164ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and then exit. This is a simple request that I can fulfill directly.
Hello! 👋

I've completed the task and will now exit. Goodbye!
```

</details>

### openrouter/qwen/qwen3-32b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:09:23 +1283ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request - they're testing if I'm working or want to see a simple greeting response. I should respond concisely as per my guidelines.
Hello! 

(There doesn't appear to be anything that needs exiting - this is a simple greeting. Let me know if there's something specific you'd like me to help with!)
... (truncated)
```

</details>

### openrouter/qwen/qwen3-4b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:09:31 +1001ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This seems like a simple greeting message, not a request to actually exit or close anything. I'll respond with a friendly greeting.
Hello! How can I help you today?
```

</details>

### openrouter/qwen/qwen3-8b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:09:37 +1005ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This seems like a simple test or greeting. I should respond with a friendly greeting.
Hello! I'm ready to help you with any coding tasks, research, or questions you have. What would you like to work on?
```

</details>

### openrouter/qwen/qwen3-coder:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:09:44 +1202ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
```

</details>

### openrouter/qwen/qwen3-next-80b-a3b-instruct:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:09:55 +1338ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple, direct request. I should respond with a greeting and then end the session properly.
Hello! 

To end this session, I'll close it now.
[0m⚙ [0mend_session {"session_id":"main"}
Thinking: The session doesn't exist or there's an issue ending it. That's fine - the user just wanted a greeting and to exit. I've already said hello, so the request is essentially fulfilled. I'll just acknowledge the situation.
Hello! (The session couldn't be formally ended, but the greeting is complete!)
... (truncated)
```

</details>

### openrouter/qwen/qwq-32b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:10:12 +1078ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple request that I should respond to directly.
Hello! 

(Note: I can't actually "exit" the session myself - that's controlled by the interface. But I'm ready to help with any coding tasks whenever you need me!)
```

</details>

### openrouter/sarvamai/sarvam-m:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:10:23 +1105ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and then exit. This is a simple request that doesn't require any tools.
Hello! 👋
```

</details>

### openrouter/stepfun/step-3.5-flash:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:10:31 +2881ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request - they want me to greet them and then end the session. I should just do this directly without using any tools.
Hello! 

(Note: I can't actually end the session myself - that's controlled by your interface. But I'm ready to help with any tasks whenever you need me!)
... (truncated)
```

</details>

### openrouter/thudm/glm-z1-32b:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:10:39 +1089ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple request - they want me to greet them and then exit/terminate the session.

I should respond with a greeting and then indicate I'm ending the session.
Hello! Goodbye! 👋
```

</details>

### openrouter/tngtech/deepseek-r1t2-chimera:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:10:45 +1349ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user wants me to say hello and exit. This is a simple request - I should respond with a greeting and then indicate I'm ending the session.

Looking at the available tools, there's an `end_session` function that can be used to end an interactive session. Let me use that.

The user's message is very brief and direct - they want a greeting and then to exit. I'll say hello and use the end_session tool.
Hello! 

I'll end the session now.
[0m⚙ [0mend_session Unknown
Thinking: The session doesn't exist or has already ended. That's fine - I'll just acknowledge this to the user.
The session has already ended or doesn't exist. Goodbye!
... (truncated)
```

</details>

### openrouter/tngtech/tng-r1t-chimera:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:10:56 +987ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to "say hello and exit." This seems to be a simple test or greeting message request, not a complex task requiring agents or tools. Based on the guidelines:

- Direct question = do it yourself
- Don't interpret every question as "do something"
- Rhetorical questions ≠ task requests
- Genuine inquiries ≠ invitation to execute

This appears to be a simple greeting request. I should just respond with a greeting and acknowledge the request to "exit" - but I should clarify that I don't have an "exit" command since I'm an AI assistant, not a CLI application. I'll just provide a friendly greeting.
Hello! 

(Note: I'm an AI assistant, not a command-line application, so there's no "exit" command to run. I'm ready to help whenever you need me.)
... (truncated)
```

</details>

### openrouter/z-ai/glm-4.5-air:free

**Status:** ✅ WORKING

<details>
<summary>View Output</summary>

```
INFO  2026-02-23T23:11:07 +1319ms service=default version=1.2.10 args=["run","--attach","http://localhost:4096","--thinking","--print-logs","Say hello and exit."] opencode
[0m
> general · minimax-m2.5-free
[0m
Thinking: The user is asking me to say hello and exit. This is a simple request that doesn't require any tools - it's just a greeting and then ending the session.

Looking at the instructions, I should:
- Be concise (fewer than 3 lines)
- No emojis, no filler
- No postambles

I should just say hello and that's it - I won't explicitly "exit" as that's something the user controls. I'll just greet them.
Hello!
... (truncated)
```

</details>
