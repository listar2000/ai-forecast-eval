# The FutureEval model leaderboard

Source: https://www.metaculus.com/notebooks/42076/the-futureeval-model-leaderboard/

Author: Sylvain (Metaculus). Published February 10, 2026; edited February 23, 2026. Retrieved November 9, 2026.

Format: web text extraction of the article body, not a summary. Original image URLs remain remote. Direct HTML retrieval was blocked by the site; use the source page for original presentation.

How do you measure forecasting skill? Since [November 2023](https://www.metaculus.com/notebooks/20025/new-scores-new-leaderboard-new-medals/), Metaculus’ answer has been the [Baseline](https://www.metaculus.com/help/scores-faq/#baseline-score) and [Peer](https://www.metaculus.com/help/scores-faq/#peer-score) scores.
Both are based on the [logarithmic scoring rule](https://en.wikipedia.org/wiki/Scoring_rule#Logarithmic_score) (aka [log score](https://www.metaculus.com/help/scores-faq/#log-score)), and compare forecasters against a flat prior, or against all other forecasters on the same question (respectively).
For [FutureEval](https://www.metaculus.com/futureeval/), we decided to create a leaderboard to rank LLM models’ forecasting ability. Each base model is given the full text of a Metaculus question, some news about the forecasted event, and has to provide a prediction. When the question resolves (i.e. when the real-world outcome is known) we can score their predictions.
AIs don’t tire, so they can very quickly predict every question on Metaculus, including of course all questions in our [Bot Tournaments](https://www.metaculus.com/aib/2026/spring/).
But how do we compare their accuracy? Not all models will forecast the same questions, both because GPT-5.2 and Claude 4.5 Opus can’t forecast questions that resolved last year, and because we’re running some models more extensively than others, on the [Metaculus Cup](https://www.metaculus.com/tournament/metaculus-cup-spring-2026/) for example. We can’t assume that all questions are the same difficulty, so we can’t use the Baseline scores.
The Peer scores compensate for question difficulty, but only if the distribution of forecaster skills is constant. This is definitely not the case for LLMs, since [they are getting better](https://www.metaculus.com/questions/31711/ai-system-beat-human-pros-in-forecasting-tournament-by-2030/) with each passing month.

To illustrate, let’s imagine we tested only five models: Clyde 1, 2, 4, 8 and 16. And let’s say they participate in 4 questions in a staggered pattern, with at most 2 models forecasting any question:

|                     | Question 1 | Question 2 | Question 3 | Question 4 | Average |
| ------------------- | ---------- | ---------- | ---------- | ---------- | ------- |
| Clyde 1 (skill -2)  | score = -1 |            |            |            | -1      |
| Clyde 2 (skill -1)  | score = +1 | score = -1 |            |            | 0       |
| Clyde 4 (skill 0)   |            | score = +1 | score = -1 |            | 0       |
| Clyde 8 (skill +1)  |            |            | score = +1 | score = -1 | 0       |
| Clyde 16 (skill +2) |            |            |            | score = +1 | +1      |

Despite each model being better than the previous one, the average scores completely fail to capture those differences.
We need a smarter method.

# A smarter method

We model the difference in log scores between two forecasters $A$ and $B$ on question $i$ as:

$$
\text{score}_{Ai} - \text{score}_{Bi} = \text{skill}_A - \text{skill}_B + \varepsilon
$$
That is, the difference between their scores is (on average) the difference between their skills. This is a simple model, but it solves several of our problems. By only looking at pairs of forecasters, we ignore which forecasters participated in which questions exactly. The only thing that matters is that forecasters have some matchups with each other.
Crucially, it can handle sparsity: if forecaster $B$ has matchups with $A$ and $C$, but $A$ and $C$ never predicted the same questions, we can still learn  $\text{skill}_C - \text{skill}_A = (\text{skill}_C - \text{skill}_B) - (\text{skill}_B - \text{skill}_A)$ (though question difficulty could still be a a problem, see [Future improvements](https://www.notion.so/Future-improvements-2ff6aaf4f101806a97cec2f97e1e0447?pvs=21) below).

A further wrinkle is forecasters with few matches: their estimated skill will be very noisy. We solve that by using a [Ridge regression](https://en.wikipedia.org/wiki/Ridge_regression). It is essentially an [OLS regression](https://en.wikipedia.org/wiki/Ordinary_least_squares) with an added regularization parameter $\lambda$ that pulls low-volume forecasters towards a skill of 0.

### Head-to-head scores
To compute score differences, we use head-to-head Peer Scores: Peer Scores calculated as if the two forecaster were the only participants on a question. Peer scores are by definition centered on 0, i.e. $\text{score}_{Ai} - \text{score}_{Bi}$, but that’s irrelevant in our model since it only looks at the difference.
We use Peer Scores because (i) they are already widely used on Metaculus, (ii) they provide comparable scores across all our question types and (iii) they handle non-synchronous participation (see [Score Weights](https://www.notion.so/Score-Weights-2ff6aaf4f1018065ad56e7b179a1a1fa?pvs=21) below).

### Score Weights
If a model starts predicting a question from the start and the other only joins halfway through, their head-to-head score will only take into account the time when they both had a standing forecast. It will hence have a weight of ½.
Scores from [Spot scored](https://www.metaculus.com/help/scores-faq/#spot-score) tournaments (like our Bot Tournaments) only count the standing prediction at a predefined spot scoring time. Since those include no forecast updates, and carry less signal, they are weighted a flat **⅓.**

### Estimating $\lambda$

The regularisation parameter should be set to the ratio:

$$
\lambda = {\sigma_\text{error}^2 \over \sigma_\text{skill}^2}
$$
This matches a Bayesian prior that skills $\sim \mathcal{N}(0, \sigma_{\text{skill}}^2)$ with observation noise $\sim \mathcal{N}(0, \sigma_{\text{error}}^2)$.

But of course we don’t know the errors or skills before we do the regression. We estimate the error term as the average standard deviation of score differences across the set $\mathcal{P}$ of all forecaster pairs:

$$
\hat{\sigma}_\text{error} = \frac{1}{|\mathcal{P}|} \sum_{(A,B) \in \mathcal{P}} \hat{\sigma}_{A,B}
$$

And we estimate the skill term by running a regression with only high-volume forecasters, and taking the variance of their skills. This is an underestimate, but has proven adequate in our testing.

### Scaling
The regression arbitrarily forces all forecaster skills to sum to 0. To make the skills more interpretable, we rescale them so they have the same range as Peer Scores, and we offset them so GPT-4o has a skill of 0 (chosen because it was our most prolific model when designing the skill score).

### Confidence Intervals
We estimate CIs by [bootstrapping](https://en.wikipedia.org/wiki/Bootstrapping_\(statistics\)): rerunning the analysis many times, each time sampling with replacement from all matchups, to get a distribution of possible results. (Bootstrapping on questions gives very similar results.)

### Code
You can find our code implementing the skill score [here](https://github.com/Metaculus/metaculus/blob/b4bd066826e40646b0d6260926cc5c420e6cf448/scoring/management/commands/update_global_bot_leaderboard.py#L408).

# Validation
To validate that this method can recover skills from scores, we simulate 100 forecasters where the first one has skill 1 and the last has skill 200, participating in a tournament. Forecasters join one by one in order of their skill, and leave one by one such that there is at most 50 forecasters on any question. This means that the first questions have only the worst forecasters, while the last have only the best.
Questions in the middle of the tournament have only middle forecasters, and crucially have neither the worst nor best.

This mimics our benchmark, where Gemini 3 was not running in late 2024, and GPT-3.5 is not running in 2026.

As expected the average scores do not capture the skills very well. The middle half of forecasters all have the same average score of 0:![](https://cdn.metaculus.com/user_uploaded/image_dykQLmZ.png)

But our regression recovers the skills very reliably:

![](https://cdn.metaculus.com/user_uploaded/image_1.png)
Forecasters near the extremes have more noise because they have fewer matches: the first questions only have a handful of forecasters, and the latest models have only participated in the last few questions.

# Implementation details

As time passes, each model's world knowledge becomes more and more out of date. To keep comparisons fair, we only use the predictions made in a model's first year.
Some Metaculus questions score forecasters at a specific point in time (aka [Spot Scores](https://www.metaculus.com/help/scores-faq#spot-score)), while others use their predictions from the whole lifetime of the question (time-averaging). The latter require forecasters to keep their predictions continuously updated, and therefore carry more signal regarding their skill. To compensate for that difference, Spot scored questions have a weight of ⅓ in the regression.

# Future improvements
### Question difficulty

The new method compensates for one dimension of question difficulty: the entropy of the questions. If two questions are about as hard to think about, then the score difference is the same regardless of their true probability. But it misses that other dimension: how hard it is to find the true probability, or in other words, how much does the spread of scores depend on skill differences. We’ll call that dimension the Discrimination of the questions.
Here are 3 questions to illustrate (this is a large oversimplification):

|                                                                                   | Outcome | Good forecaster                                          | Bad forecaster                                           | Score Difference |
| 

