# Contributing to cipherself

We welcome contributions to help improve the digital footprint intelligence engine! Whether you want to add new inference rules, support new data sources, or improve the report aesthetic, here’s how you can help.

## Adding New Inference Rules

Inference rules are located in `src/cipherself/analyzer/personality.py` within the `infer` method. 

To add a new rule:
1. Define the data point you want to analyze (e.g., repository names, bio keywords, or commit frequency).
2. Create a specific heuristic (e.g., "If subject uses 'automated' in 5+ repo descriptions, infer interest in DevOps").
3. Add your logic to the `inferences` list.

```python
# Example rule
if "DevOps" in profile.get('bio', ''):
    inferences.append("Subject explicitly identifies with DevOps methodologies.")
```

## Adding New Data Sources

Data collection logic is handled in `src/cipherself/collector/`.

1. **GitHub Data**: Add new methods to the `GitHubCollector` class to fetch additional endpoints (e.g., Organizations, Gists).
2. **Search Sources**: If you want to add a new search engine or public record site, implement a new method in `SearchCollector` or create a new collector class.

## Style & Aesthetics

Report styling is managed via `reportlab` in `src/cipherself/generator/pdf.py`. If you're improving the "declassified" look, please maintain the monospace font and high-contrast header theme.

## Pull Request Process

1. Fork the repository.
2. Create a feature branch.
3. Ensure your changes don't break the main CLI flow.
4. Submit a PR with a clear description of your changes.

---

Thank you for helping build the OSINT tool for the modern web!
