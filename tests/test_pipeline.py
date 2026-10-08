from responder.pipeline import run_pipeline


# ---------------------------------------------------------
# Basic intent tests
# ---------------------------------------------------------

def test_conversation_ideas():
    result = run_pipeline("What can we talk about?")

    assert result["intent"] == "conversation_ideas"
    assert isinstance(result["response"], list)
    assert len(result["response"]) > 0


def test_help_me_understand():
    result = run_pipeline("Can you explain this to me?")

    assert result["intent"] == "help_me_understand"
    assert isinstance(result["response"], list)
    assert len(result["response"]) > 0


def test_next_steps():
    result = run_pipeline("What should we discuss next?")

    assert result["intent"] == "next_steps"
    assert isinstance(result["response"], list)
    assert len(result["response"]) > 0


def test_privacy_safety():
    result = run_pipeline("Is my information private?")

    assert result["intent"] == "privacy_safety"
    assert isinstance(result["response"], list)
    assert len(result["response"]) > 0


# ---------------------------------------------------------
# Quick-action priority
# ---------------------------------------------------------

def test_quick_action_priority():
    result = run_pipeline(
        "Can you explain this?",
        quick_action="conversation_ideas"
    )

    assert result["intent"] == "conversation_ideas"


# ---------------------------------------------------------
# Unknown requests
# ---------------------------------------------------------

def test_unknown_message():
    result = run_pipeline("Hello, I have a question.")

    assert result["intent"] is None
    assert isinstance(result["response"], list)
    assert len(result["response"]) > 0


# ---------------------------------------------------------
# LLM response validation
# ---------------------------------------------------------

def test_invalid_llm_response_fallback():
    from responder.llm_responder import validate_response

    invalid_response = {
        "intent": "invalid_intent",
        "response": ["Some response"]
    }

    assert validate_response(invalid_response) is False


def test_pipeline_uses_fallback_when_llm_response_is_invalid():

    class InvalidProvider:

        def generate(self, prompt):
            return {
                "intent": "invalid_intent",
                "response": ["Invalid response"]
            }

    from responder import pipeline

    original_get_provider = pipeline.get_provider

    pipeline.get_provider = lambda use_gemini=False: InvalidProvider()

    try:
        result = pipeline.run_pipeline(
            "What can we talk about?",
            use_gemini=True
        )

        assert result["intent"] == "conversation_ideas"
        assert isinstance(result["response"], list)

    finally:
        pipeline.get_provider = original_get_provider


def test_pipeline_fallback_when_provider_fails():

    class FailingProvider:

        def generate(self, prompt):
            raise RuntimeError("Simulated provider failure")

    from responder import pipeline

    original_get_provider = pipeline.get_provider

    pipeline.get_provider = lambda use_gemini=False: FailingProvider()

    try:
        result = pipeline.run_pipeline(
            "What can we talk about?",
            use_gemini=True
        )

        assert result["intent"] == "conversation_ideas"
        assert isinstance(result["response"], list)

    finally:
        pipeline.get_provider = original_get_provider


# ---------------------------------------------------------
# Additional evaluation cases
# ---------------------------------------------------------

def test_conversation_question_variant():
    result = run_pipeline(
        "What questions can we ask each other?"
    )

    assert result["intent"] == "conversation_ideas"


def test_privacy_question_variant():
    result = run_pipeline(
        "Who can see my information?"
    )

    assert result["intent"] == "privacy_safety"


def test_next_steps_variant():
    result = run_pipeline(
        "What are the next steps?"
    )

    assert result["intent"] == "next_steps"


def test_understanding_variant():
    result = run_pipeline(
        "I don't understand what this means."
    )

    assert result["intent"] == "help_me_understand"


# ---------------------------------------------------------
# Journey stage and retrieved context
# ---------------------------------------------------------

def test_journey_stage_and_context():

    result = run_pipeline(
        user_message="What can we talk about?",
        journey_stage="Connect",
        retrieved_context=(
            "Both users want to get to know each other better."
        )
    )

    assert result["intent"] == "conversation_ideas"
    assert isinstance(result["response"], list)