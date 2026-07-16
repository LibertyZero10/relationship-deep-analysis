# Contributing to Relationship Deep Analysis

First off, thank you for considering contributing! 🎉

This project aims to be a useful tool for anyone who wants to understand their intimate relationship patterns through data. Whether you're fixing a bug, adding a new framework, or improving patterns for another language, every contribution matters.

## Code of Conduct

Be respectful, constructive, and empathetic. This project deals with sensitive psychological topics. No harassment, gatekeeping, or dismissive behavior will be tolerated.

## Ways to Contribute

### 🐛 Bug Reports

1. Check [existing issues](../../issues) to avoid duplicates
2. Open a new issue with:
   - **Bug description**: What happened vs. what you expected
   - **Reproduction steps**: Minimal input data that triggers the bug
   - **Environment**: Python version, OS, message count
   - **Error output**: Full traceback if available

### ✨ Feature Requests

Ideas welcome for:
- New psychological frameworks (see [Framework Criteria](#framework-criteria))
- Additional language pattern sets (English, Japanese, Korean, etc.)
- New analysis metrics or visualizations
- Integration with more chat export formats
- Performance improvements

### 🔀 Pull Requests

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test with real chat data
5. Submit a PR with a clear description

## Framework Criteria

A new psychological framework should:

1. **Have academic grounding** - Published research, established theorist, or clinical framework
2. **Be detectable from text** - Observable through chat message patterns (words, timing, response behavior)
3. **Add unique diagnostic value** - Not heavily overlap with existing 24 frameworks
4. **Include threshold criteria** - Define what scores indicate healthy vs. concerning patterns

## Adding Language Patterns

The current regex patterns are optimized for Chinese. To add support for another language:

1. Create a pattern file in `references/patterns_<language>.md`
2. Translate each framework's patterns while preserving the structure:
   ```python
   # Example: English NVC patterns
   eval_judg = [r'you always', r'you never', r'you\'re so', r'you\'re such a']
   contempt = [r'whatever', r'as if', r'pathetic', r'you\'re ridiculous']
   ```
3. Test against real chat data in that language
4. Submit a PR with test results

## Pattern Quality Guidelines

When contributing regex patterns:

- **Prioritize precision over recall** - Better to miss some matches than produce false positives
- **Consider context** - "呵呵" can be contempt or genuine laughter depending on context. Document ambiguous cases.
- **Test edge cases** - Short messages ("嗯", "哦"), emoji-only messages, voice/image markers
- **Document cultural nuances** - Chinese "哈哈" vs English "haha" have different connotations

## Development Setup

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/relationship-deep-analysis.git
cd relationship-deep-analysis

# No virtual environment needed - zero dependencies!
# Just run:
python scripts/run_analysis.py test_data.json

# For development, you can add --quiet to suppress console output
python scripts/run_analysis.py test_data.json --quiet --output dev_test.json
```

## Code Style

- **Python**: PEP 8, type hints encouraged, docstrings for all public functions
- **No external dependencies**: Only Python standard library
- **Single-pass design**: All 24 frameworks should be processed in one message iteration
- **File size**: `run_analysis.py` should stay under 1000 lines. If larger, refactor.

## Testing

Before submitting a PR:

1. **Smoke test**: Run against a small dataset (100+ messages)
2. **Scale test**: Run against a large dataset (10K+ messages) to verify performance
3. **Output validation**: Check that all 24 framework keys exist in the output JSON
4. **Edge cases**: Test with:
   - Very short conversations (<100 messages)
   - One-sided conversations (one person sends 95%+ of messages)
   - Messages with no text content (images, stickers, voice)
   - Non-standard timestamps

## Questions?

Open an issue with the `question` label. We're happy to help.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
