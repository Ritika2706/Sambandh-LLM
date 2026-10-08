# Sambandh Setu — AI/ML Intent Router & LLM Responder

## Overview

This project implements the AI/ML module for the Sambandh Setu Guide.

The module is responsible for:

* Detecting user intent
* Prioritizing selected quick actions
* Selecting intent-specific prompts
* Incorporating journey-stage information
* Incorporating retrieved context
* Calling an LLM through a provider-agnostic interface
* Validating LLM responses
* Providing a safe template fallback when the LLM is unavailable or returns invalid output

---

## Supported Intents

The system supports four Setu Guide intents:

```text
conversation_ideas
help_me_understand
next_steps
privacy_safety
```

### Conversation Ideas

Provides neutral suggestions for topics or questions that users can discuss.

### Help Me Understand

Helps break down a topic or situation into simpler points.

### Next Steps

Provides neutral discussion-oriented suggestions for what users can consider discussing next.

### Privacy and Safety

Provides privacy- and safety-aware guidance without inventing privacy guarantees or requesting unnecessary sensitive information.

---

## System Flow

```text
User Message
     |
     v
Intent Router
     |
     +---- Quick Action selected?
     |          |
     |          +---- Yes --> Use selected intent
     |          |
     |          +---- No --> Classify free text
     |
     v
Intent-specific Prompt
     |
     +---- Journey Stage
     |
     +---- User Message
     |
     +---- Retrieved Context
     |
     v
LLM Provider
     |
     v
JSON Validation
     |
     +---- Valid --> Return response
     |
     +---- Invalid / Failure
                  |
                  v
            Template Fallback
```

---

## Project Structure

```text
Sambandh-LLM/
│
├── intents/
│   └── intent_router.md
│
├── prompts/
│   ├── conversation_ideas.txt
│   ├── help_me_understand.txt
│   ├── next_steps.txt
│   └── privacy_safety.txt
│
├── responder/
│   ├── llm_provider.py
│   ├── llm_responder.py
│   └── pipeline.py
│
├── tests/
│   ├── intent_test_cases.md
│   └── test_pipeline.py
│
├── backend_integration.md
├── intent_router.py
└── README.md
```

---

## Intent Router

The intent router is implemented in:

```text
intent_router.py
```

Routing follows two priorities:

1. A valid selected quick action takes priority.
2. If no quick action is selected, the user's free-text message is classified.

If no intent can be confidently identified, the router returns:

```text
None
```

---

## Prompt Engineering

Intent-specific prompts are stored in:

```text
prompts/
```

Each prompt can receive:

* User message
* Journey stage
* Retrieved context

The prompts are designed to remain:

* Neutral
* Non-judgmental
* Respectful
* Supportive

The system does not make relationship decisions for users or pressure them toward a particular outcome.

---

## LLM Provider

The provider abstraction is implemented in:

```text
responder/llm_provider.py
```

The architecture supports:

```text
LLMProvider
    |
    +---- MockLLMProvider
    |
    +---- GeminiLLMProvider
```

The mock provider is useful for development and automated testing without making external API calls.

The Gemini provider uses the Google GenAI SDK.

API credentials are read from the environment variable:

```text
GEMINI_API_KEY
```

The API key should never be committed to source control.

---

## LLM Response Validation

The expected response structure is:

```json
{
    "intent": "conversation_ideas",
    "response": [
        "Example response 1",
        "Example response 2",
        "Example response 3"
    ]
}
```

The response validator checks:

* Response is a dictionary
* `intent` exists
* `response` exists
* Intent is supported
* Response is a list
* Response contains strings
* Response is not empty

---

## Fallback Handling

If the LLM:

* fails,
* is unavailable,
* returns invalid JSON,
* returns an unsupported intent,
* or returns an invalid response structure,

the system uses a predefined template response.

This ensures that the pipeline can still return a valid response without depending entirely on the external LLM.

---

## Pipeline

The main processing pipeline is implemented in:

```text
responder/pipeline.py
```

The internal integration function is:

```python
handle_request(request, use_gemini=False)
```

A request can contain:

```json
{
    "message": "What can we talk about?",
    "quick_action": null,
    "journey_stage": "Connect",
    "retrieved_context": "Both users want to get to know each other better."
}
```

---

## Testing

Automated tests are located in:

```text
tests/test_pipeline.py
```

The current test suite covers:

* Basic intent routing
* Intent variations
* Quick-action priority
* Unknown messages
* Invalid LLM responses
* Provider failures
* Template fallback
* Journey-stage input
* Retrieved-context input

Current result:

```text
14 passed
```

Run the tests with:

```powershell
python -m pytest tests/test_pipeline.py -v
```

---

## Backend Integration

The expected backend endpoint from the assignment is:

```text
POST /v1/guide/chat
```

The current AI/ML module exposes an internal `handle_request()` interface for integration.

The final API request/response contract should be aligned with the backend team's agreed schema before production integration.

See:

```text
backend_integration.md
```

for the current integration notes.

---

## Safety Principles

The system is designed to:

* Remain neutral and non-judgmental
* Encourage respectful communication
* Avoid making relationship decisions
* Avoid pressuring users toward a particular outcome
* Avoid unnecessary collection of sensitive information
* Avoid inventing privacy guarantees
* Provide a safe fallback when the LLM cannot respond reliably

---

## Current Status

### Completed

* Intent Router
* Four supported intents
* Quick-action priority
* Intent-specific prompts
* Journey-stage support
* Retrieved-context support
* Provider abstraction
* Gemini provider integration
* JSON response validation
* Template fallback
* Automated evaluation tests
* Backend integration documentation

### Pending Team Integration

* Final backend API schema
* RAG/retrieved-context format
* Synthetic evaluation conversations
* Final conversational UX expectations
* Backend endpoint integration

These items depend on the respective team members and the finalized backend contract.
