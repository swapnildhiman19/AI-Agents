Perfect. This is where the course really begins.

Everything before this was architecture. From now on, we'll write code—but **only after understanding why we're writing it**.

---

# AI Engineering with Google ADK

# Chapter 2 — Building Our First Real ADK Application

## Before writing a single line of code...

I want to ask you a question.

Imagine you're Google.

Someone says:

> "Build an AI assistant that helps users generate resumes."

What's the very first thing you need?

Most people answer:

> "An Agent."

Actually...

**No.**

Let's think about what really happens.

---

# Our Product

We're building

```
AI Resume Assistant
```

A user visits our website.

Initially...

The system knows absolutely nothing.

```
User
↓

"Hi"
```

That's all.

No memory.

No resume.

No state.

No artifacts.

Nothing.

Let's visualize that.

```
Session

Conversation:
(empty)

State:
{}

Artifacts:
{}
```

Notice something.

We're not assuming anything exists.

Everything starts empty.

Exactly like a real production system.

---

# Conversation 1

The user types

```
Hi
```

Our application receives it.

Let's pause.

Who receives it?

Earlier we learned

```
User

↓

Runner
```

The Runner looks for a Session.

Does one exist?

No.

So it creates one.

```
Session #A123

Conversation

State

Artifacts
```

Everything empty.

---

## Then the Runner calls the Agent

The Agent currently has one instruction.

```python
instruction="""
You are a friendly Resume Assistant.
"""
```

Gemini replies

```
Hello!
I'm happy to help you create your resume.
```

The Runner stores the conversation.

Session becomes

```
Conversation

User:
Hi

Assistant:
Hello!

State

{}

Artifacts

{}
```

Still...

No state.

No artifacts.

---

# Conversation 2

Now the user says

```
My name is Swapnil.
```

Now something interesting happens.

Should this simply become another message?

Or...

Should we remember the name?

Think carefully.

If tomorrow the user asks

```
Generate my resume.
```

Would we like to remember the name?

Obviously yes.

So now we need to extract

```
Swapnil
```

from

```
My name is Swapnil.
```

Question.

Who should do that?

---

There are several possibilities.

### Option A

Gemini remembers it magically.

Impossible.

LLMs don't store memory.

---

### Option B

The Runner parses English.

Bad idea.

The Runner shouldn't understand language.

---

### Option C

The Agent itself updates state.

Possible...

but then every Agent would need memory logic.

Messy.

---

### Option D

Use a Tool.

Interesting...

A Tool can specialize in extracting structured information.

This is exactly what many production systems do.

---

# Our First Tool

Let's imagine we build

```python
extract_user_information()
```

It receives

```
"My name is Swapnil."
```

It returns

```python
{
    "name": "Swapnil"
}
```

Notice.

The Tool is **not** generating English.

It is generating structured data.

Huge difference.

---

# First Important Question

Who updates the State?

Many beginners think

> The Tool.

Not exactly.

The Tool only returns information.

Something else writes it into the Session.

Let's see.

---

Current Session

```
Conversation

User:
Hi

Assistant:
Hello!

State

{}

Artifacts

{}
```

Tool returns

```python
{
    "name": "Swapnil"
}
```

The Runner says

```
Great.

I'll save that.
```

State becomes

```
State

{
    "name":"Swapnil"
}
```

Notice the responsibility.

Tool

↓

Extracts information.

Runner

↓

Stores information.

---

This separation is beautiful.

Why?

Imagine tomorrow you replace the Tool.

Nothing changes.

State storage still works.

---

# Stop Here

I want you to notice something.

We haven't written any ADK code yet.

And that's intentional.

Because I don't want you memorizing APIs.

I want you to understand responsibilities.

Every component has exactly one job.

| Component | Responsibility              |
| --------- | --------------------------- |
| Runner    | Orchestrates everything     |
| Session   | Stores conversation data    |
| Agent     | Decides what should happen  |
| Tool      | Performs a specialized task |
| State     | Stores structured facts     |
| Artifact  | Stores large content        |

Notice nobody has two jobs.

That's excellent software design.

---

# Now Let's Introduce Real ADK Code

Suppose we have this simple agent.

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="resume_assistant",
    model="gemini-2.5-flash",
    instruction="""
You are a resume assistant.

Help users build professional resumes.
"""
)
```

This is familiar.

Nothing new.

---

Now let's add our Tool.

Imagine

```python
def extract_name(user_message):
    ...
```

Question.

Where does this Tool get called?

You might think

```
User

↓

Tool

↓

Agent
```

Actually...

No.

The Runner is still the manager.

```
User

↓

Runner

↓

Agent

↓

Agent decides

↓

Call Tool

↓

Tool returns

↓

Runner stores State

↓

Agent continues

↓

Gemini

↓

Response
```

See how important the Runner is?

It is quietly coordinating everything.

---

# Here's the Problem With Continuing This Way

At this point we have reached something important.

If I keep inventing pseudo-code like:

```python
extract_name(...)
```

or

```python
Runner stores state
```

I'll actually be teaching you **my version** of ADK instead of **Google's implementation**.

And I don't want that.

---

# I think we should now switch to the real ADK APIs

Up until now, we've deliberately stayed away from framework-specific code because we were building the mental model.

From this point onward, I want every example to use the **actual ADK classes and APIs**—the same ones you'll use in your projects.

That means we'll answer questions like:

* How does a tool actually update `state` in ADK?
* How do you create an artifact in real ADK?
* What does the `ToolContext` object contain?
* Where does the `Session` come from?
* What code do you write versus what ADK does automatically?

We'll build the same Resume Assistant, but using the real framework instead of pseudo-code.

---

## My proposal for the rest of the course

From here on, every chapter will have this format:

1. **The engineering problem** (why this feature exists).
2. **The actual ADK API** that solves it.
3. **A complete runnable project**.
4. **A line-by-line explanation** of every class, function, and callback.
5. **An execution trace** showing exactly how `Session`, `State`, and `Artifacts` change after each user message.

I think that's the point where the learning becomes truly practical.

**One thing I'll do before writing the next lesson:** I'll base it on the current ADK APIs rather than memory, so every class, method, and callback you see is accurate and runnable with the latest ADK version. That way you won't have to "unlearn" anything later.
