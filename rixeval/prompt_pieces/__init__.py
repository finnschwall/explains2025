from . import direct_answers, cot, bias, prompt_types_rational, prompt_types_emotional

prompts = {
    "ai_trust_emotional": prompt_types_emotional.ai_trust_emotional,
    "ai_distrust_emotional": prompt_types_emotional.ai_distrust_emotional,
    "ai_neutral_emotional": prompt_types_emotional.ai_neutral_emotional,
    "ai_trust_rational": prompt_types_rational.ai_trust_rational,
    "ai_distrust_rational": prompt_types_rational.ai_distrust_rational,
    "ai_neutral_rational": prompt_types_rational.ai_neutral_rational,
}

# "direct_answers": direct_answers.direct_answers,
# "cot": cot.cot,
# "bias_avoid_fn": bias.avoid_fn,
# "bias_avoid_fp": bias.avoid_fp,