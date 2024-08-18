# BCPS Bands Analysis

This project aims to analyze the performance of various high school bands within the BCPS system by calculating an objective function based on their MPA (Music Performance Adjudication) scores. The analysis considers both the difficulty of the music performed (Grade Level) and the scores provided by judges, with a particular focus on how well bands perform relative to their feeder middle schools.

## Objective Function

The objective function is designed to measure band performance, incorporating both the Grade Level (musical difficulty) and the judges' scores. The Grade Level is considered exponential but less so because it can go up to 6 (with 6 being the best). Judges' scores are also exponential, but since a score of 1 is the best (and most bands score between 1 and 2, with rare instances of 3), we divide by 2 in the formula.

$$
Objective = (Grade Level^{(Grade Level/2)}) \times (50 - (J1^{J1}) - (J2^{J2}) - (J3^{J3}) - (SR^{SR}))
$$

## Relative Performance

The relative performance metric compares each high school's performance to the average performance of its feeder middle schools from previous years. Since high school bands often lag behind middle school performance, this metric helps identify schools that are performing better or worse than expected, given their middle school feeder's performance a few years prior.

## Handling Missing Data

- **Sightreading (N/A):** Bands that perform at too low of a level to sightread are filled in with a value of 2.2. This value was chosen because a lower value like 0 would artificially improve their score.
- **Comments Only (C/O):** Performances marked as "Comments Only" are assumed to have not performed well, and are given a value of 2.3.

## Schools and Bands

Schools can have multiple bands, such as Concert Band, Symphonic Band, or Wind Ensemble. The analysis accounts for different performances and calculates the objective function for each band individually.

## Plots and Analysis

The following plots are included in the analysis:

1. **Feeder Relationships**: Analyzes how high schools and their feeder middle schools' performances correlate.
2. **Objective Functions**: Displays maximum, average, and minimum objective functions over the years.
3. **Relative Performance**: Compares the relative performance of high schools to their feeder middle schools.

## View the Analysis

You can view some of the generated plots [here](https://zakk-h.github.io/BCPSBands/) ![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-181717?logo=github&style=for-the-badge) if you do not want to run the scripts for yourself.
