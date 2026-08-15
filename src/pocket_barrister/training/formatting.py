"""Stable prompt/target rendering shared by training and evaluation."""

from __future__ import annotations

EOS_MARKER = "<|end_of_text|>"
SYSTEM_INSTRUCTION = (
    "Analyze the synthetic Indian contract-law hypothetical. Return exactly these "
    "sections in order: REASONING, FINDINGS, LEGAL_EFFECT, CONCLUSION, and "
    "WHY ALTERNATIVES FAIL. End with <|end_of_text|>."
)


def format_prompt(case_text: str) -> str:
    """Render the prompt identically for base and adapter comparisons."""
    return (
        "### INSTRUCTION\n"
        f"{SYSTEM_INSTRUCTION}\n\n"
        "### CASE\n"
        f"{case_text.strip()}\n\n"
        "### RESPONSE\n"
    )


def format_target(output: str, tokenizer_eos_token: str = "") -> str:
    """Normalize the visible marker and append the model's real EOS token."""
    visible = output.strip()
    if not visible.endswith(EOS_MARKER):
        raise ValueError(f"target must end with {EOS_MARKER}")
    return visible + tokenizer_eos_token
