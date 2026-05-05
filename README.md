# GenAI
Projects and experiments related to Generative AI

# Examples

## Question

Show me the distinct move distribution between special and physical as ratio for every type. Include the average attack and special attack for the corresponding type. Include ratio for physical:special as float and ratio for average attack:average special attack as float

## Answer

Here are the distinct move distributions between special and physical as ratios for each type, along with the average attack and special attack for the corresponding type:

| Type      | Physical Count | Special Count | Physical:Special Ratio | Avg Attack | Avg Special Attack | Avg Attack:Avg Special Attack Ratio |
|-----------|----------------|----------------|------------------------|------------|--------------------|-------------------------------------|
| BUG       | 14             | 6              | 2.33                   | 66.25      | 56.72              | 1.17                                |
| DARK      | 23             | 4              | 5.75                   | 84.36      | 71.11              | 1.19                                |
| DRAGON    | 9              | 12             | 0.75                   | 98.81      | 80.29              | 1.23                                |
| ELECTRIC  | 12             | 14             | 0.86                   | 73.90      | 84.29              | 0.88                                |
| FAIRY     | 2              | 10             | 0.20                   | 62.76      | 78.90              | 0.79                                |
| FIGHTING  | 36             | 5              | 7.20                   | 99.67      | 52.83              | 1.89                                |
| FIRE      | 11             | 23             | 0.48                   | 83.74      | 82.64              | 1.01                                |
| FLYING    | 14             | 7              | 2.00                   | 71.57      | 68.71              | 1.04                                |
| GHOST     | 11             | 6              | 1.83                   | 69.32      | 85.61              | 0.81                                |
| GRASS     | 18             | 14             | 1.29                   | 72.77      | 71.92              | 1.01                                |
| GROUND    | 16             | 5              | 3.20                   | 92.66      | 51.49              | 1.80                                |
| ICE       | 11             | 10             | 1.10                   | 73.07      | 76.82              | 0.95                                |
| NORMAL    | 66             | 21             | 3.14                   | 73.86      | 56.05              | 1.32                                |
| POISON    | 6              | 10             | 0.60                   | 73.03      | 66.14              | 1.10                                |
| PSYCHIC   | 4              | 21             | 0.19                   | 63.53      | 91.14              | 0.70                                |
| ROCK      | 11             | 3              | 3.67                   | 87.12      | 59.74              | 1.46                                |
| STEEL     | 18             | 4              | 4.50                   | 88.57      | 68.67              | 1.29                                |
| WATER     | 12             | 19             | 0.63                   | 71.20      | 71.21              | 1.00                                |

## Question

Calculate median move power per type per category (physical, special) along with their counts. Columns should be type, median power per categories and count per categories

## Answer

| type    | median_power_physical | count_physical | median_power_special | count_special |
|---------|-----------------------|----------------|----------------------|----------------|
| Bug     | 70.0                  | 14             | 67.5                 | 6              |
| Dark    | 65.0                  | 23             | 82.5                 | 4              |
| Dragon  | 60.0                  | 9              | 100.0                | 12             |
| Electric| 87.5                  | 12             | 70.0                 | 14             |
| Fairy   | 82.5                  | 2              | 85.0                 | 10             |
| Fighting| 70.0                  | 36             | 80.0                 | 5              |
| Fire    | 80.0                  | 11             | 100.0                | 23             |
| Flying  | 70.0                  | 14             | 75.0                 | 7              |
| Ghost   | 80.0                  | 11             | 72.5                 | 6              |
| Grass   | 72.5                  | 18             | 80.0                 | 14             |
| Ground  | 77.5                  | 16             | 65.0                 | 5              |
| Ice     | 65.0                  | 11             | 65.0                 | 10             |
| Normal  | 50.0                  | 66             | 60.0                 | 21             |
| Poison  | 60.0                  | 6              | 65.0                 | 10             |
| Psychic | 75.0                  | 4              | 90.0                 | 21             |
| Rock    | 60.0                  | 11             | 80.0                 | 3              |
| Steel   | 70.0                  | 18             | 110.0                | 4              |
| Water   | 80.0                  | 12             | 80.0                 | 19             |
