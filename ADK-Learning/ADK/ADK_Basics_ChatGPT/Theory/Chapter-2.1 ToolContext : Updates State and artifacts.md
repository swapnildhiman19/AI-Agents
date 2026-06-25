Excellent. This is where we stop being **ADK users** and start becoming **AI engineers**.

I'm going to teach this as if you joined the Google ADK team and someone asked you:

> **"Can you explain why ToolContext exists?"**

By the end of today's lesson, you'll know the answer.

---

# AI Engineering with Google ADK

# Chapter 2 — Building Our First Stateful Agent

Today we're going to build something extremely small.

Not a Resume Assistant.

Not a Multi-Agent System.

Just this:

```text
User:
Hi

Assistant:
Hello!

User:
My name is Swapnil.

Assistant:
Nice to meet you Swapnil!

User:
What's my name?

Assistant:
Your name is Swapnil.
```

That's it.

But...

We're going to understand **every single object** involved.

---

# Step 0 — Forget ADK Again

Let's pretend ADK doesn't exist.

You ask me to build this application.

How would I do it?

My first attempt would probably be

```python
conversation = []
```

Whenever user types

```text
"My name is Swapnil"
```

I'll append

```python
conversation.append({
    "role":"user",
    "text":"My name is Swapnil"
})
```

Works.

---

Now user asks

```text
What's my name?
```

Now I have a problem.

Should I send Gemini

```text
What's my name?
```

or

```text
Hi

Hello

My name is Swapnil

Nice to meet you

What's my name?
```

Obviously the second one.

So conversation history solves this.

---

# But...

Imagine after 300 messages.

Conversation becomes

```text
Hi

Hello

...

...

...

...

...

...

My favourite movie is Interstellar

...

...

...

...

...

...

What's my favourite movie?
```

Should Gemini read 300 messages just to answer that?

Not ideal.

---

This is where Google asked themselves

> **Can we separate "conversation" from "important facts"?**

Answer:

Yes.

---

Instead of

```text
Conversation

Hi

Hello

My name is Swapnil

...

300 messages...
```

We'll also maintain

```python
state = {

"name":"Swapnil",

"favorite_movie":"Interstellar"

}
```

Notice

Conversation didn't disappear.

We added another layer.

---

# This is the First Big Idea

Conversation answers

> **What happened?**

State answers

> **What do we currently know?**

Those are completely different questions.

---

Example

Conversation

```text
User:
My favourite color is blue.

Assistant:
Great.

User:
Actually make it red.

Assistant:
Done.
```

State

```python
{
"favorite_color":"red"
}
```

See?

Conversation contains history.

State contains the latest truth.

This distinction is fundamental. A session tracks both: the **chronological events** (history) and the **current state** (facts). ([Medium][1])

---

# Now let's finally use REAL ADK.

Not pseudo-code.

Real ADK.

---

# Our first Tool

```python
from google.adk.tools.tool_context import ToolContext

def remember_name(
    name: str,
    tool_context: ToolContext,
) -> dict:
    """
    Save the user's name.
    """

    tool_context.state["name"] = name

    return {
        "status": "success",
        "message": f"I'll remember your name is {name}"
    }
```

Let's stop.

Don't read further.

This tiny function teaches half of ADK.

---

# Question 1

Who created

```python
tool_context
```

You?

No.

---

Google?

No.

---

Gemini?

No.

---

The Runner?

**Yes.**

Think restaurant.

Customer

↓

Runner

↓

Agent

↓

Agent decides

"I need the remember_name tool."

↓

Runner calls

```python
remember_name(...)
```

Before calling it,

the Runner creates

```python
ToolContext(...)
```

and injects it automatically.

You never instantiate `ToolContext` yourself. ADK injects it into tool functions so they can safely interact with the current session. ([Google Cloud][2])

---

# Question 2

What exactly is ToolContext?

Beginners think

> It's some helper object.

Technically yes.

Conceptually...

Think of it as

> **The tool's window into the current conversation.**

Without ToolContext

the tool knows nothing.

With ToolContext

the tool suddenly knows

* current Session
* current State
* current Artifacts
* authentication
* other runtime services

Think of ToolContext as the "backpack" ADK hands to every tool before it starts working. ([Medium][3])

---

# Let's inspect ToolContext

Conceptually

Imagine it contains

```python
ToolContext(

session=...

state=...

artifact_service=...

memory=...

)
```

Notice

Your tool never talks to Session directly.

It only talks through ToolContext.

Why?

Beautiful software engineering.

It reduces coupling.

---

# Look at this line

```python
tool_context.state["name"] = name
```

This single line is magical.

Let's see what actually happens.

Initially

```python
Session

state = {}
```

User says

```text
My name is Swapnil
```

LLM decides

"I should call remember_name."

Runner executes

```python
remember_name(
    name="Swapnil",
    tool_context=...
)
```

Inside tool

```python
tool_context.state["name"] = "Swapnil"
```

Immediately Session becomes

```python
state = {

"name":"Swapnil"

}
```

Notice

We never touched Session directly.

We only modified

```python
tool_context.state
```

ADK propagates those changes back into the session safely. Updating `tool_context.state` is the recommended way for tools to write session state. ([Ravikanth Chaganti][4])

---

# Another amazing thing

Now imagine another tool

```python
def greet(tool_context):

    print(tool_context.state["name"])
```

Output

```text
Swapnil
```

Different tool.

Same state.

Why?

Because

they're in the same Session.

Think of Session as the notebook.

Every employee reads the same notebook.

---

# Here's where `{name}` comes from

Remember this?

```python
instruction="""

You are helpful.

Current user:

{name}
"""
```

Question

Where does `{name}` come from?

Gemini?

No.

Python?

No.

Tool?

No.

---

It comes from

```python
tool_context.state["name"]
```

Earlier we stored

```python
tool_context.state["name"] = "Swapnil"
```

Later

Before Gemini is called,

ADK says

```python
instruction

↓

Find {name}

↓

Read Session.state["name"]

↓

Replace it

↓

Send final prompt
```

Suppose instruction was

```text
You are helpful.

Current user:

{name}
```

ADK transforms it into

```text
You are helpful.

Current user:

Swapnil
```

Then Gemini receives it.

The LLM never sees `{name}`. ADK performs the substitution from session state before each model call. ([Google Cloud][2])

---

# Now let's introduce Artifacts

Imagine user says

```text
Generate my resume.
```

Gemini produces

```markdown
# Resume

Swapnil Dhiman

Senior iOS Engineer

...
```

Question.

Should this go into state?

Imagine

```python
state["resume"] = """
4000 words...
"""
```

Terrible.

State should stay lightweight.

Instead

ADK provides

```python
tool_context.save_artifact(...)
```

A tool can save a document as an artifact associated with the current session (or user), and ADK versions it for you. ([Adk][5])

Conceptually

```python
resume = types.Part.from_text("""
# Resume

Swapnil

...
""")

tool_context.save_artifact(

filename="resume.md",

artifact=resume

)
```

Now Session becomes

```text
Session

State

name

Swapnil

Artifacts

resume.md
```

Notice

State stayed tiny.

Artifact stored the large document.

---

# Finally, Everything Connects

Let's replay the entire flow.

```
User
│
│  "My name is Swapnil"
▼
Runner
│
▼
Agent
│
│ decides:
│ "Call remember_name"
▼
remember_name Tool
│
│ tool_context.state["name"] = "Swapnil"
▼
Session State Updated
│
▼
Later...
│
User:
Generate resume
│
▼
Runner
│
▼
Agent Instruction

Current user:
{name}

▼
ADK substitutes

{name}

↓

Swapnil

▼
Gemini

▼
Resume Generated

▼
save_artifact()

▼
Artifacts

resume.md
```

---

# The Biggest Misconception (and Why I Delayed Code)

Most tutorials accidentally teach this mental model:

```
Tool

↓

State
```

But the real picture is:

```
Session
│
├── Events (conversation history)
├── State (structured facts)
└── Artifacts (large documents/files)
        ▲
        │
   ToolContext
        ▲
        │
      Tool
```

The tool **never owns the state**.

The **Session owns the state**.

The tool merely receives **temporary permission** (through `ToolContext`) to read and modify the session's state and artifacts.

That single design decision explains almost the entire ADK architecture.

---

## Homework (No Coding Yet)

Before we write our first complete project, I want you to be able to answer these questions without looking them up:

1. Why isn't `state` just a global Python dictionary?
2. Why doesn't a tool receive the `Session` directly?
3. Why does `ToolContext` exist?
4. Why shouldn't a resume be stored in `state`?
5. Who actually replaces `{name}` with `"Swapnil"`?
6. If two different tools use `tool_context.state`, why do they see the same values?

If you can answer those, you've already understood more about ADK's architecture than many people who have built several demo agents.

### Next Chapter

Now we'll build a **real, runnable ADK project**. Not pseudo-code.

We'll create:

* A tool that remembers the user's name.
* A tool that remembers years of experience.
* An agent that uses `{name}` and `{experience}` in its instructions.
* A tool that generates and saves a resume as an artifact.
* Another agent that reads that artifact to write a cover letter.

After **every single user message**, we'll stop and inspect:

* The session state
* The artifacts
* The exact prompt ADK sends to Gemini
* Which component changed what

You'll be able to watch the entire system evolve step by step, just like a debugger for ADK.

[1]: https://medium.com/google-cloud/how-adk-agents-remember-sessions-events-and-persistent-state-742e06e9568c?utm_source=chatgpt.com "How ADK Agents Remember: Sessions, Events, and ..."
[2]: https://cloud.google.com/blog/topics/developers-practitioners/remember-this-agent-state-and-memory-with-adk?utm_source=chatgpt.com "Remember this: Agent state and memory with ADK"
[3]: https://addozhang.medium.com/google-adk-deep-dive-part-2-specialized-context-objects-in-different-contexts-1cd8a2de6655?utm_source=chatgpt.com "Google ADK Deep Dive (Part 2): Specialized Context Objects ..."
[4]: https://ravichaganti.com/blog/google-adk-sessions-state-and-memory/?utm_source=chatgpt.com "Google ADK - Sessions, state, and memory"
[5]: https://adk.dev/artifacts/?utm_source=chatgpt.com "Artifacts - Agent Development Kit (ADK)"
