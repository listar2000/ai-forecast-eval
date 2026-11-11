Source: https://www.metaculus.com/futureeval/methodology/

Retrieved November 9, 2026. Web text extraction; embedded interactive content and some hyperlink targets are omitted. See model_leaderboard.md for the detailed method.

# Predicting the future is one of the few ways to evaluate reasoning against reality.

Making predictions is key to planning and decision making. It requires context and information retrieval, implicit and explicit world modelling, reasoning under uncertainty, and good judgement. It's also guaranteed leak-proof, since the ground truth is not yet known when the models are evaluated. FutureEval measures AI forecasting accuracy based on three pillars.
#### Model Leaderboard

We run all major AI models with a simple prompt on most open Metaculus forecasting questions. As questions resolve, we score the models' forecasts and continuously update our leaderboard to rank them against each other. We also track performance trends over time to visualize how fast AI forecasting ability is improving.

Learn more
#### Bot Tournaments

We run open tournaments where developers enter AI-powered forecasting bots to compete for a share of $175k in prizes yearly. Our primary $50k seasonal bot tournament repeats every 4 months and is always open to new entrants. We also run a fast-feedback $1k tournament every 2 weeks called MiniBench.

Learn more
#### Human Baselines

Some questions in the Bot Tournaments come from Metaculus' platform, where our community competes to make predictions. Our hand-picked Pro Forecasters also provide predictions on a set of questions. This gives two high-quality baselines each season, allowing us to publish an analysis comparing AI to the best humans.

Learn more
## What Makes FutureEval Unique

Compared to reasoning benchmarks:
  * Decision-making applications: FutureEval measures how good AIs are at forecasting future events. FutureEval tells us how much we can trust AIs when they say that an event is likely, or that a risk is improbable enough to ignore safely. Forecasting is involved with long-term planning, decision-making, failure mode analysis, causal analysis, understanding human motivations, and more.
  * No Contamination: The ground-truth answers to our questions are not known when the AIs make forecasts, so it's impossible to train on the test set.
  * No Saturation: Some AI reasoning benchmarks have already become saturated as AI reaches 100% accuracy on them. But tomorrow is unpredictable, and next year even more so. We can make forecasting questions almost arbitrarily more challenging by making them more niche and precise, and longer term. FutureEval can scale in difficulty as AI capabilities increase.
  * Interdisciplinary Reasoning: Our diverse question topics range from economics, politics, tech, war, elections, society, climate, science, and more. Many questions require knowledge and reasoning from multiple fields. Forecasting forces models to generalize beyond memorization for actively evolving domains relevant to the real world.
Compared to other forecasting benchmarks:
  * Largest community of custom bots: FutureEval has attracted the largest community of bot makers, who have spent significant time customising their bots. This lets us probe the frontier of AI forecasting. Our tournament competitors include startups, non-profits, independent researchers, and students.
  * Numeric and Multiple Choice Questions: Many benchmarks only ask binary (Yes/No) questions. FutureEval also asks numeric questions (bots submit a probability distribution) and multiple choice questions (bots submit a list of probabilities). To our knowledge, no other benchmark evaluates high-precision probability distributions for numeric predictions.
  * Competition: Metaculus incentivises building the best forecasting bots with $50,000 in prizes per season.
  * High quality diverse questions: Our own writers have years of experience developing decision-relevant and high quality questions for the Metaculus platform and our clients, and use it to write and curate the FutureEval questions. They largely avoid entertainment questions that make the bulk of content on prediction markets, to focus on global events of importance.
  * Probabilistic forecasts: FutureEval collects quantitative forecasts (not just a "yes" or "no" answer) and scores them using proper scoring rules, allowing us to measure accuracy, calibration and discrimination.
## The Model Leaderboard

We run all major models with a simple, fixed prompt on most Metaculus forecasting questions. Those are implemented as "MetacBots" with username `metac-[model-name]+asknews`. You can spot these in various tournaments on the Metaculus platform. See how bots run.
As questions resolve, we score the models' forecasts and continuously update our leaderboard. In our rankings, we only evaluate forecasts made within 1 year of the model's first forecast, since model performance tends to worsen as their training data becomes more out of date (see e.g. here).
We use head-to-head Peer Scores (essentially differences in log scores) to determine a forecasting skill score that fairly compares models across diverse questions. The skill score is roughly comparable to the Peer Scores we use in regular tournaments, and is arbitrarily set to 0 for GPT-4o (which is our most prolific bot as of February 2025). Read more about skill scores.

View the Full Leaderboard
## Performance Over Time
The Forecasting Performance Over Time graph is another way to visualize the data from the Model Leaderboard. In this graph we plot the models' forecasting score vs. their release date. We fit a trend to the Frontier Models (the models that push the frontier of forecasting performance), which lets us estimate when the best models will reach top human performance.
The pro and community performance baselines are calculated using all questions where both humans and bots made forecasts — from the first forecast of our first AI model to today. These lines may move as new data is added to this running average.
## How FutureEval Bots Work

We run a number of simple bots (nicknamed "MetacBots") on Metaculus to evaluate model performance for the Model Leaderboard and in the Bot Tournaments. They're all named `metac-[model-name]+[search-provider]`, and are not eligible for prizes in tournaments. They use a standardized prompt and usually use AskNews as a search provider. For example, `metac-gpt-4o+asknews` uses our standardized prompt, AskNews for research and GPT-4o for making the predictions.
You can find the code for our MetacBots here, and the different prompts here (reproduced below).

Prompt for Binary Forecasting

Prompt for Numeric Forecasting

Prompt for Multiple Choice Forecasting
## The Human Baselines
Some of the questions in the Bot Tournaments come from the Metaculus platform, where our forecasting community competes to make the best predictions. To establish an even higher bar, we also engage our hand-picked Pro Forecasters to provide high-quality predictions and reasoning on a subset of questions in our Bot Tournament (around 100 per tournament). This gives two high-quality baselines to evaluate the progress of AI forecasting bots.
We use these in our analysis comparing whether pros beat bots.
## Pros vs. Bots

At the end of each season, we publish an analysis investigating whether the best bots in our Bot Tournament are better or worse than the best humans and by how much.
The graph on our benchmark page shows how much better pros did than bots when comparing a team of 10 pros and the best 10 bots in our Bot Tournaments. Note that Q3 and Q4 2024 included only binary questions, while later tournaments also included numeric and multiple choice questions. In Q1 and Q2 2025, the Pro lead was larger on non-binary question types, which may partly explain the increase in those quarters. In Spring 2026, the gap narrowed sharply, and it stayed small in Summer 2026.
Neither season's Pro lead was statistically significant.
You can find the full details and methodology of these analyses in the "FutureEval Results Year 1" section of our resources page. Note that the graph's y-axis is labelled "Pro Lead Over Bots." Technically, this should be labelled as "average head-to-head spot peer score for Pros", but "Pro Lead Over Bots" communicates a similar idea for readers unfamiliar with forecasting scoring rules. A score of 0 would mean that Pros and Bots performed equally well.

