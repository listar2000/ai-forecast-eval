Source: https://www.metaculus.com/help/scores-faq/

Retrieved November 9, 2026. Converted from the official public Metaculus website source because direct HTML downloads were blocked. Includes the expandable mathematics sections. Source files are retained in `source/`; revision is recorded in `../metaculus_source_revision.txt`. This is a source snapshot, which may differ from the deployed website.

 

# Scores FAQ

Below are Frequently Asked Questions (and answers!) about scores. The general FAQ is [here](https://www.metaculus.com/faq/), and the medals FAQ is [here](https://www.metaculus.com/help/medals-faq/).

* [Scores](https://www.metaculus.com/help/scores-faq/#scores-section)

+ [What is a scoring rule?](https://www.metaculus.com/help/scores-faq/#scoring-rule)
+ [What is a proper scoring rule?](https://www.metaculus.com/help/scores-faq/#proper-scoring)
+ [What is the log score?](https://www.metaculus.com/help/scores-faq/#log-score)
+ [What is the log score for continuous questions?](https://www.metaculus.com/help/scores-faq/#continuous-log-score)
+ [What is a spot score?](https://www.metaculus.com/help/scores-faq/#spot-score)
+ [What is the Baseline score?](https://www.metaculus.com/help/scores-faq/#baseline-score)
+ [What is the Peer score?](https://www.metaculus.com/help/scores-faq/#peer-score)
+ [Why is the Peer Score of the Community Prediction positive?](https://www.metaculus.com/help/scores-faq/#cp-positive-peer)
+ [Do all my predictions on a question count toward my score?](https://www.metaculus.com/help/scores-faq/#time-averaging)
+ [Can I get better scores by predicting extreme values?](https://www.metaculus.com/help/scores-faq/#extremizing)
+ [Why did I get a small score when I was right?](https://www.metaculus.com/help/scores-faq/#score-truncation)
+ [What are the legacy scores?](https://www.metaculus.com/help/scores-faq/#legacy-scores)
  - [What is the Relative score?](https://www.metaculus.com/help/scores-faq/#relative-score)
  - [What is the coverage?](https://www.metaculus.com/help/scores-faq/#coverage)
  - [What are Metaculus points?](https://www.metaculus.com/help/scores-faq/#old-points)

* [Tournaments](https://www.metaculus.com/help/scores-faq/#tournaments-section)

+ [How are my tournament Score, Coverage, Take, Prize and Rank calculated?](https://www.metaculus.com/help/scores-faq/#tournament-scores)
+ [How are my (legacy) tournament Score, Coverage, Take, Prize and Rank calculated?](https://www.metaculus.com/help/scores-faq/#legacy-tournament-scores)
+ [What are the Hidden Period and Hidden Coverage Weights?](https://www.metaculus.com/help/scores-faq/#hidden-period)

---

# Scores

---

## What is a scoring rule?

A scoring rule is a mathematical function which, given a prediction and an outcome, gives a score in the form of a number.

A naive scoring rule could be: "you score equals the probability you gave to the correct outcome". So, for example, if you predict 80% and the question resolves Yes, your score would be 0.8 (and 0.2 if the question resolved No). At first glance this seems like a good scoring rule: forecasters who gave predictions closer to the truth get higher scores.

Unfortunately this scoring rule is not "proper", as we'll see in the next section.

---

## What is a proper scoring rule?

Proper scoring rules have a very special property: the only way to optimize your score on average is to predict your sincere beliefs.

How do we know that the naive scoring rule from the previous section is not proper? An example should be illuminating: consider the question "Will I roll a 6 on this fair die?". Since the die is fair, your belief is "1/6" or about 17%. Now consider three possibilities: you could either predict your true belief (17%), predict something more extreme, like 5%, or predict something less extreme, like 30%. Here's a table of the scores you expect for each possible die roll:

| outcome die roll | naive score of p=5% | naive score of p=17% | naive score of p=30% |
| --- | --- | --- | --- |
| 1 | 0.95 | 0.83 | 0.7 |
| 2 | 0.95 | 0.83 | 0.7 |
| 3 | 0.95 | 0.83 | 0.7 |
| 4 | 0.95 | 0.83 | 0.7 |
| 5 | 0.95 | 0.83 | 0.7 |
| 6 | 0.05 | 0.17 | 0.3 |
| average | 0.8 | 0.72 | 0.63 |

Which means you get a better score on average if you predict 5% than 17%. In other words, this naive score incentivizes you to predict something other than the true probability. This is very bad!

Proper scoring rules do not have this problem: your score is best when you predict the true probability. The log score, which underpins all Metaculus scores, is a proper score (see [What is the log score?](https://www.metaculus.com/help/scores-faq/#log-score)). We can compare the scores you get in the previous example:

| outcome die roll | log score of p=5% | log score of p=17% | log score of p=30% |
| --- | --- | --- | --- |
| 1 | -0.05 | -0.19 | -0.37 |
| 2 | -0.05 | -0.19 | -0.37 |
| 3 | -0.05 | -0.19 | -0.37 |
| 4 | -0.05 | -0.19 | -0.37 |
| 5 | -0.05 | -0.19 | -0.37 |
| 6 | -3 | -1.77 | -1.2 |
| average | -0.54 | -0.45 | -0.51 |

With the log score, you do get a higher (better) score if you predict the true probability of 17%.

---

## What is the log score?

The logarithmic scoring rule, or "log score" for short, is defined as:

$$
\text{log score} = \ln(P(outcome))
$$

Where $\ln$ is the natural logarithm and $P(outcome)$ is the probability predicted for the outcome that actually happened. This log score applies to categorical predictions, where one of a (usually) small set of outcomes can happen. On Metaculus those are Binary and Multiple Choice questions. See the next section for the log scores of continuous questions.

Higher scores are better:

* If you predicted 0% on the correct outcome, your score will be $-\infty$ (minus infinity).
* If you predict 100% on the correct outcome, your score will be 0.

This means that the log score is always negative (for Binary and Multiple Choice questions). This has proved unintuitive, which is one reason why Metaculus uses the [Baseline](https://www.metaculus.com/help/scores-faq/#baseline-score) and [Peer](https://www.metaculus.com/help/scores-faq/#peer-score) scores, which are based on the log score but can be positive.

The log score is proper (see  [What is a proper scoring rule?](https://www.metaculus.com/help/scores-faq/#proper-scoring)  ). This means that to maximize your score **you should predict your true beliefs** (see  [Can I get better scores by predicting extreme values?](https://www.metaculus.com/help/scores-faq/#extremizing)  ).

One interesting property of the log score: it is much more punitive of extreme wrong predictions than it is rewarding of extreme right predictions. Consider the scores you get for predicting 99% or 99.9%:

|  | 99% Yes, 1% No | 99.9% Yes, 0.1% No |
| --- | --- | --- |
| Score if outcome = Yes | -0.01 | -0.001 |
| Score if outcome = No | -4.6 | -6.9 |

Going from 99% to 99.9% only gives you a tiny advantage if you are correct (+0.009), but a huge penalty if you are wrong (-2.3). So be careful, and only use extreme probabilities when you're sure they're appropriate!

---

## What is the log score for continuous questions?

Since the domain of possible outcomes for numeric and date continuous questions is (drum roll) continuous, any outcome has mathematically 0 chance of happening. Thankfully we can adapt the log score in the form:

$$
\text{log score} = \ln(\operatorname{pdf}(outcome))
$$

Where $\ln$ is the natural logarithm and $\operatorname{pdf}(outcome)$ is the value of the predicted  [probability density function](https://en.wikipedia.org/wiki/Probability_density_function)  at the outcome. Note that on Metaculus, all pdfs have a  [uniform distribution](https://en.wikipedia.org/wiki/Uniform_distribution)  of height 0.01 added to them. This prevents extreme log scores.

For discrete continuous questions, the pmf is used in place of the pdf, and the minimum value assigned to any outcome cannot go below 0.01 / number of possible inbound outcomes. This is effectively the same operation as the uniform 0.01 distribution added to pdfs.

This is also a proper scoring rule, and behaves in somewhat similar ways to the log score described above. One difference is that, contrary to probabilities that are always between 0 and 1, $\operatorname{pdf}$ values can be greater than 1. This means that the continuous log score can be greater than 0: in theory it has no maximum value, but in practice Metaculus restricts how sharp pdfs can get (see the maximum scores tabulated below).

When a continuous question resolves either above the upper bound or below the lower bound, it is scored like a binary question. We do not define or collect pdf values outside the question range, so the above formula does not apply. But we do have the total probability mass out the bound, and that can be scored as in the question "Will the value be below the lower bound?" or "Will the value be above the upper bound?".

---

## What is a spot score?

A "spot" score is a specific version of the given score type (e.g. "spot peer score") where the evaluation doesn't take prediction duration into account. For a spot score, only the prediction at a specified time is considered. Unless otherwise indicated, spot scores are evaluated at the same time the Community Prediction is revealed. Coverage is 100% if there is an active prediction at the time, and 0% if there is not. The math is the same as the given score type.

---

## What is the Baseline score?

The Baseline score compares a prediction to a fixed "chance" baseline. If it is positive, the prediction was better than chance. If it is negative, it was worse than chance.

That "chance" baseline gives the same probability to all outcomes. For binary questions, this is a prediction of 50%. For an N-option multiple choice question it is a prediction of 1/N for every option. For continuous questions this is a uniform (flat) distribution.

The Baseline score is derived from the [log score](https://www.metaculus.com/help/scores-faq/#log-score), rescaled so that:

* Predicting the same probability on all outcomes gives a score of 0.
* Predicting perfectly on a binary or multiple choice question gives a score of +100.
* The average scores of binary and continuous questions roughly match.

Here are some notable values for the Baseline score:

|  | Binary questions | Multiple Choice questions   (8 options) | Continuous questions |
| --- | --- | --- | --- |
| Best possible Baseline score on Metaculus | +99.9 | +99.9 | +183 |
| Worst possible Baseline score on Metaculus | -897 | -232 | -230 |
| Median Baseline empirical score | +17 | no data yet | +14 |
| Average Baseline empirical score | +13 | no data yet | +13 |

Theoretically, binary scores can be infinitely negative, and continuous scores can be both infinitely positive and infinitely negative. In practice, Metaculus restricts binary predictions to be between 0.1% and 99.9%, and continuous pdfs to be between 0.01 and ~35, leading to the scores above. The empirical scores are based on all scores observed on all resolved Metaculus questions, as of November 2023.

Note that the above describes the Baseline score at a single point in time. Metaculus scores are time-averaged over the lifetime of the question, see  [Do all my predictions on a question count toward my score?](https://www.metaculus.com/help/scores-faq/#time-averaging)  .

You can expand the section below for more details and maths.

### Baseline score math

The Baseline scores are rescaled [log scores](https://www.metaculus.com/help/scores-faq/#log-score), with the general form:

$$
\text{Baseline score} = 100 \times
            \frac{
            \operatorname{log\ score}(prediction) - \operatorname{log\ score}(baseline)
            }{
            \text{scale}
            }
$$

For binary and multiple choice questions, the $scale$ is chosen so that a perfect prediction ($P(outcome) = 100 \%$) gives a score of +100. The formula for a binary question is:

$$
\text{binary Baseline score} = 100 \times \frac{ \ln(P(outcome)) - \ln(50 \%) }{ \ln(2)}
$$

Note that you can rearrange this formula into: $100 \times(\log_2(P(outcome)) + 1)$.

The formula for a multiple choice question with N options is:

$$
\text{multiple choice Baseline score} = 100 \times \frac{ \ln(P(outcome)) - \ln(\frac{ 1}{ N}) }{ \ln(N)}
$$

For continuous questions, the $scale$ was chosen empirically so that continuous scores have roughly the same average as binary scores. The formula for a continuous question is:

$$
\text{continuous Baseline score} = 100 \times \frac{ \ln(\operatorname{pdf}(outcome)) - \ln(baseline) }{ 2 }
$$

Where $\ln$ is the natural logarithm, $P(outcome)$ is the probability predicted for the outcome that actually happened, and $\operatorname{pdf}(outcome)$ is the value of the predicted probability density function at the outcome.

The continuous $baseline$ depends on whether the question has open or closed bounds:

* If both bounds are closed, the $baseline$ is 1, corresponding to a uniform distribution in range.
* If one bound is open, the $baseline$ is 0.95, corresponding to a uniform distribution in range + 5% probability out of the open bound.
* If both bounds are open, the $baseline$ is 0.9, corresponding to a uniform distribution in range + 5% probability out of each open bound.

---

## What is the Peer score?

The Peer score compares a prediction to all the other predictions made on the same question. If it is positive, the prediction was (on average) better than others. If it is negative it was worse than others.

The Peer score is derived from the [log score](https://www.metaculus.com/help/scores-faq/#log-score): it is the average difference between a prediction's log score, and the log scores of all other predictions on that question. Like the Baseline score, the Peer score is multiplied by 100.

One interesting property of the Peer score is that, on any given question, the sum of all participants' Peer scores is always 0. This is because each forecaster's score is their average difference with every other: when you add all the scores, all the differences cancel out and the result is 0. Here's a quick example: imagine a  [continuous question](https://www.metaculus.com/help/scores-faq/#continuous-log-score)  , with three forecasters having predicted:

| Forecaster | log score | Peer score |
| --- | --- | --- |
| Alex | $-1$ | $$
\frac{(A-B)+(A-C)}{2} = \frac{(-1-1)+(-1-2)}{2} = -2.5
$$ |
| Bailey | $1$ | $$
\frac{(B-A)+(B-C)}{2} = \frac{(1-(-1))+(1-2)}{2} = 0.5
$$ |
| Cory | $2$ | $$
\frac{(C-A)+(C-B)}{2} = \frac{(2-(-1))+(2-1)}{2} = 2
$$ |
|  | sum | $$
-2.5+0.5+2 = 0
$$ |

Here are some notable values for the Peer score:

|  | Binary and   Multiple Choice   questions | Continuous   questions |
| --- | --- | --- |
| Best possible Peer score on Metaculus | +691 | +408 |
| Worst possible Peer score on Metaculus | -691 | -408 |
| Median Peer empirical score | +2 | +3 |
| Average Peer empirical score | 0\* | 0\* |

\*The average Peer score is 0 by definition.

Theoretically, binary scores can be infinitely negative, and continuous scores can be both infinitely positive and infinitely negative. In practice, Metaculus restricts binary predictions to be between 0.1% and 99.9%, and continuous pdfs to be between 0.01 and ~35, leading to the scores above.

The "empirical scores" are based on all scores observed on all resolved Metaculus questions, as of November 2023.

Note that the above describes the Peer score at a single point in time. Metaculus scores are time-averaged over the lifetime of the question, see  [Do all my predictions on a question count toward my score?](https://www.metaculus.com/help/scores-faq/#time-averaging)  .

You can expand the section below for more details and maths.

### Peer score math

The Peer scores are built on [log scores](https://www.metaculus.com/help/scores-faq/#log-score), with the general form:

$$
\text{Peer score} = 100 \times \frac{1}{N} \sum_{i = 1}^N \operatorname{log\ score}(p) - \operatorname{log\ score}(p_i)
$$

Where $p$ is the scored prediction, $N$ is the number of other predictions, and $p_i$ is the i-th other prediction.

Note that this can be rearranged into:

$$
\text{Peer score} = 100 \times (\ln(p) - \ln(\operatorname{GM}(p_i)))
$$

Where  [$\operatorname{GM}(p_i)$](https://en.wikipedia.org/wiki/Geometric_mean)  is the geometric mean of all other predictions.

As before, for binary questions $p$ is the probability given to the correct outcome (Yes or No), for multiple choice questions it is the probability given to the option outcome that resolved Yes, and for continuous questions it is the value of the predicted pdf at the outcome.

Note: Peer scores of continuous and discrete questions are further divided by 2. This factor was chosen empirically to bring continuous and discrete scores roughly in line with binary and multiple choice scores.

$$
\text{continuous Peer score} = 100 \times \frac{1}{2} \frac{1}{N} \sum_{i = 1}^N \operatorname{log\ score}(p) - \operatorname{log\ score}(p_i)
$$

---

## Why is the Peer score of the Community Prediction positive?

The [Peer score](https://www.metaculus.com/help/scores-faq/#peer-score) measures whether a forecaster was on average better than other forecasters. It is the difference between the forecaster's [log score](https://www.metaculus.com/help/scores-faq/#log-score) and the average of all other forecasters' log scores. If you have a positive Peer score, it means your log score was better than the average of all other forecasters' log scores.

The [Community Prediction](https://www.metaculus.com/faq/#community-prediction) is a time-weighted median of all forecasters on the question. Like most aggregates, it is better than most of the forecasters it feeds on: it is less noisy, less biased, and updates more often.

Since the Community Prediction is better than most forecasters, it follows that its score should be higher than the average score of all forecasters. And so its Peer score is positive.

### Further math details for nerds

If you have an intuition that something should be 0 and not positive, you are correct! The average Peer score across all users is guaranteed to be 0. This does not imply that the score of the average (or median) forecast is 0: the score of the mean is not the mean of the scores.

There is another reason why the Peer score of the Community Prediction is positive: you can rearrange the Peer score formula to show that it is the difference between the forecaster log score and the log score of the geometric mean of all other forecasters. Since the median will be higher than the geometric mean in most cases, it follows that the score of the Community Prediction will be positive in most cases.

---

## Do all my predictions on a question count toward my score?

Yes. Metaculus uses time-averaged scores, so all your predictions count, proportional to how long they were standing. An example goes a long way (we will use the Baseline score for simplicity, but the same logic applies to any score):

A binary question is open 5 days, then closes and resolves Yes. You start predicting on the second day, make these predictions, and get those scores:

|  | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 | Average |
| --- | --- | --- | --- | --- | --- | --- |
| Prediction |  | 40% | 70% |  | 80% | N/A |
| Baseline score | 0 | -32 | +49 | +49 | +68 | +27 |

Some things to note:

* Before you predict, your score is considered to be 0 (this is true for all scores based on the log score). This means that if you believe you can do better than 0, you should predict as early as possible.
* You have a score for Day 4, despite not having predicted that day. This is because your predictions stay standing until you update them, so on Day 4 you were scored on your Day 3 prediction. On Day 5 you updated to 80%, so you were scored on that.
* This example uses days, but your Metaculus scores are based on exact timestamped predictions, so a prediction left standing for 1 hour will count for 1/24th of a prediction left standing for a day, etc.

Lastly, note that scores are always averaged for every instant between the Open date and (scheduled) Close date of the question. If a question resolves early (i.e. before the scheduled close date), then scores are set to 0 between the resolution date and scheduled close date, and still count in the average. This ensures alignment of incentives, as explained in the section  [Why did I get a small score when I was right?](https://www.metaculus.com/help/scores-faq/#score-truncation)  below.

---

## Can I get better scores by predicting extreme values?

Metaculus uses proper scores (see  [What is a proper scoring rule?](https://www.metaculus.com/help/scores-faq/#proper-scoring)  ), so you cannot get a better score (on average) by making predictions more extreme than your beliefs. On any question, if you want to maximize your expected score, you should predict exactly what you believe.

Let's walk through a simple example using the Baseline score. Suppose you are considering predicting a binary question. After some thought, you conclude that the question has 80% chance to resolve Yes.

If you predict 80%, you will get a score of +68 if the question resolves Yes, and -132 if it resolves No. Since you think there is an 80% chance it resolves Yes, you expect on average a score of

$80\% \times 68 + 20\% \times -132 = +28$

If you predict 90%, you will get a score of +85 if the question resolves Yes, and -232 if it resolves No. Since you think there is an 80% chance it resolves Yes, you expect on average a score of

$80\% \times 85 + 20\% \times -232 = +21$

So by predicting a more extreme value, you actually lower the score you expect to get (on average!).

Here are some more values from the same example, tabulated:

| Prediction | Score if Yes | Score if No | Expected score |
| --- | --- | --- | --- |
| 70% | +48 | -74 | +24 |
| 80% | +68 | -132 | +28 |
| 90% | +85 | -232 | +21 |
| 99% | +99 | -564 | -34 |

The 99% prediction gets the highest score when the question resolves Yes, but it also gets the lowest score when it resolves No. This is why, on average, the strategy that maximizes your score is to predict what you believe. This is one of the reasons why looking at scores on individual questions is not very informative; only aggregate over many questions are interesting!

---

## Why did I get a small score when I was right?

To make sure incentives are aligned, Metaculus needs to ensure that our scores are proper. We also time-average scores.

This has a counter-intuitive consequence: when a question resolves before its intended close date, the times between resolution and close date need to count in the time-average, with scores of 0. We call this "score truncation".

An example is best: imagine the question "Will a new human land on the Moon before 2030?". It can either resolve Yes before 2030 (because someone landed on the Moon), or it can resolve No in 2030. If we did not truncate scores, you could game this question by predicting close to 100% in the beginning (since it can only resolve positive early), and lower later (since it can only resolve negative at the end).

Another way to think about this is that if a question lasts a year, then each day (or in fact each second) is scored as a separate question. To preserve properness, it is imperative that each day is weighted the same in the final average (or at least that the weights be decided in advance). From this perspective, not doing truncation is equivalent to retroactively giving much more weight to days before the question resolves, which is not proper.

You can read a worked example with maths by expanding the section below.

### Score truncation example

This example uses the Baseline score, which will be noted $S$, but results would be equivalent with any proper score.

Alex wants to predict if they will be fired this year. They have a performance review scheduled this week. They estimate there is a $20\%$ chance they fail it, and if so they will be fired on the spot. If they don’t fail this week, there is still a $5\%$ chance they will be fired at the end of the year. A proper scoring rule ensures that the best strategy on this question is to predict $(p=(20\%+80\% \times 5\%)=24\%$ this week, and then $5\%$ for the other 51 weeks (if they weren’t fired).

**Without truncation**

Without truncation, this honest strategy gives Baseline scores of:

* $S(24\%) \approx -106$ in the $20\%$ of cases they are fired this week.
* $\frac{1}{52}S(24\%) + \frac{51}{52}S(5\%) = -328$ in the $80\% \times 5\% = 4\%$ of cases they are fired at the end of the year.
* $\frac{1}{52}S(76\%) + \frac{51}{52}S(95\%) = +92$ in the $80\% \times 95\% = 76\%$ of cases they are not fired.

For an average score of $20\% \times -106 + 4\% \times -327 + 76\% \times +92 = +36$ in expectation.

But the strategy of “predicting close to 100% in the beginning and lower later”, let's say 99% today, then 5% the other 6 days, without truncation gives Baseline scores of:

* $S(99\%) \approx +99$ in the $20\%$ of cases they are fired this week.
* $\frac{1}{52}S(99\%) + \frac{51}{52}S(5\%) = -324$ in the $80\% \times 5\% = 4\%$ of cases they are fired at the end of the year.
* $\frac{1}{52}S(1\%) + \frac{51}{52}S(95\%) = +80$ in the $80\% \times 95\% = 76\%$ of cases they are not fired.

For an average score of $20\% \times +99 + 4\% \times -324 + 76\% \times +80 = +68$ in expectation.

Notice that $+68 > +36$, so without truncation, the gaming strategy gives you a score almost twice as high in expectation! It is really not proper.

**With truncation**

With truncation, the honest strategy gives Baseline scores of:

* $\frac{1}{52}S(24\%) \approx −2$ in the $20\%$ of cases they are fired this week.
* $\frac{1}{52}S(24\%) + \frac{51}{52}S(5\%) = -328$ in the $80\% \times 5\% = 4\%$ of cases they are fired at the end of the year.
* $\frac{1}{52}S(76\%) + \frac{51}{52}S(95\%) = +92$ in the $80\% \times 95\% = 76\%$ of cases they are not fired.

For an average score of $20\% \times -2 + 4\% \times -327 + 76\% \times +92 = +56$ in expectation.

While the gaming strategy gives:

* $\frac{1}{52}S(99\%) \approx +2$ in the $20\%$ of cases they are fired this week.
* $\frac{1}{52}S(99\%) + \frac{51}{52}S(5\%) = -324$ in the $80\% \times 5\% = 4\%$ of cases they are fired at the end of the year.
* $\frac{1}{52}S(1\%) + \frac{51}{52}S(95\%) = +80$ in the $80\% \times 95\% = 76\%$ of cases they are not fired.

For an average score of $20\% \times +2 + 4\% \times -324 + 76\% \times +80 = +48$ in expectation.

This time, $+56 > +48$, so with truncation, the gaming strategy gives you a worse score than the honest strategy! Which is proper.

---

## What are the legacy scores?

### What is the Relative score?

The Relative score compares a prediction to the median of all other predictions on the same question. If it is positive, the prediction was (on average) better than the median. If it is negative it was worse than the median.

It is based on the log score, with the formula:

$$
\text{Relative score} = \log_2(p) - \log_2(m)
$$

Where $p$ is the prediction being scored and $m$ is the median of all other predictions on that question.

As of late 2023, the Relative score is in the process of being replaced by the [Peer score](https://www.metaculus.com/help/scores-faq/#peer-score), but it is still used for many open tournaments.

### What is the coverage?

The Coverage measures for what proportion of a question's lifetime you had a prediction standing.

If you make your first prediction right when the question opens, your coverage will be 100%. If you make your first prediction one second before the question closes, your coverage will be very close to 0%.

The Coverage is used in tournaments, to incentivize early predictions.

### What are Metaculus points?

Metaculus points were used as the main score on Metaculus until late 2023.

You can still find the rankings based on points [here](https://www.metaculus.com/legacy-points-rankings/).

They are a proper score, based on the log score. They are a mixture of a Baseline-like score and a Peer-like score, so they reward both beating an impartial baseline and beating other forecasters.

For full mathematical details, expand the section below.

### Metaculus points math

Your score $S(T,o)$ at any given time $T$ is the sum of an "absolute" component and a "relative" component:

$$
S(T,o) = a(N) \times L(p,o) + b(N) \times B(p,o)
$$

where:

* $o$ is the outcome of the question: 1 if the question resolves positive, 0 if it resolves negative.
* $N$ is the number of forecasters on the question.
* $L(p,o)$ is the log score relative to a 50% prior, defined as:

$$
L(p, o) =
  \begin{cases}
  \log_2 \left ( \frac{p}{0.5} \right ) & \text{if } o = 1 \\
  \log_2 \left ( \frac{1 - p}{0.5} \right ) & \text{if } o = 0
  \end{cases}
$$

* $B(p,o)$ is the betting score and represents a bet placed against every other forecaster. It is described under "constant pool scoring" on the Metaculus scoring demo (but with a modification that for computational efficiency, the full distribution of other forecaster predictions is replaced by a fitted  [beta distribution](https://en.wikipedia.org/wiki/Beta_distribution)  ).
* $a(N)$ and $b(N)$ depend on $N$ only and define how the points scale with the number of forecasters.

$$
\begin{align*}
  A(N) &= 45 + 15 \log_2(1 + N/30) \\
  B(N) &= 30 \log_2(1 + N/30)
  \end{align*}
$$

Note that $B$, $N$, and $p$ can all depend on $T$ and contribute to the time-dependence of $S(T, o)$.

Your final score is given by the integral of $S(T, o)$ over $T$:

$$
S = \frac{1}{t_c-t_o} \int_{t_o}^{t_c} S(T, o) \, dT
$$

where $t_o$ and $t_c$ are the opening and closing times. (Note that $S(T) = 0$ between the opening time and your first prediction, and is also zero after question resolution but before question close, in the case when a question resolves early.)

Before May 2022, there was also a 50% point bonus given at the time the question closes, but it was discontinued and the points multiplied by 1.5 henceforth.

---

# Tournaments

---

## How are my tournament Score, Take, Prize, and Rank calculated?

This scoring method was introduced in March 2024. It is based on the [Peer scores](https://www.metaculus.com/help/scores-faq/#peer-score) described above.

Your rank in the tournament is determined by the sum of your Peer scores over all questions weighted by the question's weight in the tournament (you get 0 for any question you didn't forecast). Questions that have weights other than 1.0 are indicated in the sidebar of the question detail page. Typically, a question weight is changed if it is determined to be highly correllated with other questions included in the same tournament, especially question groups.

The share of the prize pool you get is proportional to that same sum of Peer scores, squared. If the sum of your Peer scores is negative, you don't get any prize.

$$
\text{your total score} = \sum_\text{questions} \text{your peer score} * \text{question weight}
$$

$$
\text{your take} = \max ( \text{your total score}, 0)^2
$$

$$
\text{your \% prize} = \frac{\text{your take}}{\sum_\text{all users} \text{user take}}
$$

For a tournament with a sufficiently large number of independent questions, this scoring method is essentially  [proper](https://www.metaculus.com/help/scores-faq/#proper-scoring)  . In short, you should predict your true belief on any question.

Taking the square of your Peer scores incentivizes forecasting every question and forecasting early. Don’t forget to **Follow** a tournament to be notified of new questions.

Note: to limit administrative costs, tournaments that end after 1st of June, 2025 no longer give prizes below 50$, and the remaining money is redistributed to forecasters with higher scores. Tournaments that end before 1st of June, 2025 still do not give prizes below 10$.

Forecasting scores are  [noisy](https://www.metaculus.com/notebooks/19335/comparing-two-forecasters-in-an-ideal-world/)  . Being near the top of a leaderboard requires skill, but finishing first rather than second is often largely luck. So tournament leaderboards show a 95% confidence interval for each Rank and, in the advanced view, for each total Score. To compute it, we use  [bootstrapping](https://en.wikipedia.org/wiki/Bootstrapping_(statistics))  : we resample the tournament's questions with replacement thousands of times, recompute everyone's score and rank on each resample, and take the 2.5th to 97.5th percentiles. Entries that are not eligible to rank still show a Rank interval, which tells you where they would have placed had they been eligible.

---

## How are my (legacy) tournament Score, Coverage, Take, Prize, and Rank calculated?

**This scoring method was superseded in March 2024 by the New Tournament Score described above. It is still in use for tournaments that concluded before March 2024 for some tournaments that were in flight then.**

Your tournament Score is the sum of your Relative scores over all questions in the tournament. If, on average, you were better than the Community Prediction, then it will be positive; otherwise, it will be negative.

Your tournament Coverage is the average of your coverage on each question. If you predicted all questions when they opened, your Coverage will be 100%. If you predicted all questions halfway through, or if you predicted half the questions when they opened, your Coverage will be 50%.

Your tournament Take is the exponential of your Score, times your Coverage:

$$
\text{Take} = e^\text{Score} \times \text{Coverage}
$$

Your Prize is how much money you earned on that tournament. It is proportional to your take and is equal to your Take divided by the sum of all competing forecasters' Takes.

Your Rank is simply how high you were in the leaderboard, sorted by Prize.

The higher your Score and Coverage, the higher your Take will be. The higher your Take, the more Prize you'll receive, and the higher your Rank will be.

---

## What are the Hidden Period and Hidden Coverage Weights?

The Community Prediction is on average much better than most forecasters. This means that you could get decent scores by just copying the Community Prediction at all times. To prevent this, many tournament questions have a significant period of time at the beginning when the Community Prediction is hidden. We call this time the Hidden Period.

To incentivize forecasting during the hidden period, questions sometimes are also set up so that the coverage you accrue during the Hidden Period counts more. For example, the Hidden Period could count for 50% of the question coverage, or even 100%. We call this percentage the Hidden Period Coverage Weight.

If the Hidden Period Coverage Weight is 50%, then if you don't forecast during the hidden period your coverage will be at most 50%, regardless of how long the hidden period lasted.

 
