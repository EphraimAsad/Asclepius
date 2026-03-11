"""
Tests for LLM providers and cache.
"""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.llm import (
    EnhancementContext,
    EnhancedResult,
    LLMCache,
    get_cache,
    reset_cache,
)
from app.llm.providers import OllamaProvider
from app.llm.factory import get_llm_provider
from app.llm.prompts import format_enhancement_prompt, format_followup_prompt


# Test fixtures
@pytest.fixture
def sample_context():
    """Create a sample enhancement context."""
    return EnhancementContext(
        explanation="You should seek emergency care immediately.",
        disposition="ER_NOW",
        matched_rules=["cp_high_acuity", "chest_pressure_rule"],
        chief_complaint="chest_pain",
        symptoms={
            "chest_pressure": True,
            "shortness_of_breath": True,
            "radiating_pain": False,
        },
        patient_age=55,
        patient_sex="male",
        reason_codes=["POSSIBLE_ACS"],
    )


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    settings = MagicMock()
    settings.llm_enabled = True
    settings.llm_provider = "ollama"
    settings.llm_model = "qwen3.5:4b"
    settings.llm_base_url = "http://127.0.0.1:11434"
    settings.llm_api_key = None
    settings.llm_timeout_seconds = 20.0
    settings.llm_cache_ttl_seconds = 3600
    return settings


@pytest.fixture(autouse=True)
def reset_cache_fixture():
    """Reset the global cache before each test."""
    reset_cache()
    yield
    reset_cache()


# Cache tests
class TestLLMCache:
    """Tests for the LLM cache."""

    def test_make_key_consistent(self, sample_context):
        """Test that make_key produces consistent keys."""
        cache = LLMCache()

        key1 = cache.make_key(
            sample_context.matched_rules,
            sample_context.chief_complaint,
            sample_context.symptoms,
        )
        key2 = cache.make_key(
            sample_context.matched_rules,
            sample_context.chief_complaint,
            sample_context.symptoms,
        )

        assert key1 == key2

    def test_make_key_different_for_different_input(self, sample_context):
        """Test that different inputs produce different keys."""
        cache = LLMCache()

        key1 = cache.make_key(
            sample_context.matched_rules,
            sample_context.chief_complaint,
            sample_context.symptoms,
        )
        key2 = cache.make_key(
            ["different_rule"],
            sample_context.chief_complaint,
            sample_context.symptoms,
        )

        assert key1 != key2

    def test_cache_set_and_get(self):
        """Test basic cache set and get."""
        cache = LLMCache()
        result = EnhancedResult(
            enhanced_explanation="Enhanced text",
            follow_up_questions=["Question 1?", "Question 2?"],
        )

        cache.set("test_key", result)
        cached = cache.get("test_key")

        assert cached is not None
        assert cached.enhanced_explanation == "Enhanced text"
        assert cached.follow_up_questions == ["Question 1?", "Question 2?"]
        assert cached.from_cache is True

    def test_cache_miss(self):
        """Test cache miss returns None."""
        cache = LLMCache()
        cached = cache.get("nonexistent_key")
        assert cached is None

    def test_cache_lru_eviction(self):
        """Test LRU eviction when cache is full."""
        cache = LLMCache(max_size=3)

        for i in range(5):
            result = EnhancedResult(enhanced_explanation=f"Text {i}")
            cache.set(f"key_{i}", result)

        # First two should be evicted
        assert cache.get("key_0") is None
        assert cache.get("key_1") is None
        # Last three should exist
        assert cache.get("key_2") is not None
        assert cache.get("key_3") is not None
        assert cache.get("key_4") is not None

    def test_cache_stats(self):
        """Test cache statistics."""
        cache = LLMCache()
        result = EnhancedResult(enhanced_explanation="Test")

        cache.set("key1", result)
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss

        stats = cache.stats()
        assert stats["size"] == 1
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["hit_rate"] == 0.5

    def test_cache_clear(self):
        """Test cache clear."""
        cache = LLMCache()
        result = EnhancedResult(enhanced_explanation="Test")

        cache.set("key1", result)
        cache.clear()

        assert cache.get("key1") is None
        stats = cache.stats()
        assert stats["size"] == 0


# Prompt formatting tests
class TestPromptFormatting:
    """Tests for prompt formatting functions."""

    def test_format_enhancement_prompt(self):
        """Test enhancement prompt formatting.

        Optimized prompts are simpler - only include explanation text.
        Context fields kept for backwards compatibility but not used.
        """
        prompt = format_enhancement_prompt(
            explanation="Original text",
            disposition="ER_NOW",
            chief_complaint="chest_pain",
            symptoms={"chest_pressure": True, "nausea": True, "headache": False},
        )

        assert "Original text" in prompt
        assert "EXAMPLE" in prompt  # Few-shot example included
        assert "rewritten text" in prompt.lower()

    def test_format_followup_prompt(self):
        """Test follow-up questions prompt formatting.

        Optimized prompts include chief_complaint and symptoms.
        Disposition kept for backwards compatibility but not used.
        """
        prompt = format_followup_prompt(
            chief_complaint="headache",
            symptoms={"severe_pain": True, "vision_changes": True},
            disposition="URGENT_CARE_TODAY",
        )

        assert "headache" in prompt
        assert "severe pain" in prompt
        assert "vision changes" in prompt
        assert "json array" in prompt.lower()
        assert "EXAMPLE" in prompt  # Few-shot example included


# Ollama provider tests
class TestOllamaProvider:
    """Tests for the Ollama provider."""

    @pytest.mark.asyncio
    async def test_enhance_returns_result(self, mock_settings, sample_context):
        """Test that enhance returns an EnhancedResult."""
        provider = OllamaProvider(mock_settings)

        # Mock the HTTP calls
        with patch.object(provider, "_call_ollama") as mock_call:
            mock_call.side_effect = [
                "Enhanced explanation text.",
                '["When did symptoms start?", "Any medications?"]',
            ]

            result = await provider.enhance(sample_context)

            assert isinstance(result, EnhancedResult)
            assert result.enhanced_explanation == "Enhanced explanation text."
            assert len(result.follow_up_questions) == 2

    @pytest.mark.asyncio
    async def test_enhance_uses_cache(self, mock_settings, sample_context):
        """Test that enhance uses cache on second call."""
        provider = OllamaProvider(mock_settings)

        with patch.object(provider, "_call_ollama") as mock_call:
            mock_call.side_effect = [
                "Enhanced text.",
                '["Question?"]',
            ]

            # First call - should hit LLM
            result1 = await provider.enhance(sample_context)
            assert result1.from_cache is False

            # Second call - should hit cache
            result2 = await provider.enhance(sample_context)
            assert result2.from_cache is True

            # LLM should only be called twice (once for each prompt on first call)
            assert mock_call.call_count == 2

    @pytest.mark.asyncio
    async def test_enhance_handles_timeout(self, mock_settings, sample_context):
        """Test graceful fallback on timeout."""
        provider = OllamaProvider(mock_settings)

        with patch.object(provider, "_call_ollama") as mock_call:
            mock_call.return_value = None  # Simulates timeout

            result = await provider.enhance(sample_context)

            # Should return original explanation
            assert result.enhanced_explanation == sample_context.explanation
            assert result.follow_up_questions == []

    @pytest.mark.asyncio
    async def test_health_check_success(self, mock_settings):
        """Test health check when Ollama is running."""
        provider = OllamaProvider(mock_settings)

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "models": [{"name": "qwen3.5:4b"}]
            }

            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            is_healthy = await provider.health_check()
            assert is_healthy is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self, mock_settings):
        """Test health check when Ollama is not running."""
        provider = OllamaProvider(mock_settings)

        with patch("httpx.AsyncClient") as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(side_effect=Exception("Connection refused"))
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            is_healthy = await provider.health_check()
            assert is_healthy is False

    def test_parse_questions_json_valid(self, mock_settings):
        """Test parsing valid JSON array."""
        provider = OllamaProvider(mock_settings)

        questions = provider._parse_questions_json(
            '["Question 1?", "Question 2?"]'
        )

        assert questions == ["Question 1?", "Question 2?"]

    def test_parse_questions_json_with_markdown(self, mock_settings):
        """Test parsing JSON wrapped in markdown code block."""
        provider = OllamaProvider(mock_settings)

        questions = provider._parse_questions_json(
            '```json\n["Question 1?", "Question 2?"]\n```'
        )

        assert questions == ["Question 1?", "Question 2?"]

    def test_parse_questions_json_embedded(self, mock_settings):
        """Test parsing JSON embedded in text."""
        provider = OllamaProvider(mock_settings)

        questions = provider._parse_questions_json(
            'Here are the questions: ["Q1?", "Q2?"] as requested.'
        )

        assert questions == ["Q1?", "Q2?"]

    def test_parse_questions_json_invalid(self, mock_settings):
        """Test handling invalid JSON."""
        provider = OllamaProvider(mock_settings)

        questions = provider._parse_questions_json("not valid json at all")

        assert questions == []


# Factory tests
class TestLLMFactory:
    """Tests for the LLM provider factory."""

    def test_factory_returns_ollama(self, mock_settings):
        """Test factory returns Ollama provider."""
        mock_settings.llm_provider = "ollama"
        provider = get_llm_provider(mock_settings)

        assert provider is not None
        assert provider.provider_name == "ollama"

    def test_factory_returns_openai(self, mock_settings):
        """Test factory returns OpenAI provider."""
        mock_settings.llm_provider = "openai"
        mock_settings.llm_api_key = "test-key"
        provider = get_llm_provider(mock_settings)

        assert provider is not None
        assert provider.provider_name == "openai"

    def test_factory_returns_anthropic(self, mock_settings):
        """Test factory returns Anthropic provider."""
        mock_settings.llm_provider = "anthropic"
        mock_settings.llm_api_key = "test-key"
        provider = get_llm_provider(mock_settings)

        assert provider is not None
        assert provider.provider_name == "anthropic"

    def test_factory_returns_none_when_disabled(self, mock_settings):
        """Test factory returns None when LLM is disabled."""
        mock_settings.llm_enabled = False
        provider = get_llm_provider(mock_settings)

        assert provider is None

    def test_factory_returns_none_for_unknown_provider(self, mock_settings):
        """Test factory returns None for unknown provider."""
        mock_settings.llm_provider = "unknown_provider"
        provider = get_llm_provider(mock_settings)

        assert provider is None


# Integration test (requires Ollama running locally)
@pytest.mark.skip(reason="Requires Ollama running locally")
class TestOllamaIntegration:
    """Integration tests with actual Ollama instance."""

    @pytest.mark.asyncio
    async def test_real_ollama_enhancement(self, mock_settings, sample_context):
        """Test actual enhancement with Ollama."""
        provider = OllamaProvider(mock_settings)

        # Check if Ollama is available
        is_healthy = await provider.health_check()
        if not is_healthy:
            pytest.skip("Ollama not available")

        result = await provider.enhance(sample_context)

        assert result.enhanced_explanation != ""
        # The enhanced explanation might be different from original
        # but should still convey the same urgency
        assert len(result.follow_up_questions) >= 0
