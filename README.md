# MaddenTools

A collection of Python automation scripts designed to enhance Madden NFL franchise through data-driven roster management, contract modeling, draft tooling, and probabilistic event simulation. All scripts are designed to either improve upon existing game logic or add components missing from the game entirely to more closely resemble the actual NFL processes and front office decision-making.

---

## Tech Stack

- **Python 3** — pandas, numpy, PuLP, openpyxl
- **Data Format** — Excel (`.xlsx` / `.xlsm`) via Madden's Import/Export system
- **Techniques** — Vectorized DataFrame operations, in-memory SQLite queries, linear programming, probabilistic simulation

---

## Scripts

### Contract Value Engine — `ContractFixer.py`

Normalizes and corrects player contracts at the start of each season, using an expected salary table to determine market-rate AAV, bonus, and length by position and overall rating.

**Key features:**
- Salary interpolation from a configurable market-rate table
- Restructures year-by-year salary distributions to match realistic front-loading patterns (by contract length)
- Veteran age discounts by position:
- NFL-accurate **Proven Performance Escalator** for 4th-year Round 2-7 rookies — three escalator tiers based on snap participation percentages and Pro Bowl appearances
- Rookie minimum salary enforcement (Year 1-3 players)

---

### Contract Salary Adjustment — `ContractSalaryAdjustment.py`

Applies a configurable league-wide multiplier to all signed player contract values to simulate salary cap deflation or correction after import.

**Key features:**
- Configurable `adjustment_multiplier` (default ~0.928)
- Applies to all `ContractSalary0-7`, `ContractBonus0-7`, and `PLYR_CAPSALARY` columns
- Exports only modified columns to minimize import scope

---

### Draft Class Setup — `DraftClassEdit.py`

Prepares incoming draft class players for simulation. Operates in two configurable phases:

**Phase 1 — `No_Traits`** (attribute editing):
- Resets out-of-position attributes (awareness, kick ratings, injury ratings)
- Applies position-specific floor/ceiling adjustments for all 19 positions
- Rare chance for skill position players to have legitimate kick ratings, WRs to have coverage ability, CBs to have route-running ability
- DT Nose Tackle sub-archetype logic via a hidden weight marker attribute

**Phase 2 — `Traits`** (personality assignment):
- Assigns player traits probabilistically based on underlying attribute ratings (e.g., high `JukeMoveRating` increases `PT_ELUSIVEINSTINCT` odds)
- Full QB archetype logic: Pocket Passer, Scrambler, or Neither — sets scramble-relevant ratings accordingly
- Home state assignment using weighted state probabilities based on real NFL player origin data
- Sleeve temperature preferences by position group

---

### Draft Class Normalizer — `DraftClassNormalizer.py`

Applies position-specific random adjustments to draft class ratings to introduce realistic variance and reduce cookie-cutter ratings.

**Key features:**
- Configurable per-position strength modifiers (`Weak`, `Normal`, `Strong`) to model positional depth of the draft class
- Random deltas applied to all key attributes per position group
- Elite player protection: top-N players at each position receive an additional randomized boost to maintain separation from the pack

---

### Draft Class Position Edits — `DraftClassPositionEdits.py`

A manual fine-tuning layer applied after normalization. Applies flat adjustments to specific position groups based on the current year's roster composition and overall depth imbalances.

---

### Draft Class Letter Grades — `DraftLetterGrades.py`

Converts raw draft class attribute ratings into letter grades (A–F) and tiered labels (1-Poor through 7-Elite) for scouting readability. Grades are driven by position-specific spline curves loaded from an external scouting config file.

**Key features:**
- Per-position-group output sheets (QB, RB, WR, TE, OL, DL, LB, CB, SAF, ST) plus an "All" overview tab
- Color-coded cells by grade tier (green → red) with auto-width columns and filter rows
- Preferred column ordering per position group using abbreviated stat names
- Includes Rank (overall pick number), formatted height/weight, and age

---

### Draft Day Trade Simulator — `DraftDayTrades.py`

Simulates realistic draft day trade offers using a multi-factor probability engine.

**Key features:**
- Supports both **trading up** and **trading down** scenarios
- Trade probability calculated from: base pick position odds, team draft capital, number of current picks, and distance between picks
- "Hot zone" boosts for historically active trade windows (picks 1-5, 30-35, etc.)
- Value tier system (Fair, Slight Over, Big Over) determines the offer quality
- Outputs interested teams sorted by pick proximity with capital and offer tier details

---

### Draft Pick Trade Simulator — `DraftPickTrades.py`

Determines which teams are likely to trade down on each pick in the draft order and identifies eligible trade partners.

**Key features:**
- Trade-down probability driven by team draft capital: fewer picks = higher chance to move down (multiplier range 0.5x–2.5x)
- Pick position "hot zone" bonuses for historically active trade windows (picks 20–49)
- Eligible trade partners identified as teams holding picks of comparable value (50–100% of the trading pick's value)
- Exports a `DraftOrder` sheet with trade-down flags and a list of up to 3 potential trade partner team names

---

### Event System — `EventSystem.py`

A probabilistic offseason/preseason event simulator. Generates realistic player events to add narrative depth to the franchise.

**Simulated Events:**

| Event | Description |
|---|---|
| `Young_NewContract` | Young stars seeking extensions (3rd-4th year players) |
| `Vet_NewContract` | Veterans requesting new deals relative to market rate |
| `TradeUnhappy` | Trade requests driven by low morale |
| `TradeWR` | WR-specific trade demands based on usage, contract status, and morale |
| `TradePlayingTime` | Players low on depth chart requesting trades for more playing time |
| `TradeCutYoungPlayer` | Front office recommendations to trade/cut underperforming draft picks |
| `OffseasonInjury` | Preseason/offseason injury events |
| `Retire` | Age driven retirement |

---

### Free Agent Contract Fix — `FAContractFix.py`

Corrects contracts for players who sign as free agents mid-roster. Detects status changes between the pre-FA export and the current player sheet, computes expected contract length, and restructures salary year-by-year to reflect realistic escalating structures.

---

### Free Agent Class Report — `FreeAgentClass.py`

Generates a concise scouting report of the top 10 players per position among all free agents and expiring-contract players, sorted by overall rating. Used to update positional contract demands for that Free Agency (Ex. Low rated players at a certain position can get paid significantly more money than their OverallRating typically receives because the talent pool is limited that free agenecy)

---

### Re-Sign Contract Fix — `ResignContractFix.py`

Handles players with expiring contracts being re-signed. Identical restructuring logic to `FAContractFix.py` but cross-references the expiring contracts sheet and validates team continuity before applying changes.

---

### Practice Squad Contracts — `PracticeSquadContracts.py`

Normalizes contracts for players signed to the practice squad at the start of each season, converting short-term deals into proper multi-year futures contracts with minimum salary escalation.

**Key features:**
- Extends Year 0–1 players on 1-year contracts to 3-year futures deals
- Applies NFL minimum salary floors per years-pro bracket ($80K / $92K / $98K)
- Handles special case for 2nd-year UDFA players (`PLYR_DRAFTROUND == 63`) to correctly set contract year relative to their active roster eligibility

---

### Void Year Tracker — `VoidYears.py`

Identifies all signed players with void years in their contracts and flags which void years are triggered in the current season.

**Key features:**
- Detects void years by scanning for contract years where bonus > 0 but salary = 0, or where both are 0 at the player's current contract year
- Outputs `WhenVoid` (the year the void triggers), `VoidThisYear` activation flag, and full team/position context

---

### Preseason Trait & Attribute Check — `PreseasonTraitCheck.py`

The largest single-pass edit applied each preseason. Runs across all active, practice squad, and free agent players to normalize simulation attributes.

**Key features:**
- QB archetype resolution: maps pre-assigned draft traits to simulation-relevant ratings (pocket tendency, scramble aggressiveness, zone read awareness)
- Age-based speed decay for QBs 30+
- Throw accuracy composite recalculated from short/mid/deep components
- HB receiving threat proxy, WR/TE separation ability proxy via repurposed defensive ratings
- Edge rusher and DT pass rush signature ratings
- LB, CB, and Safety play style ratings
- Defensive tier simulation stat set from a coach-level team defensive tier sheet
- League minimum salary enforcement by years-pro bracket
- Player role tag assignments: `FranchiseQB`, `QBofTheFuture`, `BridgeQB`, `Day1Starter`, `FutureStarter`, `BridgePlayer`, `Mentor`

---

### Roster Position Checker — `RosterPositionChecks.py`

Generates a full roster depth report used as input for other scripts.

**Output sheets:**

| Sheet | Contents |
|---|---|
| `Counts` | Active player counts by team and position |
| `Differences` | Positional imbalances (e.g., LT count vs RT count per team) |
| `Contracts` | AAV and signing bonus for all signed players, adjusted by contract year with cap multipliers |
| `Team Position Depth` | Full depth chart with `Rank` and `HealthyRank` (among uninjured players), contract years remaining, position group groupings |

---

### Practice Squad Call-Up Checker — `PullFromPracticeSquad.py`

Scans the active roster for teams that fall below minimum position requirements (accounting for injury), and flags teams that have practice squad players eligible to fill those gaps.

---

### Preseason Waiver Claims — `PreseasonWaiverClaims.py`

Simulates preseason waiver wire activity by combining team positional need assessment with waiver claim priority order.

**Key features:**
- 14-position-group need tier system (Tiers 1–3): tiers assigned based on depth chart OVR thresholds (e.g., Tier 3 = critical need)
- Waiver claim priority derived from draft order (worst record picks first)
- Probabilistic claim simulation: base 65% claim probability, decreasing by 2% per additional claim placed, with tier-based bonuses (+15% for Tier 3, +10% for Tier 2)
- Maximum 4 claims per team per run
- Outputs top waiver targets per position group from free agents and practice squad players with ≤3 years pro

---

### Schedule Editor — `ScheduleEditor.py`

Generates realistic 18-week NFL schedules using **linear programming** (PuLP).

**Constraints enforced:**
- Exact game counts per week (matching EA's output distribution)
- Added Week 18 division matchups
- Super Bowl champion assigned Week 1 home game opener
- Lions and Cowboys guaranteed Thanksgiving home games

---

### Weekly Run Script — `WeeklyScript.py`

Updates injury lengths, assigns proper sim rating to newly signed players.

**Key features:**
- Recovery probability weighted by `InjuryRating` tier
- Player morale rating slightly shifts recovery probability
- Clears all injury data for uninjured players and resets wear-and-tear attributes
- Sets simulation tier stat based on coach tier ratings

---

### Development Trait Upgrader — `DevelopmentTraitUpgrade.py`

Assigns or removes Superstar development trait based on overall rating thresholds, with position-specific cutoffs. Downgrades XFactor/Superstar players who have declined below their threshold back to Star or Normal.

---

### Preseason Rookie Progression — `PreseasonRookieProgression.py`

Awards skill points to first-year players at the start of preseason based on development trait, using tiered weighted probability distributions.

| Dev Trait | Average Skill Points |
|---|---|
| Normal | ~1.5 |
| Star | ~3.0 |
| Superstar | ~4.5 |

---

### Stat-Based Progression Engine — `StatBasedEditor.py`

The primary in-season skill point award engine. Reads end-of-season game statistics from the AllProgRegInfo.xlsm file, calculates position-specific performance metrics, and cross-references against a configurable logic table to award or subtract skill points.

**Key features:**
- Processes 5 stat groups: Offensive, Defensive, O-Line, Kicking, and Return stats
- Minimum playing time filters enforced per group (e.g., 10+ games, 250+ snaps for skill positions; 400+ snaps for O-Line)
- Per-snap/per-touch efficiency metrics: scrimmage yards per 1,000 snaps, sacks per 1,000 snaps, FG%, DL sacks + TFL per 1,000 snaps, WR % of team pass yards, etc.
- In-memory SQLite join against a configurable logic/threshold table to determine stat tier and awarded points
- Negative skill points (below-baseline performers) convert to regression points before export
- Produces intermediate CSVs per stat group for debugging, then merges all results into a final player CSV

---

### Non-Qualifier Regression — `NonQualifiersStatBased.py`

Awards regression points to players who did not reach minimum playing time thresholds to qualify for stat-based skill points, penalizing lower-tier players who failed to contribute in a season.

**Key features:**
- Applies additional regression to WR, TE, HB, OL, and defensive players below snap thresholds, differentiated by OVR rating tier
- Higher regression for lower-tier non-contributors (3 points for tier_0–2, 2 points for tier_3–5 by position group)
- Rookies (YearsPro == 0) receive lighter regression (1 point) regardless of tier

---

### Age-Based Progression & Regression — `AgeBasedProgAndReg.py`

Final step of the annual progression/regression pipeline. Applies age-driven regression, free agent decline, veteran skill point bonuses, and zeroes out points for players past career-end thresholds.

**Key features:**
- Position-specific age-regression tables loaded from a configurable Excel file, supporting both age ranges and exact ages
- Free agent regression: 1–2 additional regression points for veteran free agents (OVR 51+)
- Veteran skill point lottery: small random chance for role players (OVR ≤ 75) to gain 1–2 skill points
- First-round rookie QB bonus: dev-trait weighted skill point additions for young QBs in their first pro year
- Career-end zero-out: players past position-specific age cutoffs (e.g., HB 30+, QB 38+) have all skill/regression points set to 0

---

### Compensatory Pick Status Setup — `CompPickContractStatusSetup.py`

Pre-processing step for the compensatory pick pipeline. Detects players on expiring contracts whose current-year contract slot has no salary — indicating void years have activated — and reclassifies them as `Expiring` to ensure accurate comp pick eligibility tracking.

---

### Compensatory Pick Value Determination — `CompPickValueDetermination.py`

Calculates each comp-pick-eligible player's market value ranking using AAV, All-Pro recognition, and snap participation, then assigns a compensatory pick round (3–7).

**Key features:**
- AAV computed from total contract value divided by active contract years
- Snap participation score: downs played as a percentage of positional expected snaps (1,100), capped at 100 points
- All-Pro bonuses: +20 points for 1st team, +5 points for 2nd team (from a separate `AllPros.xlsx` input)
- Percentile binning assigns `CompPickValue` labels of 3–7 to the top 35% of eligible players
- Outputs a full `CompPickPlayerValue.xlsx` with `CompRank` and `TotalPoints`

---

### Compensatory Picks Awarded — `CompPicksAwarded.py`

Final step of the comp pick pipeline. Cross-references player movement against their calculated pick values to determine which teams lost net comp-pick-eligible players and at what round.

**Key features:**
- Matches players who changed teams between the prior season's expiring contracts and the current roster
- Calculates `NetPlayersLost` per team (players lost to free agency minus comp-eligible players signed)
- Teams with `NetPlayersLost ≥ 1` are awarded comp picks; outputs separate `CompPickReport_picks` and `CompPickReport_nopicks` sheets
- Flags data mismatches (players in current data not found in the prior expiring contracts sheet)

---

### Potential System — `PotentialSystem`

A college-to-pro potential simulation engine for incoming draft classes. Models multi-year development across three skill point slots with a separate rookie roll distribution.

**Key features:**
- Three-season skill point rolls per player (`SkillPoints1/2/3`) using dev-trait weighted distributions
- Tracks dev trait changes between draft season and import (e.g., `Normal → Superstar`, `Star → XFactor`) and adjusts awarded points accordingly
- Partial redistribution of skill points into a "rookie roll" pool with random chance to unlock in-season
- Final output splits points into `NewSkillPoints1-3` for structured import

---

## File Structure

```
MaddenTools/
├── ContractFixer.py               # Season contract normalization + rookie escalators
├── ContractSalaryAdjustment.py    # League-wide salary multiplier correction
├── DraftClassEdit.py              # Draft class attribute + trait setup
├── DraftClassNormalizer.py        # Position-level rating variance
├── DraftClassPositionEdits.py     # Manual position group fine-tuning
├── DraftLetterGrades.py           # Draft class attribute → letter grade converter
├── DraftDayTrades.py              # Draft day trade probability simulator
├── DraftPickTrades.py             # Draft pick trade-down probability + partner finder
├── EventSystem.py                 # Offseason/preseason event simulation
├── FAContractFix.py               # Free agent contract restructuring
├── FreeAgentClass.py              # Top-10 free agent scouting report by position
├── ResignContractFix.py           # Re-sign contract restructuring
├── PracticeSquadContracts.py      # Practice squad future contract normalization
├── VoidYears.py                   # Void year detection and activation tracker
├── PreseasonTraitCheck.py         # Preseason attribute + tag normalization
├── PreseasonWaiverClaims.py       # Preseason waiver claim simulation
├── PotentialSystem                # College prospect potential engine
├── PullFromPracticeSquad.py       # Practice squad call-up eligibility checker
├── RosterPositionChecks.py        # Depth chart + contract report generator
├── ScheduleEditor.py              # LP-based season schedule generator
├── WeeklyScript.py                # Weekly injury duration adjustments + sim logic
├── DevelopmentTraitUpgrade.py     # Dev trait upgrade/downgrade logic
├── PreseasonRookieProgression.py  # Rookie preseason skill point awards
├── StatBasedEditor.py             # Stat-based skill point engine (main pipeline)
├── NonQualifiersStatBased.py      # Regression for non-qualifying players
├── AgeBasedProgAndReg.py          # Age/veteran progression and regression
├── CompPickContractStatusSetup.py # Comp pick pipeline: contract status pre-processing
├── CompPickValueDetermination.py  # Comp pick pipeline: player value calculation
├── CompPicksAwarded.py            # Comp pick pipeline: award determination
└── Files/
    └── Madden26/IE/               # Excel input/output files by season
```

---

## Dependencies

```
pandas
numpy
openpyxl
PuLP
```

Install with:

```bash
pip install pandas numpy openpyxl pulp
```
