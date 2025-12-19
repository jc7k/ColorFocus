# ColorFocus

A color-based cognitive training application featuring Stroop test puzzles with accessibility-first design.

**Live Demo:** [colorfocus.vercel.app](https://colorfocus.vercel.app)

## Why I Built This

My mother suffered a minor stroke recently and occasionally exhibited difficulty verbalizing her thoughts—even though she could think of the words and sentences, she couldn't deliver them correctly. I vaguely remembered the Stroop test from my college Perception and Cognition class and wanted to help her figure out the root cause of the trouble she was experiencing.

I manually made an 8x8 grid of Chinese words for four different colors, and we uncovered a pattern that caused task interference. When the Chinese word for red is colored green and placed next to another word colored green, my mom claimed the color would shift between red and green in her perception. After discussing the mechanics of how this struggle might be taking place in her brain, she was able to think about it and adapt. The next morning, armed with the knowledge of how the brain juggles the meaning of words versus the visual perception of ink on paper, she was able to slow down and read the puzzle correctly.

I built this app so she can use it to practice and rehab during her recovery from her stroke. I hope by making this open source, the app can help many people who are recovering from stroke or other brain trauma.

> **Important:** Please use this app under the direction of a medical professional.

## Features

- **Interactive 8x8 Stroop Puzzle** - Count ink colors while ignoring word meanings
- **Configurable Difficulty** - 2-8 colors, 0-100% congruence levels
- **Multi-language Support** - Chinese, English, and Vietnamese color labels
- **Mobile Responsive** - Dynamic font sizing adapts to viewport and language
- **Answer Submission** - Enter counts and check accuracy with scoring feedback
- **Hidden Answer Key** - Reveal after attempting the puzzle
- **Seed-based Generation** - Reproducible puzzles for consistent testing
- **Language Persistence** - Preference saved across sessions via localStorage

## Supported Languages

| Language | Labels |
|----------|--------|
| Chinese | 藍, 橙, 紫, 黑, 青, 金, 品, 灰 |
| English | Blue, Orange, Purple, Black, Cyan, Amber, Magenta, Gray |
| Vietnamese | Xanh, Cam, Tím, Đen, Lơ, Vàng, Hồng, Xám |

## Difficulty Levels

| Colors | Congruence | Difficulty | Description |
|--------|------------|------------|-------------|
| 2 | 12.5% | Easy | Only Blue/Orange, minimal choices |
| 4 | 12.5% | Medium | Default setting |
| 8 | 75% | Medium | Many colors but word often matches ink |
| 8 | 0% | Hardest | Maximum Stroop interference |

**Congruence** controls how often the word meaning matches the ink color. Lower congruence = stronger Stroop effect = harder puzzle.

## Quick Start

### Try it Online

Visit [colorfocus.vercel.app](https://colorfocus.vercel.app) to use the app immediately.

### Run Locally

```bash
# Clone the repository
git clone https://github.com/jc7k/ColorFocus.git
cd ColorFocus

# Start a local server
python3 -m http.server 8080

# Open in browser
# http://localhost:8080/frontend/puzzle.html
```

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Backend:** Python 3.11+, pytest
- **Shared:** JSON source of truth for cross-platform color constants
- **Hosting:** Vercel (static frontend)
- **Accessibility:** Color-blind friendly palette (deuteranopia, protanopia, tritanopia validated)

## Color Token System

The foundation of the application is a color token system optimized for color-blind accessibility.

### 8 Canonical Colors

| Token   | Dark | Base | Bright |
|---------|------|------|--------|
| BLUE    | Yes  | Yes  | Yes    |
| ORANGE  | Yes  | Yes  | Yes    |
| PURPLE  | Yes  | Yes  | Yes    |
| BLACK   | No   | Yes  | Yes    |
| CYAN    | Yes  | Yes  | Yes    |
| AMBER   | Yes  | Yes  | Yes    |
| MAGENTA | Yes  | Yes  | Yes    |
| GRAY    | Yes  | Yes  | Yes    |

**23 total color values** - All colors validated for deuteranopia, protanopia, and tritanopia accessibility.

### Architecture

```
/shared/
  colors.json              # Single source of truth for colors
  color_labels.json        # Multi-language color labels

/frontend/
  puzzle.html              # Interactive Stroop puzzle
  src/constants/colors.ts  # TypeScript constants

/backend/
  app/constants/colors.py  # Python constants (StrEnums)
```

## Development

### Prerequisites

- Node.js 18+
- Python 3.11+
- uv (Python package manager)

### Setup

**Frontend:**
```bash
cd frontend
npm install
npm test
```

**Backend:**
```bash
uv sync
uv run pytest
```

### Running Tests

```bash
# All Python tests
uv run pytest -v

# Frontend tests
cd frontend && npm test
```

## Deployment

### Deploy to Vercel (Recommended)

The frontend can be deployed as a static site on Vercel's free tier.

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project root
vercel

# For production deployment
vercel --prod
```

Your app will be live at `https://your-project.vercel.app`

## Contributing

Contributions are welcome! This project was built to help stroke recovery patients, and I'd love for the community to help make it even better.

### Ways to Contribute

- **Add new languages** - Help translate color labels to more languages
- **Improve accessibility** - Enhance screen reader support, keyboard navigation
- **Add features** - Progress tracking, difficulty progression, statistics
- **Fix bugs** - Report or fix issues you encounter
- **Documentation** - Improve README, add tutorials, translate docs

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`uv run pytest && cd frontend && npm test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Python: Follow PEP 8
- JavaScript: Use consistent formatting with existing code
- Commits: Use clear, descriptive commit messages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the classic Stroop test developed by John Ridley Stroop in 1935
- Built with love for my mother's stroke recovery
- Thanks to the open source community for making tools like this possible

---

**Disclaimer:** This application is intended for cognitive training and rehabilitation practice only. It is not a medical device and should not be used for diagnosis or treatment. Always consult with qualified healthcare professionals for medical advice and stroke rehabilitation programs.
