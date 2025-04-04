# Sweetspot: Optimizing generation for learnability
*Kasper Rasmussen*
*April 2025*

## General idea
llm's are good at editing code and so, but they can lack robustness. my idea is an aversarial game between two BugIntroducer, Fixer. It works like this: We source working code c from the internet, or get a third model Generator to generate some (by checking that it is valid and so). We then generate a test set based on just collecting input output pairs s(c)= (x,y) from the program c. We then have BugIntroducer introduce a little bug, i will actually only be concerned with things that give compiler warnings etc. So then we have buggy code c' ~ bugintroducer(*|c), and warnings w = compiler(c'). We then generated fixed code c'' ~ fixer(*|c') and evaluate it both wrt compiler and input output pairs. It is adversarial in special sense. The goal is not for bugintroducer to create weird code that cannot be fixed, neither code that can easily be fixed. Let p(c',s(c)) be the probabiliy that a c'' ~ fixer(*|c') is a valid fix, where probability is wrt to stochasticity of fixer. Then let learnability z(c',w,c) for fixer of c' is z(c',w)=p(c',c)*(1-p(c',c)). Meaning that if the bugintorducer makes it too difficult for fixer learnability will be low and if it too easy it will be also be low. bugintroducer ideally has to make fixer be able to do fix half of the time - this idea is from a recent paper Learning to Reason at the Frontier of Learnability. but my idea is the code and the adversarial idea for synthetically generating it. So to continue, now make an iterative training procedure. At step k, we generate samples bugintroducerk be trained for maximising learnability wrt to to fixerk

## Programming language framework
Consider some programming language with a compiler.

- Let $\Sigma^*$ be the set of finite strings
- We view a piece of code $c$ as a string $c \in \Sigma^*$.
- Let $\mathcal{W}$ be the space of compiler warnings and errors (we will use the word warnings to always mean warnings and errors) that the compiler can give when building a piece of code.
- We view a program $\phi : \mathcal{T}_1 \to \mathcal{T}_2$ as some function that maps terms of type $\mathcal{T}_1$ to terms of type $\mathcal{T}_2$.
- Let $\Phi$ be the space of programs that the programming language express, and $\Phi' = \Phi \cup \epsilon$ be the union of the programs that it can express and a non-program for the case where the compiler does not build.
- The compiler $\mathcal{C} : \Sigma^* \to \mathcal{W}^* \times \Phi'$ maps a piece of code $c$ to a list of compiler warnings and either the working program $\phi_c$ or in case the code does not compile the non-program $\epsilon$.

Furthermore, for use in our setup we have:

- We say a piece of code $c$ is valid if it compiles with no warnings. The resulting program is $\phi_c : \mathcal{T}^c_1 \to \mathcal{T}^c_2$.
- A test $(i,o) \in \mathcal{T}^c_1 \times \mathcal{T}^c_2$ is valid for $c$ if $\phi_c(i) = o$
- A test sef $\mathcal{S}_c$ for $c$ is a set tests that are valid for $c$.
- We formalize then notion of trying out the test set of some other piece of code: For two codes $c_1$ and $c_2$, where $\mathcal{S}_{c_1}$ is a test set for $c_1$, we say $\mathcal{S}_{c_1}(c_2) : \Sigma^* \to \{0,1\}$ is a function that takes $c_2$, applies the compiler $\phi_{c_2} = \mathcal{C}(c_2)$. If $\phi_{c_2} = \epsilon$ then ${S}_{c_1}(c_2) = 0$. Else if $\phi_{c_2}$ is a valid program, then if $\phi_{c_2}(i_n) = o_n$ for all $(i_n,o_n) \in \mathcal{S}_{c_1}$, then ${S}_{c_1}(c_2) = 1$ else ${S}_{c_1}(c_2) = 0$

## Language model framework
The most common use case of language models is to give it some string in $\Sigma^*$ as input and generate some string as output $\Sigma^*$. This gives us a stochastic policy $\pi(y|x)$, where for an input string $x$ there is some probability of generating an output string $y$. $x$ can either be passed directly to the language model or it can be processed by some program into another string $x'$ that is then passed to a language model or something more complex. Likewise the response from the language model can either be used directly as $y$ or it can be processed by some program that is then used as $y$ or something more complex.

In any case it is coherent to talk of policies $\pi$ that are conditional distributions over sequences.

## Adversarial game framework

Consider a valid code $c$, and an associated test set $\mathcal{S}_c$. We say that $c$ is the "original code".

- The adversary $A(c'|c)$ takes a valid code and produces another piece of code $c'$. Note that it is stochastic.
- The fixer $F(c''|c')$ takes a piece of code $c'$ and produces another piece of code $c''$. Note that it is stochastic.
- Using random variable notation $C' \sim A(\cdot|c)$ is a random code sampled from the adversary, when giving the adversary a fixed input code $c$. We say that $C'$ is the "buggy code".
- Using random variable notation $C'' \sim F(\cdot|c')$ is a random code sampled from the fixer, when giving the fixer a fixed input code $c'$. We say that $C''$ is the "potentially fixed code".
- We now can talk about the probability that the fixer gives a valid fix for the code. The fixer fixes the code if the random potential fix $C''$ passes the test set for $c$. We have $\mathcal{S}_c(C'')$ being an indicator for whether $C''$ sampled from the fixer when given $c'$ as input fixes the code.
- The *performance* $h(c',F,\mathcal{S}_c)$ of a fixer $F$ on a buggy code $c'$ wrt a test set $\mathcal{S}_c$ is the probability that given $c'$ as input, the fixer will generate a fix $C''$ that passes the test set for $c$.

$$
h(c',F,\mathcal{S}_c) = \mathbb{E}_{c'' \sim F(\cdot|c')}[\mathcal{S}_c(c'')]
$$

- The *learnability* $l(c',F,\mathcal{S}_c)$ of a fixer $F$ on a buggy code $c'$ wrt a test set $\mathcal{S}_c$ is

$$
l(c',F,\mathcal{S}_c) = h(c',F,\mathcal{S}_c) (1 - h(c',F,\mathcal{S}_c))
$$ 

## Adversarial game procedure
We will assume a distribution of pairs of codes and associated test sets $p_{data} = p(c, \mathcal{S}_c)$. How to attain such a distribution is an interesting problem in its own right.

### Generation
- The adversary $A_\psi(c'|c)$ is parameterized by an LLM with parameters $\psi$. The fixer $F_\theta(c''|c')$ is parameterized by an LLM with parameters $\theta$.
- Our procedure is iterative with steps $k = 1, ..., K$, where $K$ is a hyperparameter.
- We will start with initial parameters $\psi_0$ and $\theta_0$ and in each iteration use parameters $\psi_k$ and $\theta_k$ to get new parameters $\psi_{k+1}$ and $\theta_{k+1}$.
- So we now start a round with adversary $A_{\psi_k}(c'|c)$ and fixer $F_{\theta_k}(c''|c')$. We sample iid from $p_data$, to get a batch of $N$ pairs of valid codes and test set $(c_n, \mathcal{S}_{c_n})$.
- For each $c_n$ in the batch, we sample $M$ buggy codes $c'_{n,1}, ..., c'_{n,M} \sim A_{\psi{k}}(\cdot|c_n)$ conditionally iid from the current adversary.
- For each buggy code $c'_{n,m}$ we will sample $Q$ potential fixes $c''_{n,m,1}, c''_{n,m,2}, ..., c''_{n,m,Q} \sim F_{\theta_k}(\cdot|c'_{n,m})$ conditionally iid from the current fixer.
- For each buggy code $c'_{n,m}$, we will compute the empirical performance $\hat{h}(c'_{n,m},F_{\theta_k},\mathcal{S}_c)$ as as a Monte Carlo estimate by calculating the fraction of potential fixes $c''_{n,m,q}$ that compile and passe their associated test set $\mathcal{S}_{c_n}$, that is

$$
\hat{h}(c'_{n,m},F_{\theta_k},\mathcal{S}_c) = \frac{1}{Q}\sum_{q=1}^{Q} \mathcal{S}_{c_n}(c''_{n,m,q})
$$

- We will compute the empirical learnability $\hat{l}(c'_{n,m},F_{\theta_k},\mathcal{S}_{c_n})$ for the buggy code $c'_{n,m}$ as

$$
\hat{l}(c'_{n,m},F_{\theta_k},\mathcal{S}_c) = \hat{h}(c'_{n,m},F_{\theta_k},\mathcal{S}_{c_n}) (1 - \hat{h}(c'_{n,m},F_{\theta_k},\mathcal{S}_{c_n}))
$$

### Reward
For each $c_n$ we now have a reward signal for the fixer and the agent.

- For the adversary, given original code $c_n$ as input, the reward for output sequence $c'_{n,m}$ is the empirical learnability $r^A_{n,m} = \hat{l}(c'_{n,m},F_{\theta_k},\mathcal{S}_c)$
- For the fixer, given buggy code $c'_{n,m}$ as input, the reward for the output sequence $c''_{n,m,q}$ is the binary indicator of passing the tests $r^A_{n,m,q} = \mathcal{S}_{c_n}(c''_{n,m,q})$.

### Policy gradient
We can now compute group relative policy gradient for the adversary and the fixer. Let $c'_{n,m,t}$ denote the $t$'th token in the token sequence $c'_{n,m}$ and $|c'_{n,m}|$ denote the number of tokens in the sequence $c'_{n,m}$.w

$$
J^A_{GRPO}(\psi_{k+1}) = \frac{1}{NM}\sum_{n=1}^{N}\sum_{m=1}^{M}\sum_{t=1}^{|c'_{n,m}|} \gamma(t,c'_{n,m},\hat{A}_{n,m,t},
$$

## Experiment 1: CodeContests
- Using the CodeContests, I filtered a bunch of competitive programming problems with instruction, example python solutions $c$, and private and public test cases $\mathcal{S}_c$.
- My first investigation is: Ignoring for now any training, can we even for a start get some level of learnability with available models on this dataset? I will primarily be interested in models for which there exists open weights, such that if anything shows promise, it would be possible to proceed, but will also investigate more generally. I am also interested in smaller models, as they are cheaper to conduct this experiment with and will also be cheaper to investigate training with.
- I set up a prompted adversary parameterized by a string $m_a$ which is the name of the OpenRouter llm one wants to use, giving it instructions on introducing a bug into the code and gave it the competitive programming problem description and example solution $c$. It yields a buggy code $c'$. It will also check that the python code $c'$ is syntactically correct and whether $c'$ already passes the test cases $\mathcal{S}_c$. If it already passes the cases we might consider it equivalent to learnability $0$.
- I set up a prompted fixer, parameterized also by the name $m_f$ of the OpenRouter LLM one wants to use, giving it the competitive programming problem description and the buggy code $c'$, asking it to give a fixed code. It yields code $c''$. I test $c''$ on the test cases.
- Consider first the adversary, it has to generate buggy codes $c'$ and as mentioned they can either be syntactically incorrect or not pass the test suite. If we allow the adversary to output syntactically incorrect codes it makes it hard for us, because we cannot know if it is because there is some other thing than code that we do not want which would give the fixer too much information and bias our estimates and mess up training.
- One obstacle is when the adversary adds comments in the code of $c'$ that indicates where the introduced bug is. This will make it very easy for the fixer. Even if we prompt for this, weak models may fail to follow the instruction. Therefore we remove all comments from code generated.
- Weak models like \texttt{qwen/qwen2.5-vl-3b-instruct:free} seem to have a difficult time as adversary, not making the tests fail when using a senseful prompt. By senseful adversary prompt i mean a prompt explaining the situation that the bug should not be too hard and not too easy to fix.
- For models like Gemma3-27b as adversary and fixer, we get valid buggy codes (syntactically correct and fails tests) but easily fixed.
- One idea might be focus on the objective of what we are doing: We are trying to drive good adversaries and good fixers. There does therefore not necessarily have to be a problem if the interaction between them was more sequential. If the adversary tried to create a buggy code and the fixer easily fixes it we can report back to the adversary that it is too easy for the fixer.