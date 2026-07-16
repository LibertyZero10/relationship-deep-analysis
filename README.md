# Relationship Deep Analysis

> A Python-based toolkit for deep psychological analysis of intimate relationship chat data using 24 evidence-based psychological frameworks across 6 dimensions.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-green.svg)](#)

## What It Does

This tool analyzes chat records (WeChat, WhatsApp, Telegram, or any JSON export with sender/content/timestamp fields) between two people in an intimate relationship and produces a comprehensive psychological profile across **24 frameworks** in **6 dimensions**:

| Dimension | Frameworks | Key Questions Answered |
|-----------|-----------|----------------------|
| **A. Communication Patterns** | Gottman's Four Horsemen, NVC, Transactional Analysis (PAC), Drama Triangle | How do they talk to each other? Is it toxic? |
| **B. Psychological Structure** | Schema Therapy, Defense Mechanisms, Inner Child, Johari Window | What unconscious patterns drive their behavior? |
| **C. Relationship Dynamics** | Relational Dialectics, Social Exchange, Power Bases, Attachment Model, Trust Formula | What's the power balance? Are they securely attached? |
| **D. Emotions & Needs** | Self-Determination Theory, Emotion Regulation, Maslow's Hierarchy, Enneagram | What needs are met/unmet? How do they handle emotions? |
| **E. Dark Side & Pathology** | Gaslighting Detection, Trauma Bond Assessment, Silent Treatment, Codependency | Is there emotional abuse? Is the bond healthy or traumatic? |
| **F. Behavioral Patterns** | Habit Loops, BIS/BAS, Gottman Sound Relationship House | What recurring cycles trap them? How resilient is the relationship? |

## Key Features

- **One-command analysis**: Single script processes 100K+ messages in ~30 seconds
- **Zero dependencies**: Pure Python standard library (json, re, sys, os, argparse, math, statistics, collections)
- **Normalized metrics**: All frequency indicators include per-1k-messages normalization for fair comparison
- **Monthly trend tracking**: Time-series analysis shows whether patterns are improving or deteriorating
- **Emotional burst detection**: Identifies sequences of ≥5 consecutive negative-emotion messages
- **Cross-framework correlation matrix**: Discovers hidden connections between psychological dimensions
- **Report template**: Jinja2-style template for generating structured analysis reports

## Quick Start

```bash
# Analyze a chat export
python scripts/run_analysis.py chat_data.json

# With options
python scripts/run_analysis.py chat_data.json \
  --output results.json \
  --sender-a "your_id" \
  --sender-b "partner_id" \
  --quiet
```

### Input Format

JSON file with an array of message objects:

```json
[
  {
    "sender": "alice",
    "content": "I miss you",
    "timestamp": "2023-06-15T10:30:00",
    "type": "text"
  },
  {
    "sender": "bob",
    "content": "Miss you too",
    "timestamp": "2023-06-15T10:31:00",
    "type": "text"
  }
]
```

| Field | Required | Description |
|-------|----------|-------------|
| `sender` | ✅ | Identifier for who sent the message |
| `content` | ✅ | Message text content |
| `timestamp` | ✅ | ISO 8601 or `YYYY-MM-DD HH:MM:SS` format |
| `type` | ❌ | Message type: text, call, voice, image, transfer, etc. |

### Output

A JSON file containing:

```json
{
  "meta": { "total_messages": 50000, "total_days": 365, ... },
  "frameworks": { "A1": {...}, "A2": {...}, ..., "F24": {...} },
  "monthly_trends": { "2023-01": {...}, "2023-02": {...}, ... },
  "normalized": { "A1": { "contempt": { "a_per_1k": 1.5, ... } } },
  "emotional_bursts": { "a_count": 2, "b_count": 1, "top_5_bursts": [...] },
  "additional_metrics": { "response_time": {...}, "conversations": {...}, ... },
  "correlations": { "strong_pairs": [...] }
}
```

## Generating a Report

1. Run the analysis script to produce a JSON results file
2. Use `templates/report_template.md` as the report skeleton
3. Fill in the Jinja2-style placeholders (`{{ A1.contempt.a }}`, etc.) with values from the JSON
4. Add qualitative interpretations for each framework based on the data

## Project Structure

```
relationship-deep-analysis/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                   # Contribution guidelines
├── CHANGELOG.md                       # Version history
├── .gitignore                         # Python gitignore
├── SKILL.md                          # Full framework theory + execution guide
├── scripts/
│   └── run_analysis.py               # Core analysis script (760 lines, zero deps)
├── templates/
│   └── report_template.md            # Report template with Jinja2 placeholders
└── references/
    └── verified-patterns.md          # Regex pattern library + formula tables
```

## Supported Chat Platforms

Any JSON export with `sender`/`content`/`timestamp` fields works. Tested with:

- **WeChat** (via wechat-decrypt tools, WeChatFerry, wxauto exports)
- **WhatsApp** (via WhatsApp Chat Export)
- **Telegram** (via Telegram Desktop export)

The regex patterns are optimized for **Chinese-language** chat data. For other languages, see [Contributing](#contributing) to add pattern sets.

## Key Metrics & Thresholds

| Metric | Formula | Healthy | Warning | Danger |
|--------|---------|---------|---------|--------|
| Gottman Ratio | Positive/Negative interactions | >5:1 | 0.8-5:1 | <0.8:1 |
| Contempt/Criticism Ratio | Contempt count / Criticism count | <0.5 | 0.5-1.0 | >1.0 |
| NVC Maturity | Non-violent / Total × 10 | >7 | 5-7 | <5 |
| Cross-transaction Rate | Cross / (Cross + Complementary) × 100% | <15% | 15-30% | >30% |
| Trust Score | (Predictability + Dependability + Faith) / 3 | >7 | 4-7 | <4 |
| Emotional Suppression Rate | Suppression / Total strategies × 100% | <40% | 40-60% | >60% |
| Trauma Bond Score | (Intermittent + Polarization + Cycle + Power) / 4 | <4 | 4-6 | >6 |
| Punitive Silence Rate | Punitive / (Punitive + Protective) × 100% | <50% | 50-80% | >80% |
| Relationship Resilience | 7-layer average score | >7 | 5-7 | <5 |

## Ethical Notice

This tool performs **behavioral pattern analysis based on chat data**, not clinical diagnosis. All outputs should be interpreted as data-driven observations, not medical or therapeutic advice. If you or someone you know is in an abusive relationship, please seek professional help.

- **National Domestic Violence Hotline** (US): 1-800-799-7233
- **Women's Aid** (UK): 0808 2000 247
- **全国妇女维权热线** (China): 12338

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions welcome for:

- Additional language pattern sets (English, Japanese, Korean, etc.)
- New psychological frameworks
- Improved regex patterns
- Report template improvements
- Bug reports and feature requests

## License

[MIT License](LICENSE) - free for personal and commercial use.

## Acknowledgments

This tool is based on the work of many psychologists and researchers:

- **John Gottman** - Four Horsemen, Sound Relationship House, Trust Formula
- **Marshall Rosenberg** - Nonviolent Communication (NVC)
- **Eric Berne** - Transactional Analysis (PAC Model)
- **Stephen Karpman** - Drama Triangle
- **Jeffrey Young** - Schema Therapy
- **Anna Freud / George Vaillant** - Defense Mechanisms
- **Leslie Baxter** - Relational Dialectics Theory
- **Thibaut & Kelley** - Social Exchange Theory
- **French & Raven** - Five Bases of Power
- **Bartholomew & Horowitz** - Attachment Model
- **Edward Deci & Richard Ryan** - Self-Determination Theory
- **James Gross** - Emotion Regulation
- **Abraham Maslow** - Hierarchy of Needs
- **Robin Stern** - Gaslighting Detection
- **Patrick Carnes** - Trauma Bonding
- **Pia Mellody** - Codependency
- **Charles Duhigg** - Habit Loops
- **Jeffrey Gray** - BIS/BAS
