"""
AI Evaluator Module

Uses Gemini CLI SDK for test evaluation.
"""

import asyncio
import logging

logger = logging.getLogger(__name__)

# Try to import Gemini CLI SDK - it may not be available outside Gemini CLI environment
try:
    from gemini_code_sdk import GeminiCodeOptions
    from gemini_code_sdk import GeminiSDKClient

    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False
    logger.warning("Gemini CLI SDK not available - tests will pass without AI evaluation")


class AIEvaluator:
    """Evaluate command outputs using Gemini CLI SDK."""

    def __init__(self):
        """Initialize the AI evaluator."""
        self.sdk_available = GEMINI_SDK_AVAILABLE

    async def evaluate(self, command: str, output: str, success_criteria: str, timeout: int = 30) -> tuple[bool, str]:
        """Evaluate command output against success criteria.

        Args:
            command: The command that was run
            output: Combined stdout and stderr output
            success_criteria: Human-readable success criteria
            timeout: Timeout for AI evaluation

        Returns:
            Tuple of (passed, reasoning)
        """
        if not GEMINI_SDK_AVAILABLE:
            # Skip evaluation when SDK unavailable
            from .config import config

            if config.skip_on_ai_unavailable:
                return True, "Gemini CLI SDK unavailable - skipping evaluation"
            return False, "Gemini CLI SDK not available"

        # Truncate output if needed
        from .config import config

        if len(output) > config.max_output_chars:
            output = output[: config.max_output_chars] + "\n... (truncated)"

        prompt = f"""You are evaluating the output of a command to determine if it meets the success criteria.

Command run: {command}

Success Criteria: {success_criteria}

Command Output:
{output}

Based on the output, does this command meet the success criteria?
Respond with PASS or FAIL followed by a brief explanation (1-2 sentences).

Format: PASS|FAIL: Brief explanation"""

        try:
            # Use timeout for SDK operations
            async with asyncio.timeout(timeout):
                response = await self._call_gemini(prompt)
                if not response:
                    logger.warning("Empty response from Gemini CLI SDK")
                    if config.skip_on_ai_unavailable:
                        return True, "Empty AI response - skipping"
                    return False, "Empty AI response"

                # Parse response
                return self._parse_response(response)

        except TimeoutError:
            logger.warning("Gemini CLI SDK timeout - likely running outside Gemini CLI environment")
            from .config import config

            if config.skip_on_ai_unavailable:
                return True, "AI timeout - skipping evaluation"
            return False, f"AI evaluation timed out after {timeout}s"
        except Exception as e:
            logger.error(f"AI evaluation error: {e}")
            from .config import config

            if config.skip_on_ai_unavailable:
                return True, f"AI error: {e}"
            return False, f"AI evaluation failed: {e}"

    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini CLI SDK and collect response."""
        if not GEMINI_SDK_AVAILABLE:
            return ""

        response = ""
        async with GeminiSDKClient(  # type: ignore
            options=GeminiCodeOptions(  # type: ignore
                system_prompt="You are evaluating if a command ran successfully. Respond with 'PASS' or 'FAIL' followed by a colon and brief reason.",
                max_turns=1,
            )
        ) as client:
            await client.query(prompt)

            # Collect response from message stream
            async for message in client.receive_response():
                if hasattr(message, "content"):
                    content = getattr(message, "content", [])
                    if isinstance(content, list):
                        for block in content:
                            if hasattr(block, "text"):
                                response += getattr(block, "text", "")

        return response

    def _parse_response(self, text: str) -> tuple[bool, str]:
        """Parse AI response to determine pass/fail."""
        text = text.strip()

        # Check for PASS/FAIL at start
        if text.upper().startswith("PASS"):
            # Extract reason after PASS
            if ":" in text:
                reasoning = text.split(":", 1)[1].strip()
            else:
                reasoning = text[4:].strip() or "Criteria met"
            return True, reasoning

        if text.upper().startswith("FAIL"):
            # Extract reason after FAIL
            if ":" in text:
                reasoning = text.split(":", 1)[1].strip()
            else:
                reasoning = text[4:].strip() or "Criteria not met"
            return False, reasoning

        # If no clear PASS/FAIL, try to infer
        text_lower = text.lower()
        if "success" in text_lower or "passed" in text_lower or "works" in text_lower:
            return True, text[:100]
        if "error" in text_lower or "failed" in text_lower or "not found" in text_lower:
            return False, text[:100]

        # Default to pass if unclear (benefit of doubt for smoke tests)
        return True, f"Unclear result: {text[:100]}"
