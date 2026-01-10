# Product Roadmap

## Phase 1: MVP - Core Puzzle Experience

1. [x] Color Token System — Implement the 8 canonical color tokens (BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY) with DARK, BASE, and BRIGHT variants, ensuring all colors are distinguishable for common forms of color blindness. `S`

2. [x] Puzzle Grid Generator — Build the core algorithm that generates 8x8 word jungle grids with color words rendered in different ink colors, creating Stroop interference patterns. `M`

3. [x] Answer Key Generation — Automatically calculate and store the correct count for each ink color in a generated puzzle, providing immediate verification capability. `S`

4. [x] Difficulty Tier Configuration — Implement three difficulty tiers (Accessible/Recovery, Standard, Advanced) with configurable parameters for grid size, color count, and interference level. `S`

5. [x] Puzzle Display UI — Create the main puzzle interface with large sans-serif fonts, clear grid layout, and the color counting task instructions prominently displayed. `M`

6. [x] Answer Submission Interface — Build the UI for users to enter their color counts and receive immediate feedback on accuracy against the answer key. `S`

7. [x] Adjustable Grid Spacing — Add user controls for grid density and spacing to accommodate various visual and motor abilities. `S`

8. [x] Chinese Character Labels — Add single-character Chinese labels as an alternative identifier for each color token, supporting users who may benefit from dual-coding. `XS`

9. [x] Basic User Authentication — Implement simple user accounts to enable puzzle history and progress tracking across sessions. `M`

10. [ ] Puzzle History Storage — Store completed puzzles with timestamps, user answers, and accuracy for each authenticated user. `S`

## Phase 2: Scoring and Caregiver Features

11. [ ] Scoring Metrics Calculation — Calculate and store detailed metrics including accuracy percentage, completion time, error distribution by color, and Stroop interference patterns. `M`

12. [ ] User Progress Dashboard — Create a personal dashboard showing recent puzzle completions, accuracy trends, and average completion times over configurable time periods. `M`

13. [ ] Caregiver Account Linking — Enable caregiver accounts to be linked to user accounts with appropriate permissions for viewing progress data. `S`

14. [ ] Caregiver Dashboard — Build a dedicated dashboard for caregivers showing linked users' activity summaries, engagement patterns, and performance trends. `M`

15. [ ] Weekly Summary Generation — Automatically generate weekly summaries highlighting practice frequency, accuracy changes, completion time trends, and areas of difficulty. `M`

16. [ ] Trend Visualization Charts — Implement line and bar charts showing performance metrics over time, with filtering by date range and difficulty tier. `M`

17. [ ] Error Pattern Analysis — Analyze and display which color combinations cause the most errors for each user, identifying specific Stroop interference challenges. `S`

## Phase 3: Export and Advanced Features

18. [ ] Printable Puzzle Layout — Generate print-optimized puzzle layouts with proper margins, clear typography, and space for written answers. `S`

19. [ ] PDF Export for Puzzles — Enable users to download individual puzzles or puzzle sets as PDF files for offline practice. `M`

20. [ ] PDF Progress Reports — Generate professional PDF reports summarizing user progress, suitable for sharing with healthcare providers or family members. `M`

21. [ ] Batch Puzzle Generation — Allow generation of multiple puzzles at once for users who want to prepare a week of exercises or print a workbook. `S`

22. [ ] Custom Difficulty Configuration — Enable advanced users or clinicians to customize specific puzzle parameters beyond the three preset tiers. `S`

23. [ ] Session-Based Practice Mode — Implement timed practice sessions with multiple puzzles and aggregate scoring for structured cognitive exercise. `M`

24. [ ] Research/Clinical Mode — Add optional detailed data export capabilities for occupational therapists or researchers tracking patient progress with granular metrics. `L`

25. [ ] Expanded Puzzle Types — Introduce additional Stroop-variant puzzles such as directional interference or numeric Stroop to provide variety while maintaining the core cognitive training focus. `L`

> Notes
> - Order reflects technical dependencies and incremental value delivery
> - Phase 1 delivers a complete, accessible puzzle experience
> - Phase 2 adds engagement and monitoring features for sustained use
> - Phase 3 extends utility for clinical and offline contexts
> - Each item represents a complete, testable feature spanning frontend and backend as needed
