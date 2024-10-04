# LangGraph Memory Service

[![CI](https://github.com/langchain-ai/memory-template/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/langchain-ai/memory-template/actions/workflows/unit-tests.yml)
[![Integration Tests](https://github.com/langchain-ai/memory-template/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/langchain-ai/memory-template/actions/workflows/integration-tests.yml)
[![Open in - LangGraph Studio](https://img.shields.io/badge/Open_in-LangGraph_Studio-00324d.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4NS4zMzMiIGhlaWdodD0iODUuMzMzIiB2ZXJzaW9uPSIxLjAiIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHBhdGggZD0iTTEzIDcuOGMtNi4zIDMuMS03LjEgNi4zLTYuOCAyNS43LjQgMjQuNi4zIDI0LjUgMjUuOSAyNC41QzU3LjUgNTggNTggNTcuNSA1OCAzMi4zIDU4IDcuMyA1Ni43IDYgMzIgNmMtMTIuOCAwLTE2LjEuMy0xOSAxLjhtMzcuNiAxNi42YzIuOCAyLjggMy40IDQuMiAzLjQgNy42cy0uNiA0LjgtMy40IDcuNkw0Ny4yIDQzSDE2LjhsLTMuNC0zLjRjLTQuOC00LjgtNC44LTEwLjQgMC0xNS4ybDMuNC0zLjRoMzAuNHoiLz48cGF0aCBkPSJNMTguOSAyNS42Yy0xLjEgMS4zLTEgMS43LjQgMi41LjkuNiAxLjcgMS44IDEuNyAyLjcgMCAxIC43IDIuOCAxLjYgNC4xIDEuNCAxLjkgMS40IDIuNS4zIDMuMi0xIC42LS42LjkgMS40LjkgMS41IDAgMi43LS41IDIuNy0xIDAtLjYgMS4xLS44IDIuNi0uNGwyLjYuNy0xLjgtMi45Yy01LjktOS4zLTkuNC0xMi4zLTExLjUtOS44TTM5IDI2YzAgMS4xLS45IDIuNS0yIDMuMi0yLjQgMS41LTIuNiAzLjQtLjUgNC4yLjguMyAyIDEuNyAyLjUgMy4xLjYgMS41IDEuNCAyLjMgMiAyIDEuNS0uOSAxLjItMy41LS40LTMuNS0yLjEgMC0yLjgtMi44LS44LTMuMyAxLjYtLjQgMS42LS41IDAtLjYtMS4xLS4xLTEuNS0uNi0xLjItMS42LjctMS43IDMuMy0yLjEgMy41LS41LjEuNS4yIDEuNi4zIDIuMiAwIC43LjkgMS40IDEuOSAxLjYgMi4xLjQgMi4zLTIuMy4yLTMuMi0uOC0uMy0yLTEuNy0yLjUtMy4xLTEuMS0zLTMtMy4zLTMtLjUiLz48L3N2Zz4=)](https://langgraph-studio.vercel.app/templates/open?githubUrl=https://github.com/langchain-ai/memory-template)

## Motivation

Memory lets your AI applications learn from each user interaction. It makes them more effective as they learn from mistakes and engaging as they adapt to personal tastes. This template shows you how to build and deploy a long-term memory service that you can connect to from any LangGraph agent so they can manage user-scoped memories.

![Motivation](./static/memory_motivation.png)

## Quickstart

Create a `.env` file.

```bash
cp .env.example .env
```

Set the required API keys in your `.env` file.

<!--
Setup instruction auto-generated by `langgraph template lock`. DO NOT EDIT MANUALLY.
-->

### Setup Model

The defaults values for `model` are shown below:

```yaml
model: anthropic/claude-3-5-sonnet-20240620
```

Follow the instructions below to get set up, or pick one of the additional options.

#### Anthropic

To use Anthropic's chat models:

1. Sign up for an [Anthropic API key](https://console.anthropic.com/) if you haven't already.
2. Once you have your API key, add it to your `.env` file:

```
ANTHROPIC_API_KEY=your-api-key
```

#### OpenAI

To use OpenAI's chat models:

1. Sign up for an [OpenAI API key](https://platform.openai.com/signup).
2. Once you have your API key, add it to your `.env` file:

```
OPENAI_API_KEY=your-api-key
```

<!--
End setup instructions
-->

[Open this template](https://langgraph-studio.vercel.app/templates/open?githubUrl=https://github.com/langchain-ai/memory-template) in LangGraph studio to get started and navigate to the `chatbot` graph.

_If you want to deploy to the cloud, [follow these instructions to deploy this repository to LangGraph Cloud](https://langchain-ai.github.io/langgraph/cloud/) and use Studio in your browser._

![Flow](./static/studio.png)

Try chatting with the bot. Saying your name and other the bot may want to remember.

Wait ~10-20 seconds for memories to be created and saved.

Create a _new_ thread using the `+` icon and chat with the bot again.

The bot should have access to the memories you've saved, and will use them to personalize its responses.

## How it works

An effective memory service should address some key questions:

1. What should each memory contain?
2. How should memories be updated? (and on what schedule?)
3. How should your bot recall memories?

The "correct" answer to these questions can be application-specific. We'll address these challenges below, and explain how this template lets you flexibly
configure what and how memories are managed to keep your bot's memory on-topic and up-to-date. First, we'll talk about how you configure "what each memory should contain" using memory schemas.

### Memory Schemas

Memory schemas tell the service the "shape" of individual memories and how to update them. You can define any custom memory schema by providing `memory_types` as configuration. Let's review the [two default schemas](./src/memory_graph/configuration.py) we've provided along the template to get a better sense of what they are doing.

The first schema is the `User` profile schema, copied below:

```json
{
  "name": "User",
  "description": "Update this document to maintain up-to-date information about the user in the conversation.",
  "update_mode": "patch",
  "parameters": {
    "type": "object",
    "properties": {
      "user_name": {
        "type": "string",
        "description": "The user's preferred name"
      },
      "age": {
        "type": "integer",
        "description": "The user's age"
      },
      "interests": {
        "type": "array",
        "items": { "type": "string" },
        "description": "A list of the user's interests"
      },
      "home": {
        "type": "string",
        "description": "Description of the user's home town/neighborhood, etc."
      },
      "occupation": {
        "type": "string",
        "description": "The user's current occupation or profession"
      },
      "conversation_preferences": {
        "type": "array",
        "items": { "type": "string" },
        "description": "A list of the user's preferred conversation styles, pronouns, topics they want to avoid, etc."
      }
    }
  }
}
```

The schema has a name and description, as well as JSON schema parameters that are all passed to an LLM. The LLM infers the values for the schema based on the conversations you send to the memory service.

The schema also has an `update_mode` parameter that defines **how** the service should update its memory when new information is provided. The **patch** update_mode instructs the graph that we should always have a single JSON object to represent this user. When new information is provided, the model can generate "patches", or small updates to extend, delete, or replace content in the current memory document. This type of `update_mode` is useful if you want strict visibility into a user's representation at any given point or if you want to let the end user directly view and update their own representation for the bot. By defining these specific parameters, we are decideing that this (and only this) information is relevant to track and excluding other information (like "relationships" or "religion", etc.) from being tracked. It's an easy way for us to bias the service into focusing on what we think is important for our specific bot.

The second memory schema we provide is the **Note** schema, shown below:

```json
{
  "name": "Note",
  "description": "Save notable memories the user has shared with you for later recall.",
  "update_mode": "insert",
  "parameters": {
    "type": "object",
    "properties": {
      "context": {
        "type": "string",
        "description": "The situation or circumstance where this memory may be relevant. Include any caveats or conditions that contextualize the memory. For example, if a user shares a preference, note if it only applies in certain situations (e.g., 'only at work'). Add any other relevant 'meta' details that help fully understand when and how to use this memory."
      },
      "content": {
        "type": "string",
        "description": "The specific information, preference, or event being remembered."
      }
    },
    "required": ["context", "content"]
  }
}
```

Just like the previous example, this schema has a name, description, and parameters. Notic that the `update_mode` this time is "insert". This instructs the LLM in the memory service to **insert new memories to the list or update existing ones**. The number of memories for this `update_mode` is **unbound** since the model can continue to store new notes any time something interesting shows up in the conversation. Each time the service runs, the model can generate multiple schemas, some to update or re-contextualize existing memories, some to document new information. Note taht these memory schemas tend to have fewer parameters and are usually most effective if you have a field to let the service provide contextual information (so that if your bot fetches this memory, it isn't taken out-of-context).

To wrap up this section: `memory_schemas` provide a name, description, and parameters that the LLM populates to store in the database. The `update_mode` controls whether new information should always overwrite an existing memory or whether it should insert new memories (while optionally updating existing ones).

These schemas are fully customizable! Try extending the above and seeing how it updates memory formation in the studio by passing in via configuration (or defining in an assistant).

### Handling Memory Updates

In the previous section we showed how the memory schemas define how memories should be updated with new information over time. Let's now turn our attention to _how_ new information is handled. Each update type using tool calling in slightly different ways. We will use the [`trustcall` library](https://github.com/hinthornw/trustcall), which we created as a simple interface for generating and continuously updating json documents, to handle all of the cases below:

#### patch

If no memory has been saved yet, `trust_call` prompts the model to populate the document. It additionally does schema validation to ensure the output is correct.

If a memory already exists, you _could_ simply prompt the model to re-geerate the schema anew on each round. Doing so, however, leads to frequent information loss, especially on complicated schemas, since LLMs are wont to forget or omit previously stored details when regenerating information from scratch if it doesn't happen to be immediately relevant.

To avoid memory loss, your memory schema is placed in the system prompt but **not** made available as a tool for the model to call. Instead, the LLM is provided a `PatchDoc` tool. This forces the model to generate a chain-of-thought of 0 or more planned edits, along with patches to individual JSON paths to be modified.

Applying updates as JSON patches helps minimize information loss, save token costs, and simplifies the memory management task.

#### insert

If no memories have been saved yet, the model is given a single tool (the schema from your memory config). It is prompted to use multi-tool callint to generate 0 or more instances of your schema depending on the conversation context.

If memories exist for this user, the memory graph searches for existing ones to provide additional context. These are put in the system promt along with two two tools: your memory schema as well as a "PatchDoc" tool. The LLM is prompted to invoke whichever tools are appropriate given the conversational context. The LLM can call the PatchDoc tool to update existing memories in case they are no longer correct or require additional context. It can also call your memory schema tool any number of times to save new memories or notes. Either way, it calls these tools in a single generation step, and the graph upserts the results to the memory store.

![Memory Diagram](./static/memory_graph.png)

### Memory Scheduling

All of this sounds like a lot of tokens! If we were to process memories on every new message to your chat bot, the costs could indeed mount up. We only really need to process memories after a conversation ends, but in reality we typically don't know when the thread is finished.

As a compromise, our memory service supports **debouncing** by deferring when it will process memories. Memory updates are scheduled for some point in the future (using the LangGraph SDK's `after_seconds` parameter).

If the chatbot makes a call second time within that interval, the initial request is cancelled and a **new** request for memory processing is scheduled.

See this in the code here: [chatbot/graph.py](./src/chatbot/graph.py).

![DeBounce](./static/scheduling.png)

### Memory Storage

All these memories need to go somewhere reliable. All LangGraph deployments come with a built-in memory storage layer that you can use to persist information across conversations.

You can learn more about Storage in LangGraph [here](https://langchain-ai.github.io/langgraph/how-tos/memory/shared-state/).

In our case, we are saving all memories namespaced by `user_id` and by the memory scheam you provide. That way you can easily search for memories for a given user and of a particualr type. This diagram shows how these pieces fit together:

![Memory types](./static/memory_types.png)

### Calling the Memory Service

The studio uses the LangGraph API as its backend and exposes graph endpoints for all the graphs defied in your `langgraph.json` file.

```json
    "graphs": {
        "chatbot": "./src/chatbot/graph.py:graph",
        "memory_graph": "./src/memory_graph/graph.py:graph"
    },
```

You can interact with your server and storage using the studio UI or the LangGraph SDK.

```python
from langgraph_sdk import get_client
client = get_client(url="http:...") # your server
items = await client.store.search_items(namespace)
```

![Flow](./static/memory_template_flow.png)

## Benefits

The separation of concerns between the application logic (chatbot) and the memory (the memory graph) a few advantages:

(1) minimal overhead by removing memory creation logic from the hotpath of the application (e.g., no latency cost for memory creation)

(2) memory creation logic is handled in a background job, separate from the chatbot, with scheduling to avoid duplicate processing

(3) memory graph can be updated and / or hosted (as a service) independently of the application (chatbot)

Here is a schematic of the interaction pattern:

![Interaction Pattern](./static/memory_interactions.png)

## How to evaluate

Memory management can be challenging to get right. To make sure your memory_types suit your applications' needs, we recommend starting from an evaluation set, adding to it over time as you find and address common errors in your service.

We have provided a few example evaluation cases in [the test file here](./tests/integration_tests/test_graph.py). As you can see, the metrics themselves don't have to be terribly complicated, especially not at the outset.

We use [LangSmith's @unit decorator](https://docs.smith.langchain.com/how_to_guides/evaluation/unit_testing#write-a-test) to sync all the evaluations to LangSmith so you can better optimize your system and identify the root cause of any issues that may arise.

## How to customize

Customize memory memory_types: This memory graph supports two different `update_modes` that dictate how memories will be managed:

1. Patch Schema: This allows updating a single, continuous memory schema with new information from the conversation. You can customize the schema for this type by defining the JSON schema when initializing the memory schema. For example:

```json
{
  "name": "User",
  "description": "Update this document to maintain up-to-date information about the user in the conversation.",
  "update_mode": "patch",
  "parameters": {
    "type": "object",
    "properties": {
      "user_name": {
        "type": "string",
        "description": "The user's preferred name"
      },
      "age": {
        "type": "integer",
        "description": "The user's age"
      },
      "interests": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "A list of the user's interests"
      }
    }
  }
}
```

2. Insertion Schema: This allows inserting individual "event" memories, such as key pieces of information or summaries from the conversation. You can define custom memory_types for these event memories by providing a JSON schema when initializing the InsertionMemorySchema. For example:

```json
{
  "name": "Note",
  "description": "Save notable memories the user has shared with you for later recall.",
  "update_mode": "insert",
  "parameters": {
    "type": "object",
    "properties": {
      "context": {
        "type": "string",
        "description": "The situation or circumstance in which the memory occurred that inform when it would be useful to recall this."
      },
      "content": {
        "type": "string",
        "description": "The specific information, preference, or event being remembered."
      }
    },
    "required": ["context", "content"]
  }
}
```

3. Select a different model: We default to anthropic/claude-3-5-sonnet-20240620. You can select a compatible chat model using provider/model-name via configuration. Example: openai/gpt-4.
4. Customize the prompts: We provide default prompts in the graph definition. You can easily update these via configuration.

We'd also encourage you to extend this template by adding additional memory types! "Patch" and "insert" are incredibly powerful already, but you could also extend the logic to add more reflection over related memories to build stronger associations between the saved content. Make the code your own!

<!--
Configuration auto-generated by `langgraph template lock`. DO NOT EDIT MANUALLY.
{
  "config_schemas": {
    "chatbot": {
      "type": "object",
      "properties": {}
    },
    "memory_graph": {
      "type": "object",
      "properties": {
        "model": {
          "type": "string",
          "default": "anthropic/claude-3-5-sonnet-20240620",
          "description": "The name of the language model to use for the agent. Should be in the form: provider/model-name.",
          "environment": [
            {
              "value": "anthropic/claude-1.2",
              "variables": "ANTHROPIC_API_KEY"
            },
            {
              "value": "anthropic/claude-2.0",
              "variables": "ANTHROPIC_API_KEY"
            },
            {
              "value": "anthropic/claude-2.1",
              "variables": "ANTHROPIC_API_KEY"
            },
            {
              "value": "anthropic/claude-3-5-sonnet-20240620",
              "variables": "ANTHROPIC_API_KEY"
            },
            {
              "value": "anthropic/claude-3-haiku-20240307",
              "variables": "ANTHROPIC_API_KEY"
            },
            {
              "value": "anthropic/claude-3-opus-20240229",
              "variables": "ANTHROPIC_API_KEY"
            },
            {
              "value": "anthropic/claude-3-sonnet-20240229",
              "variables": "ANTHROPIC_API_KEY"
            },
            {
              "value": "anthropic/claude-instant-1.2",
              "variables": "ANTHROPIC_API_KEY"
            },
            {
              "value": "openai/gpt-3.5-turbo",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-3.5-turbo-0125",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-3.5-turbo-0301",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-3.5-turbo-0613",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-3.5-turbo-1106",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-3.5-turbo-16k",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-3.5-turbo-16k-0613",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4-0125-preview",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4-0314",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4-0613",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4-1106-preview",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4-32k",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4-32k-0314",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4-32k-0613",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4-turbo",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4-turbo-preview",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4-vision-preview",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4o",
              "variables": "OPENAI_API_KEY"
            },
            {
              "value": "openai/gpt-4o-mini",
              "variables": "OPENAI_API_KEY"
            }
          ]
        }
      }
    }
  }
}
-->
