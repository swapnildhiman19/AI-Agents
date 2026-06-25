Excellent. This is the chapter I think is the **most important** in the entire course.

If you truly understand this chapter, **the rest of ADK will feel like common sense instead of framework magic.**

---

# AI Engineering with Google ADK

# Chapter 1 — Meet the Team Behind Your Agent

Before we write a single line of ADK code, imagine you're building an AI company.

Let's call it

> **Swapnil AI Services Pvt. Ltd.**

You have exactly **one employee**.

His name is Gemini.

---

## Day 1

A customer asks

```
Hi
```

Gemini replies

```
Hello!
```

Everything works.

---

Next customer asks

```
What is 143 * 289?
```

Gemini replies.

Still works.

---

Then another customer asks

```
What's the weather in Bangalore?
```

Gemini doesn't know.

Uh oh...

---

Then someone uploads

```
Resume.pdf
```

Gemini doesn't know how to open PDFs.

Another problem.

---

Then someone asks

```
Send this email.
```

Gemini cannot send emails.

More problems.

---

After one week you realize

> **Gemini cannot run an entire AI application by itself.**

Gemini is an amazing **reasoner**.

But an application needs much more.

So you start hiring employees.

---

# The Company

Instead of thinking

```
User
   ↓
Gemini
```

Think

```
                    AI Company

             ┌────────────────────┐
             │                    │
User ───────►│ Reception          │
             │                    │
             │ Manager            │
             │                    │
             │ Workers            │
             │                    │
             │ Memory Room        │
             │                    │
             │ File Storage       │
             │                    │
             └─────────┬──────────┘
                       │
                       ▼
                    Gemini
```

Now let's identify everyone.

---

# Employee 1

## Agent

Most beginners think

> Agent == Gemini

Wrong.

This is probably the biggest misconception.

An **Agent** is **NOT** the LLM.

Think of an Agent as

> **The job description given to an employee.**

For example

```
You are an HR assistant.
```

or

```
You are a Travel Planner.
```

or

```
You are an Email Writer.
```

That instruction creates a personality.

Imagine you hire someone.

You tell them

```
You work in HR.

Always be polite.

Only answer HR questions.
```

That's exactly what an Agent is.

The person doing reasoning is still Gemini.

The Agent simply tells Gemini

**what role to play.**

---

In ADK

```python
root_agent = Agent(
    model="gemini-2.5-flash",
    instruction="""
    You are an HR assistant.
    """
)
```

Notice

The Agent **contains** Gemini.

It isn't Gemini.

---

# Employee 2

## Tool

Suppose Gemini says

```
The weather is probably...
```

Stop.

Don't guess.

Instead

Use a Weather API.

That Weather API is called a Tool.

Think of a Tool as

> **Something the Agent can ask someone else to do.**

Restaurant analogy

Customer

↓

Chef

↓

Chef says

"I don't know today's weather."

↓

Calls Meteorologist

↓

Meteorologist answers

↓

Chef continues cooking.

Meteorologist is a Tool.

---

Examples

```
Weather Tool

Calculator

Database Tool

Gmail Tool

Google Calendar Tool

GitHub Tool

Slack Tool

```

Notice

Gemini reasons.

Tools perform actions.

---

# Employee 3

## Session

This is where beginners become confused.

Imagine Google launches ChatGPT.

10 million users join.

If Google stores everything in

```python
conversation = []
```

Disaster.

Everyone's messages mix.

Instead

Every user gets

their own notebook.

```
Swapnil

↓

Notebook
```

```
Rahul

↓

Notebook
```

That notebook is called

a Session.

---

A Session represents

> **One conversation.**

Not one user.

Not one message.

One conversation.

---

Imagine you close ChatGPT.

Come back tomorrow.

Continue the same conversation.

Still same Session.

Start a new chat.

New Session.

---

Restaurant analogy

Every table gets its own order book.

Table 1

↓

Notebook

Table 2

↓

Notebook

Table 3

↓

Notebook

Those notebooks never mix.

---

# Inside a Session

A Session owns everything related to one conversation.

```
Session

├── Messages

├── State

├── Artifacts

├── Metadata

└── History
```

Notice

State doesn't exist alone.

Artifacts don't exist alone.

They belong to a Session.

---

# Employee 4

## State

Now imagine inside the notebook

there is one page called

```
Facts
```

It contains

```
Name

Swapnil

City

Bangalore

Experience

5
```

Notice

These are facts.

Not conversation.

Conversation

```
User:
Hi

Assistant:
Hello

User:
My name is Swapnil.
```

State

```
name = Swapnil
```

Very different.

---

Conversation is

everything.

State is

important things.

---

Think

Conversation

```
Entire movie
```

State

```
Movie summary
```

---

Another example

Conversation

```
100 messages
```

State

```
customer_id

order_id

language

```

Tiny.

Fast.

Useful.

---

# Employee 5

## Artifact

Imagine another page.

Instead of facts

it stores documents.

```
Resume.pdf

CoverLetter.md

MeetingTranscript.txt

Invoice.pdf
```

Those are Artifacts.

---

State

```
name

age

city
```

Artifact

```
Entire Resume

Entire PDF

Entire CSV

Entire Markdown
```

---

Think

State

Sticky Notes

Artifacts

Filing Cabinet

---

# Employee 6

## Event

This one sounds scary.

It isn't.

Event simply means

> **Something happened.**

Examples

```
User sent a message.

Tool finished.

Artifact created.

LLM replied.

Agent started.

```

Each one is an Event.

Think

Doorbell rings.

That's an event.

Email received.

That's an event.

Customer entered.

That's an event.

Nothing more.

---

Restaurant

Customer arrives.

↓

Event.

Food ready.

↓

Event.

Bill paid.

↓

Event.

---

# Employee 7

## Runner

Now imagine

Who coordinates everyone?

Who says

```
Customer arrived.

↓

Call Agent.

↓

Agent wants Weather Tool.

↓

Call Tool.

↓

Tool finished.

↓

Call Gemini.

↓

Gemini replied.

↓

Save State.

↓

Return Response.
```

Someone has to orchestrate all this.

That someone is called

Runner.

---

Runner is basically

the manager.

He doesn't answer questions.

He coordinates work.

---

Restaurant

Manager

↓

Calls Chef

↓

Calls Waiter

↓

Calls Cashier

↓

Delivers Food

Manager never cooks.

He coordinates.

---

# The Complete Company

Now we finally have

the entire picture.

```
                     USER
                       │
                       ▼
                  Runner
                       │
                       ▼
                  Session
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
 Conversation        State         Artifacts
      │                │                │
      └────────────────┼────────────────┘
                       │
                       ▼
                    Agent
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
      Gemini                    Tools
          │                         │
          └────────────┬────────────┘
                       ▼
                  Response
```

Look carefully.

This diagram is almost the entire architecture of ADK.

---

# Let's Replay a Real Conversation

User types

```
Hi
```

### Step 1

Runner receives message.

---

### Step 2

Runner finds the Session.

```
Session #18
```

---

### Step 3

Runner loads State.

Currently

```
{}
```

---

### Step 4

Runner loads Artifacts.

Currently

```
{}
```

---

### Step 5

Runner asks Agent

```
What should we do?
```

---

### Step 6

Agent prepares prompt.

---

### Step 7

Gemini generates response.

---

### Step 8

Runner stores conversation.

---

### Step 9

Runner returns response.

Done.

---

Second message

```
My name is Swapnil.
```

Runner again

↓

Find Session

↓

Load State

↓

Agent

↓

Gemini

↓

State updated

```
name = Swapnil
```

↓

Conversation saved

↓

Reply

Notice

The Session persists across turns, so the agent can build on what it already knows.

---

# One Thing I Want You to Remember Forever

Most people think

```
Agent

↓

LLM
```

Reality

```
Runner

↓

Session

↓

Agent

↓

LLM

↓

Tools

↓

State

↓

Artifacts
```

The LLM is just one component.

The real engineering happens **around** the LLM.

---

# A Few Questions You Might Be Thinking

You should actually be wondering things like:

* **Who decides what gets stored in State?**
* **Who creates an Artifact?**
* **How does State get updated?**
* **When does `{name}` become `Swapnil`?**
* **Where is the Session stored—in memory, on disk, or in a database?**
* **If the agent calls three tools, who coordinates them?**
* **Why doesn't the Agent itself manage the Session?**

Those are exactly the questions we'll answer next.

---

# Chapter 2 Is Where Everything Becomes Real

So far we've built the mental model.

In the next chapter, we'll stop talking in abstractions and build a real ADK project from scratch.

We will **not** assume that `state` or `artifacts` already exist.

We'll watch them come into existence naturally:

1. The user introduces themselves.
2. A tool extracts structured information.
3. State is populated.
4. Another agent consumes that state.
5. The agent generates a resume.
6. The resume becomes an artifact.
7. Another agent reads that artifact to create a cover letter.
8. We'll inspect every object after every step so you can literally see what ADK is storing internally.

That project will answer the remaining "who creates what, when, and why" questions with actual runnable code rather than assumptions.
