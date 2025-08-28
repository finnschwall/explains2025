from . import prompt_types_rational, prompt_types_emotional

prompts = {
    "ai_trust_emotional": prompt_types_emotional.ai_trust_emotional,
    "ai_distrust_emotional": prompt_types_emotional.ai_distrust_emotional,
    "ai_neutral_emotional": prompt_types_emotional.ai_neutral_emotional,
    "ai_trust_rational": prompt_types_rational.ai_trust_rational,
    "ai_distrust_rational": prompt_types_rational.ai_distrust_rational,
    "ai_neutral_rational": prompt_types_rational.ai_neutral_rational,
}