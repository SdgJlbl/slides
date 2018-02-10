Data Science and Ethics

1) Why this talk?
Machine Learning techniques are more and more widely applied, and some of these application domains are increasingly
sensitive. Yet the mechanisms explaining how exactly these algorithms are working is not always thoroughly understood.
Some characteristics inherent to Machine Learning are not always known even by practitioners, and are often overlooked
by decision makers.
The goal of this talk is to present a few of these problematics, that I feel every data scientist should keep in mind.

Focus on current problematics which are already happening day to day, not hypothetical issues (like ethics for
    autonomous car).

More detailed references in the bibliography.

2) ML models versus The World: from research to real life
    In research, you collect data or download a dataset. You learn a model ONCE, evaluate it on a well-known benchmark,
    beat the state-of-the-art results (or not), publish a nice paper / blog article,
    and forget about it and never use it again.
    In real life, you do all that (minus the paper publishing part), THEN you put your model in production. And then,
    it starts to change the real world.
    a) Feedback loops
        -> not limited to ML usage, of course
        -> and tend to strengthen effects (vicious circles and all) : mortage rates
        -> in ML, influence data collection -> asthma story
        -> filter bubbles

    b) How to mitigate that? We need explainability

    c) Factor in massive deployment -> Cathy O'Neil's WMD

3) Data security
    It is not only the responsibility of data scientists, but it is ALSO the responsibility of data scientists.
    https://medium.com/@andrew.therriault/data-security-for-data-scientists-2f1fcd8c261b
    a) General tips on gathering and processing of sensitive data
        i) The only data which will never get stolen is the data you don't have -> need to know basis
        ii) Data encryption
        iii) Delete what is no longer needed
    b) Data anonymization
    Not as easy as just deleting names and addresses...
    https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html

    c) Adversarial attacks on deep learning
    https://blog.xix.ai/how-adversarial-attacks-work-87495b81da2d

4) Bias, bias everywhere
Quote : "there are 3 kinds of lies, small lies, big lies and statistics."
    a) Data is biased
        i) Real world is prejudiced.
        ii) Data collection is a biased process
        Even seemingly simple and straightforward tasks such data plotting is not unbiased by itself.
    https://medium.com/@angebassa/data-alone-isnt-ground-truth-9e733079dfd4

    b) Data scienstists are human, thus biased (cognitive bias)
     -> scientific method

    b) Bias affects global performances, but more specifically minorities
        Video du lave-main qui ne fonctionne pas pour les noirs
        i) Undersampling of "minority" classes
        ii) Subconcepts

    c) Some bias can be corrected if we know what to look for.
    (Bias in word embeddings : https://gist.github.com/rspeer/ef750e7e407e04894cb3b78a82d66aed )
