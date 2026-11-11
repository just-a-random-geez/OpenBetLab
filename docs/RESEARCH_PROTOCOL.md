# Research Protocol

These guidelines describe how research built on OpenBetLab should be done. The
aim is results that are honest, reproducible and hard to fool ourselves with.

## 1. Write the question down first

Before running anything, write down:

- the exact question (e.g. "How large is the average margin in this market?");
- the data you will use and where it came from;
- the method and calculations you will apply;
- what result would count as "no effect".

Writing this first protects against changing the question after seeing the
answer.

## 2. State every assumption

Every calculation rests on assumptions. Say them plainly. Examples:

- `joint_probability_independent` assumes the events are **independent**.
  Outcomes from the same match are usually **not** independent.
- `expected_value` assumes the probability you pass in is the *true*
  probability. It almost never is exactly.
- Implied probabilities from odds include the bookmaker's **margin**; they are
  not "true" probabilities.

## 3. Separate exploration from confirmation

It is fine to explore data freely, but any pattern found while exploring must
be checked on **different data** that was not used to find it. Otherwise
random noise looks like a real effect.

## 4. Beware of common traps

- **Multiple testing:** try enough ideas and one will look good by chance.
  Report how many things you tried.
- **Look-ahead bias:** never use information that would not have been
  available at the time (e.g. closing odds when studying opening odds).
- **Small samples:** a handful of matches proves nothing. Report sample sizes
  and uncertainty.
- **Survivorship bias:** don't silently drop matches, markets or seasons.

## 5. Make it reproducible

- Record the OpenBetLab version (`openbetlab --version`) and Python version.
- Keep scripts and data descriptions under version control.
- Anyone should be able to re-run your work and get the same numbers.

## 6. Report honestly

- Report negative and null results as well as positive ones.
- Do not describe findings as predictions of future outcomes.
- Do not present results as betting advice.

## 7. Respect the Data Policy

Only use data permitted by the [Data Policy](DATA_POLICY.md).
