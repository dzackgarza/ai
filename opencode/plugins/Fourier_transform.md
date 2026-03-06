https://en.wikipedia.org/wiki/Fourier_transform

# Fourier transform
Mathematical transform that expresses a function of time as a function of frequency

Not to be confused with [[Fourier method]] or Fourier's original [[sine and cosine transforms]] .

| Fourier transforms | | --- | | - Fourier transform - [[Fourier series]] - [[Discrete-time Fourier transform]] - [[Discrete Fourier transform]] - [[Discrete Fourier transform over a ring]] - [[Fourier transform on finite groups]] - [[Fourier analysis]] - [[Related transforms]] |

[[]]

The Fourier transform applied to the waveform of a [[C major]] [[piano]] [[chord]] (with logarithmic horizontal (frequency) axis). The first three peaks on the left correspond to the [[fundamental frequencies]] of the chord (C, E, G). The remaining smaller peaks are higher-frequency [[overtones]] of the fundamental pitches.

In [[mathematics]] , the **Fourier transform** ( **FT** ) is an [[integral transform]] that takes a [[function]] as input, and outputs another function that describes the extent to which various [[frequencies]] are present in the original function. The output of the transform is a [[complex valued function]] of frequency. The term Fourier transform refers to both the [[mathematical operation]] and to this complex-valued function. When a distinction needs to be made, the output of the operation is sometimes called the [[frequency domain]] representation of the original function. The Fourier transform is analogous to decomposing the [[sound]] of a musical [[chord]] into the [[intensities]] of its constituent [[pitches]] .

[[]]

The Fourier transform relates the time domain, in red, with a function in the domain of the frequency, in blue. The component frequencies, extended for the whole frequency spectrum, are shown as peaks in the domain of the frequency.

Functions that are localized in the time domain have Fourier transforms that are spread out across the frequency domain and vice versa, a phenomenon known as the [uncertainty principle](#Uncertainty_principle) . The [[critical]] case for this principle is the [[Gaussian function]] , of substantial importance in [[probability theory]] and [[statistics]] as well as in the study of physical phenomena exhibiting [[normal distribution]] (e.g., [[diffusion]] ). The Fourier transform of a Gaussian function is another Gaussian function. [[Joseph Fourier]] introduced [[sine and cosine transforms]] (which [[correspond to the imaginary and real components]] of the modern Fourier transform) in his study of [[heat transfer]] , where Gaussian functions appear as solutions of the [[heat equation]] .

The Fourier transform can be formally defined as an [[improper]] [[Riemann integral]] , making it an integral transform, although this definition is not suitable for many applications requiring a more sophisticated integration theory. For example, many relatively simple applications use the [[Dirac delta function]] , which can be treated formally as if it were a function, but the justification requires a mathematically more sophisticated viewpoint.

The Fourier transform can also be generalized to functions of several variables on [[Euclidean space]] , sending a function of 3-dimensional "position space" to a function of 3-dimensional momentum (or a function of space and time to a function of [[4-momentum]] ). This idea makes the spatial Fourier transform very natural in the study of waves, as well as in [[quantum mechanics]] , where it is important to be able to represent wave solutions as functions of either position or momentum and sometimes both. In general, functions to which Fourier methods are applicable are complex-valued, and possibly [[vector-valued]] . Still further generalization is possible to functions on [[groups]] , which, besides the original Fourier transform on [[`R`]] or `Rn` , notably includes the [[discrete-time Fourier transform]] (DTFT, group = `Z` ), the [[discrete Fourier transform]] (DFT, group = [[`Z mod N`]] ) and the [[Fourier series]] or circular Fourier transform (group = [[`S1`]] , the unit circle ≈ closed finite interval with endpoints identified). The latter is routinely employed to handle [[periodic functions]] . The [[fast Fourier transform]] (FFT) is an algorithm for computing the DFT.

## Definition

The Fourier transform of a complex-valued function $f(x)$ on the real line, is the complex valued function ⁠ ${\widehat {f}}(\xi )$ ⁠ , defined by the integral

Fourier transform

| | | | | --- | --- | --- | | ${\widehat {f}}(\xi )=\int _{-\infty }^{\infty }f(x)\ e^{-i2\pi \xi x}\,dx,\quad \forall \xi \in \mathbb {R} .$ | | Eq.1 |

In this case $f(x)$ is (Lebesgue) integrable over the whole real line, i.e., the above integral converges to a continuous function ${\widehat {f}}(\xi )$ at all $\xi$ (decaying to zero as ⁠ $\xi \to \infty$ ⁠ ).

However, the Fourier transform can also be defined for (generalized) functions for which the [[Lebesgue integral]] **[Eq.1](#math_Eq.1)** does not make sense. Interpreting the integral [[suitably]] (e.g. as an [[improper integral]] for [[locally integrable]] functions) extends the Fourier transform to functions that are not necessarily integrable over the whole real line. More generally, the Fourier transform also applies to [[generalized functions]] like the [[Dirac delta]] (and all other [[tempered distributions]] ), in which case it is defined by duality rather than an integral.

First introduced in [[Fourier's]] Analytical Theory of Heat ., the corresponding inversion formula for " [[sufficiently nice]] " functions is given by the [[Fourier inversion theorem]] , i.e.,

Inverse transform

| | | | | --- | --- | --- | | $f(x)=\int _{-\infty }^{\infty }{\widehat {f}}(\xi )\ e^{i2\pi \xi x}\,d\xi ,\quad \forall x\in \mathbb {R} .$ | | Eq.2 |

The functions $f$ and ${\widehat {f}}$ are referred to as a **Fourier transform pair** . A common notation for designating transform pairs is: $f(x)\ {\stackrel {\mathcal {F}}{\longleftrightarrow }}\ {\widehat {f}}(\xi ).$ For example, the Fourier transform of the delta function is the constant function ⁠ $1$ ⁠ : $\delta (x)\ {\stackrel {\mathcal {F}}{\longleftrightarrow }}\ 1.$

### Angular frequency ( ω )

When the independent variable ( ⁠ $x$ ⁠ ) represents time (often denoted by ⁠ $t$ ⁠ ), the transform variable ( ⁠ $\xi$ ⁠ ) represents [[frequency]] (often denoted by ⁠ $f$ ⁠ ). For example, if time has the unit [[second]] , then frequency has the unit [[hertz]] . The transform variable can also be written in terms of [[angular frequency]] , ⁠ $\omega =2\pi \xi$ ⁠ , with the unit [[radian]] per second.

The substitution $\xi ={\tfrac {\omega }{2\pi }}$ into **[Eq.1](#math_Eq.1)** produces this convention, where function ${\widehat {f}}$ is relabeled ⁠ ${\widehat {f}}_{1}$ ⁠ : ${\begin{aligned}{\widehat {f}}_{3}(\omega )&\triangleq \int _{-\infty }^{\infty }f(x)\cdot e^{-i\omega x}\,dx={\widehat {f}}_{1}\left({\tfrac {\omega }{2\pi }}\right),\\f(x)&={\frac {1}{2\pi }}\int _{-\infty }^{\infty }{\widehat {f}}_{3}(\omega )\cdot e^{i\omega x}\,d\omega .\end{aligned}}$ Unlike the **[Eq.1](#math_Eq.1)** definition, the Fourier transform is no longer a [[unitary transformation]] , and there is less symmetry between the formulas for the transform and its inverse. Those properties are restored by splitting the $2\pi$ factor evenly between the transform and its inverse, which leads to another convention: ${\begin{aligned}{\widehat {f}}_{2}(\omega )&\triangleq {\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{\infty }f(x)\cdot e^{-i\omega x}\,dx={\frac {1}{\sqrt {2\pi }}}\ \ {\widehat {f}}_{1}\left({\tfrac {\omega }{2\pi }}\right),\\f(x)&={\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{\infty }{\widehat {f}}_{2}(\omega )\cdot e^{i\omega x}\,d\omega .\end{aligned}}$ Variations of all three conventions can be created by conjugating the complex-exponential [[kernel]] of both the forward and the reverse transform. The signs must be opposites.

Summary of popular forms of the Fourier transform, one-dimensional

| | | | | --- | --- | --- | | ordinary frequency `ξ` (Hz) | unitary | ${\begin{aligned}{\widehat {f}}_{1}(\xi )\ &\triangleq \ \int _{-\infty }^{\infty }f(x)\,e^{-i2\pi \xi x}\,dx={\sqrt {2\pi }}\ \ {\widehat {f}}_{2}(2\pi \xi )={\widehat {f}}_{3}(2\pi \xi )\\f(x)&=\int _{-\infty }^{\infty }{\widehat {f}}_{1}(\xi )\,e^{i2\pi x\xi }\,d\xi \end{aligned}}$ | | angular frequency `ω` (rad/s) | unitary | ${\begin{aligned}{\widehat {f}}_{2}(\omega )\ &\triangleq \ {\frac {1}{\sqrt {2\pi }}}\ \int _{-\infty }^{\infty }f(x)\,e^{-i\omega x}\,dx={\frac {1}{\sqrt {2\pi }}}\ \ {\widehat {f}}_{1}\!\left({\frac {\omega }{2\pi }}\right)={\frac {1}{\sqrt {2\pi }}}\ \ {\widehat {f}}_{3}(\omega )\\f(x)&={\frac {1}{\sqrt {2\pi }}}\ \int _{-\infty }^{\infty }{\widehat {f}}_{2}(\omega )\,e^{i\omega x}\,d\omega \end{aligned}}$ | | non-unitary | ${\begin{aligned}{\widehat {f}}_{3}(\omega )\ &\triangleq \ \int _{-\infty }^{\infty }f(x)\,e^{-i\omega x}\,dx={\widehat {f}}_{1}\left({\frac {\omega }{2\pi }}\right)={\sqrt {2\pi }}\ \ {\widehat {f}}_{2}(\omega )\\f(x)&={\frac {1}{2\pi }}\int _{-\infty }^{\infty }{\widehat {f}}_{3}(\omega )\,e^{i\omega x}\,d\omega \end{aligned}}$ |

Generalization for `n` -dimensional functions

| | | | | --- | --- | --- | | ordinary frequency `ξ` (Hz) | unitary | ${\begin{aligned}{\widehat {f}}_{1}(\xi )\ &\triangleq \ \int _{\mathbb {R} ^{n}}f(x)e^{-i2\pi \xi \cdot x}\,dx=(2\pi )^{\frac {n}{2}}{\widehat {f}}_{2}(2\pi \xi )={\widehat {f}}_{3}(2\pi \xi )\\f(x)&=\int _{\mathbb {R} ^{n}}{\widehat {f}}_{1}(\xi )e^{i2\pi \xi \cdot x}\,d\xi \end{aligned}}$ | | angular frequency `ω` (rad/s) | unitary | ${\begin{aligned}{\widehat {f}}_{2}(\omega )\ &\triangleq \ {\frac {1}{(2\pi )^{\frac {n}{2}}}}\int _{\mathbb {R} ^{n}}f(x)e^{-i\omega \cdot x}\,dx={\frac {1}{(2\pi )^{\frac {n}{2}}}}{\widehat {f}}_{1}\!\left({\frac {\omega }{2\pi }}\right)={\frac {1}{(2\pi )^{\frac {n}{2}}}}{\widehat {f}}_{3}(\omega )\\f(x)&={\frac {1}{(2\pi )^{\frac {n}{2}}}}\int _{\mathbb {R} ^{n}}{\widehat {f}}_{2}(\omega )e^{i\omega \cdot x}\,d\omega \end{aligned}}$ | | non-unitary | ${\begin{aligned}{\widehat {f}}_{3}(\omega )\ &\triangleq \ \int _{\mathbb {R} ^{n}}f(x)e^{-i\omega \cdot x}\,dx={\widehat {f}}_{1}\left({\frac {\omega }{2\pi }}\right)=(2\pi )^{\frac {n}{2}}{\widehat {f}}_{2}(\omega )\\f(x)&={\frac {1}{(2\pi )^{n}}}\int _{\mathbb {R} ^{n}}{\widehat {f}}_{3}(\omega )e^{i\omega \cdot x}\,d\omega \end{aligned}}$ |

### Lebesgue integrable functions

See also: [[Lp space § Lp spaces and Lebesgue integrals]]

A [[measurable function]] $f:\mathbb {R} \to \mathbb {C}$ is called (Lebesgue) integrable if the [[Lebesgue integral]] of its [[absolute value]] is finite: $\|f\|_{1}=\int _{\mathbb {R} }|f(x)|\,dx<\infty .$ If $f$ is Lebesgue integrable then the Fourier transform, given by **[Eq.1](#math_Eq.1)** , is well-defined for all ⁠ $\xi \in \mathbb {R}$ ⁠ . Furthermore, ${\widehat {f}}\in L^{\infty }\cap C_{0}(\mathbb {R} )$ is bounded, [[uniformly continuous]] and (by the [[Riemann–Lebesgue lemma]] ) [[vanishing at infinity]] . Here $C_{0}(\mathbb {R} )$ denotes the space of continuous functions on $\mathbb {R}$ that approach 0 as x approaches positive or negative infinity.

The space $L^{1}(\mathbb {R} )$ is the space of measurable functions for which the norm $\|f\|_{1}$ is finite, modulo the [[equivalence relation]] of equality [[almost everywhere]] . The Fourier transform on $L^{1}(\mathbb {R} )$ is [[one-to-one]] . However, there is no easy characterization of the image, and thus no easy characterization of the inverse transform. In particular, **[Eq.2](#math_Eq.2)** is no longer valid, as it was stated only under the hypothesis that $f(x)$ was "sufficiently nice" (e.g., $f(x)$ [[decays with all derivatives]] ).

While **[Eq.1](#math_Eq.1)** defines the Fourier transform for (complex-valued) functions in ⁠ $L^{1}(\mathbb {R} )$ ⁠ , it is not well-defined for other integrability classes, most importantly the space of [[square-integrable functions]] ⁠ $L^{2}(\mathbb {R} )$ ⁠ . For example, the function $f(x)=(1+x^{2})^{-1/2}$ is in $L^{2}$ but not $L^{1}$ and therefore the Lebesgue integral **[Eq.1](#math_Eq.1)** does not exist. However, the Fourier transform on the dense subspace $L^{1}\cap L^{2}(\mathbb {R} )\subset L^{2}(\mathbb {R} )$ admits a unique continuous extension to a [[unitary operator]] on ⁠ $L^{2}(\mathbb {R} )$ ⁠ . This extension is important in part because, unlike the case of ⁠ $L^{1}$ ⁠ , the Fourier transform is an [[automorphism]] of the space ⁠ $L^{2}(\mathbb {R} )$ ⁠ .

In such cases, the Fourier transform can be obtained explicitly by [[regularizing]] the integral, and then passing to a limit. In practice, the integral is often regarded as an [[improper integral]] instead of a proper Lebesgue integral, but sometimes for convergence one needs to use [[weak limit]] or [[principal value]] instead of the (pointwise) limits implicit in an improper integral. [Titchmarsh (1986)](#CITEREFTitchmarsh1986) and [Dym & McKean (1985)](#CITEREFDymMcKean1985) each gives three rigorous ways of extending the Fourier transform to square integrable functions using this procedure. A general principle in working with the $L^{2}$ Fourier transform is that Gaussians are dense in ⁠ $L^{1}\cap L^{2}$ ⁠ , and the various features of the Fourier transform, such as its unitarity, are easily inferred for Gaussians. Many of the properties of the Fourier transform can then be proven from two facts about Gaussians:

- that $e^{-\pi x^{2}}$ is its own Fourier transform; and - that the [[Gaussian integral]] ⁠ $\textstyle \int _{-\infty }^{\infty }e^{-\pi x^{2}}\,dx=1$ ⁠ .

A feature of the $L^{1}$ Fourier transform is that it is a homomorphism of Banach algebras from $L^{1}$ equipped with the convolution operation to the Banach algebra of continuous functions under the $L^{\infty }$ (supremum) norm. The conventions chosen in this article are those of [[harmonic analysis]] , and are characterized as the unique conventions such that the Fourier transform is both [[unitary]] on ⁠ $L^{2}$ ⁠ and an algebra homomorphism from ⁠ ${1}$ ⁠ to ⁠ $L^{\infty }$ ⁠ , without renormalizing the Lebesgue measure.

## Background

### History

Main articles: [[Fourier analysis § History]] , and [[Fourier series § History]]

In 1822, Fourier claimed (see Joseph Fourier § The Analytic Theory of Heat ) that any function, whether continuous or discontinuous, can be expanded into a series of sines. That important work was corrected and expanded upon by others to provide the foundation for the various forms of the Fourier transform used since.

### Complex sinusoids

[[]]

[[]]

The red [[sinusoid]] can be described by peak amplitude (1), peak-to-peak (2), [[RMS]] (3), and [[wavelength]] (4). The red and blue sinusoids have a phase difference of `θ` .

In general, the coefficients ${\widehat {f}}(\xi )$ are complex numbers, which have two equivalent forms (see Euler's formula ): ${\widehat {f}}(\xi )=\underbrace {Ae^{i\theta }} _{\text{polar coordinate form}}=\underbrace {A\cos(\theta )+iA\sin(\theta )} _{\text{rectangular coordinate form}}.$

The product with $e^{i2\pi \xi x}$ ( **[Eq.2](#math_Eq.2)** ) has these forms: ${\begin{aligned}{\widehat {f}}(\xi )\cdot e^{i2\pi \xi x}&=Ae^{i\theta }\cdot e^{i2\pi \xi x}\\[6pt]&=\underbrace {Ae^{i(2\pi \xi x+\theta )}} _{\text{polar coordinate form}}\\[6pt]&=\underbrace {A\cos(2\pi \xi x+\theta )+iA\sin(2\pi \xi x+\theta )} _{\text{rectangular coordinate form}},\end{aligned}}$ which conveys both [[amplitude]] and [[phase]] of frequency ⁠ $\xi$ ⁠ . Likewise, the intuitive interpretation of **[Eq.1](#math_Eq.1)** is that multiplying $f(x)$ by $e^{-i2\pi \xi x}$ has the effect of subtracting $\xi$ from every frequency component of function ⁠ $f(x)$ ⁠ . Only the component that was at frequency $\xi$ can produce a non-zero value of the infinite integral, because (at least formally) all the other shifted components are oscillatory and integrate to zero (see § Example ).

It is noteworthy how easily the product was simplified using the polar form, and how easily the rectangular form was deduced by an application of Euler's formula.

### Negative frequency

See also: [[Negative frequency § Simplifying the Fourier transform]]

Euler's formula introduces the possibility of negative ⁠ $\xi$ ⁠ . **[Eq.1](#math_Eq.1)** is defined ⁠ $\forall \xi \in \mathbb {R}$ ⁠ . Only certain complex-valued $f(x)$ have transforms ⁠ ${\widehat {f}}=0,\ \forall \ \xi <0$ ⁠ . (See Analytic signal ; a simple example is ⁠ $e^{i2\pi \xi _{0}x}\ (\xi _{0}>0)$ ⁠ .)  But negative frequency is necessary to characterize all other complex-valued ⁠ $f(x)$ ⁠ , found in [[signal processing]] , [[partial differential equations]] , [[radar]] , [[nonlinear optics]] , [[quantum mechanics]] , and others.

For a real-valued ⁠ $f(x)$ ⁠ , **[Eq.1](#math_Eq.1)** has the symmetry property ${\widehat {f}}(-\xi )={\widehat {f}}^{\*}(\xi )$ (see § Conjugation below). This redundancy enables **[Eq.2](#math_Eq.2)** to distinguish $f(x)=\cos(2\pi \xi _{0}x)$ from ⁠ $e^{i2\pi \xi _{0}x}$ ⁠ . But it cannot determine the actual sign of ⁠ $\xi _{0}$ ⁠ , because $\cos(2\pi \xi _{0}x)$ and $\cos(2\pi (-\xi _{0})x)$ are indistinguishable on just the real numbers line.

### Fourier transform for periodic functions

The Fourier transform of a periodic function cannot be defined using the integral formula directly. In order for integral in **[Eq.1](#math_Eq.1)** to be defined the function must be [[absolutely integrable]] . Instead it is common to use [[Fourier series]] . It is possible to extend the definition to include periodic functions by viewing them as [[tempered distributions]] .

This makes it possible to see a connection between the [[Fourier series]] and the Fourier transform for periodic functions that have a [[convergent Fourier series]] . If $f(x)$ is a [[periodic function]] , with period ⁠ $P$ ⁠ , that has a convergent Fourier series, then: ${\widehat {f}}(\xi )=\sum _{n=-\infty }^{\infty }c_{n}\cdot \delta \left(\xi -{\tfrac {n}{P}}\right),$ where $c_{n}$ are the Fourier series coefficients of ⁠ $f$ ⁠ , and $\delta$ is the [[Dirac delta function]] . In other words, the Fourier transform is a [[Dirac comb]] function whose teeth are multiplied by the Fourier series coefficients.

### Sampling the Fourier transform

For broader coverage of this topic, see [[Poisson summation formula]] .

The Fourier transform of an [[integrable]] function $f$ can be sampled at regular intervals of arbitrary length ⁠ $1/P$ ⁠ . These samples can be deduced from one cycle of a periodic function ⁠ $f_{P}$ ⁠ , which has [[Fourier series]] coefficients proportional to those samples by the [[Poisson summation formula]] : $f_{P}(x)\triangleq \sum _{n=-\infty }^{\infty }f(x+nP)={\frac {1}{P}}\sum _{k=-\infty }^{\infty }{\widehat {f}}\left({\tfrac {k}{P}}\right)e^{i2\pi {\frac {k}{P}}x},\quad \forall k\in \mathbb {Z} .$

The integrability of $f$ ensures the [[periodic summation]] converges. Therefore, the samples ${\widehat {f}}({\tfrac {k}{P}})$ can be determined by Fourier series analysis: ${\widehat {f}}\left({\tfrac {k}{P}}\right)=\int _{P}f_{P}(x)\cdot e^{-i2\pi {\frac {k}{P}}x}\,dx.$

When $f(x)$ has [[compact support]] , $f_{P}(x)$ has a finite number of terms within the interval of integration. When $f(x)$ does not have compact support, numerical evaluation of $f_{P}(x)$ requires an approximation, such as tapering $f(x)$ or truncating the number of terms.

## Units

See also: [[Spectral density § Units]]

The frequency variable must have inverse units to the units of the original function's domain (typically named $t$ or ⁠ $x$ ⁠ ). For example, if $t$ is measured in seconds, $\xi$ should be in cycles per second or [[hertz]] . If the scale of time is in units of $2\pi$ seconds, then another Greek letter $\omega$ is typically used instead to represent [[angular frequency]] (where ⁠ $\omega =2\pi \xi$ ⁠ ) in units of [[radians]] per second. If using $x$ for units of length, then $\xi$ must be in inverse length, e.g., [[wavenumbers]] . That is to say, there are two versions of the real line: one that is the [[range]] of $t$ and measured in units of ⁠ $t$ ⁠ , and the other that is the range of $\xi$ and measured in inverse units to the units of ⁠ $t$ ⁠ . These two distinct versions of the real line cannot be equated with each other. Therefore, the Fourier transform goes from one space of functions to a different space of functions: functions that have a different domain of definition.

In general, $\xi$ must always be taken to be a [[linear form]] on the space of its domain, which is to say that the second real line is the [[dual space]] of the first real line. See the article Linear algebra for a more formal explanation and for more details. This point of view becomes essential in generalizations of the Fourier transform to general [[symmetry groups]] , including the case of Fourier series.

That there is no one preferred way (often, one says "no canonical way") to compare the two versions of the real line that are involved in the Fourier transform—fixing the units on one line does not force the scale of the units on the other line—is the reason for the plethora of rival conventions on the definition of the Fourier transform. The various definitions resulting from different choices of units differ by various constants.

In other conventions, the Fourier transform has `i` in the exponent instead of `−i` , and vice versa for the inversion formula. This convention is common in modern physics and is the default for [Wolfram Alpha](https://www.wolframalpha.com) , and does not mean that the frequency has become negative, since there is no canonical definition of positivity for frequency of a complex wave. It simply means that ${\widehat {f}}(\xi )$ is the amplitude of the wave ⁠ $e^{-i2\pi \xi x}$ ⁠ instead of the wave $e^{i2\pi \xi x}$ (the former, with its minus sign, is often seen in the time dependence for [[sinusoidal plane-wave solutions of the electromagnetic wave equation]] , or in the [[time dependence for quantum wave functions]] ). Many of the identities involving the Fourier transform remain valid in those conventions, provided all terms that explicitly involve `i` have it replaced by `−i` . In [[electrical engineering]] the letter `j` is typically used for the [[imaginary unit]] instead of `i` because `i` is used for current.

When using [[dimensionless units]] , the constant factors might not be written in the transform definition. For instance, in [[probability theory]] , the characteristic function `Φ` of the probability density function ⁠ $f$ ⁠ of a random variable ⁠ $X$ ⁠ of continuous type is defined without a negative sign in the exponential, and since the units of ⁠ $x$ ⁠ are ignored, there is no ⁠ $2\pi$ ⁠ either: $\varphi (\lambda )=\int _{-\infty }^{\infty }f(x)e^{i\lambda x}\,dx.$

In probability theory and mathematical statistics, the use of the Fourier—Stieltjes transform is preferred, because many random variables are not of continuous type, and do not possess a density function, and one must treat not functions but [[distributions]] , i.e., measures that possess "atoms".

From the higher point of view of [[group characters]] , which is much more abstract, all these arbitrary choices disappear, as will be explained in the later section of this article, which treats the notion of the Fourier transform of a function on a [[locally compact abelian group]] .

## Properties

Let $f(x)$ and $h(x)$ represent integrable functions [[Lebesgue-measurable]] on the real line satisfying: $\int _{-\infty }^{\infty }|f(x)|\,dx<\infty .$ We denote the Fourier transforms of these functions as ${\widehat {f}}(\xi )$ and ${\widehat {h}}(\xi )$ respectively.

### Basic properties

The Fourier transform has the following basic properties:

#### Linearity

$a\ f(x)+b\ h(x)\ \ {\stackrel {\mathcal {F}}{\Longleftrightarrow }}\ \ a\ {\widehat {f}}(\xi )+b\ {\widehat {h}}(\xi );\quad \ a,b\in \mathbb {C}$

#### Time shifting

$f(x-x_{0})\ \ {\stackrel {\mathcal {F}}{\Longleftrightarrow }}\ \ e^{-i2\pi x_{0}\xi }\ {\widehat {f}}(\xi );\quad \ x_{0}\in \mathbb {R}$

#### Frequency shifting

$e^{i2\pi \xi _{0}x}f(x)\ \ {\stackrel {\mathcal {F}}{\Longleftrightarrow }}\ \ {\widehat {f}}(\xi -\xi _{0});\quad \ \xi _{0}\in \mathbb {R}$

#### Time scaling

$f(ax)\ \ {\stackrel {\mathcal {F}}{\Longleftrightarrow }}\ \ {\frac {1}{|a|}}{\widehat {f}}\left({\frac {\xi }{a}}\right);\quad \ a\neq 0$ The case $a=-1$ leads to the time-reversal property : $f(-x)\ \ {\stackrel {\mathcal {F}}{\Longleftrightarrow }}\ \ {\widehat {f}}(-\xi )$

[[]]

$\scriptstyle f(t)$

$\scriptstyle {\widehat {f}}(\omega )$

$\scriptstyle g(t)$

$\scriptstyle {\widehat {g}}(\omega )$

$\scriptstyle t$

$\scriptstyle \omega$

$\scriptstyle t$

$\scriptstyle \omega$

[[]]

[[ ]]

The transform of an even-symmetric real-valued function ⁠ $f(t)=f_{_{\text{RE}}}$ ⁠ is also an even-symmetric real-valued function ( ⁠ ${\widehat {f}}\!_{_{\text{RE}}}$ ⁠ ). The time-shift, ⁠ $g(t)=g_{_{\text{RE}}}+g_{_{\text{RO}}}$ ⁠ , creates an imaginary component, ⁠ $i\ {\widehat {g\ \!}}_{_{\text{IO}}}$ ⁠ . (See § Symmetry .)

#### Symmetry

When the real and imaginary parts of a complex function are decomposed into their [[even and odd parts]] , there are four components, denoted below by the subscripts RE, RO, IE, and IO. And there is a one-to-one mapping between the four components of a complex time function and the four components of its complex frequency transform:

: ${\begin{array}{rlcccccccc}{\mathsf {Time\ domain}}&f&=&f_{_{\text{RE}}}&+&f_{_{\text{RO}}}&+&i\ f_{_{\text{IE}}}&+&\underbrace {i\ f_{_{\text{IO}}}} \\&{\Bigg \Updownarrow }{\mathcal {F}}&&{\Bigg \Updownarrow }{\mathcal {F}}&&\ \ {\Bigg \Updownarrow }{\mathcal {F}}&&\ \ {\Bigg \Updownarrow }{\mathcal {F}}&&\ \ {\Bigg \Updownarrow }{\mathcal {F}}\\{\mathsf {Frequency\ domain}}&{\widehat {f}}&=&{\widehat {f}}\!_{_{\text{RE}}}&+&\overbrace {i\ {\widehat {f}}\!_{_{\text{IO}}}} &+&i\ {\widehat {f}}\!_{_{\text{IE}}}&+&{\widehat {f}}\!_{_{\text{RO}}}\end{array}}$

From this, various relationships are apparent, for example:

- The transform of a real-valued function ( ⁠ $f_{_{\text{RE}}}+f_{_{\text{RO}}}$ ⁠ ) is the conjugate symmetric function ⁠ ${\widehat {f}}\!_{_{\text{RE}}}+i\ {\widehat {f}}\!_{_{\text{IO}}}$ ⁠ . Conversely, a conjugate symmetric transform implies a real-valued time-domain. - The transform of an imaginary-valued function ( ⁠ $i\ f_{_{\text{IE}}}+i\ f_{_{\text{IO}}}$ ⁠ ) is the conjugate antisymmetric function ⁠ ${\widehat {f}}\!_{_{\text{RO}}}+i\ {\widehat {f}}\!_{_{\text{IE}}}$ ⁠ , and the converse is true. - The transform of a conjugate symmetric function $(f_{_{\text{RE}}}+i\ f_{_{\text{IO}}})$ is the real-valued function ⁠ ${\widehat {f}}\!_{_{\text{RE}}}+{\widehat {f}}\!_{_{\text{RO}}}$ ⁠ , and the converse is true. - The transform of a conjugate antisymmetric function $(f_{_{\text{RO}}}+i\ f_{_{\text{IE}}})$ is the imaginary-valued function ⁠ $i\ {\widehat {f}}\!_{_{\text{IE}}}+i\ {\widehat {f}}\!_{_{\text{IO}}}$ ⁠ , and the converse is true.

#### Conjugation

${\bigl (}f(x){\bigr )}^{\*}\ \ {\stackrel {\mathcal {F}}{\Longleftrightarrow }}\ \ \left({\widehat {f}}(-\xi )\right)^{\*}$ (Note: the ⁠ $\*$ ⁠ denotes [[complex conjugation]] .)

In particular, if $f$ is real , then ${\widehat {f}}$ is [[conjugate symmetric]] ( a.k.a. [[Hermitian function]] ): ${\widehat {f}}(-\xi )={\bigl (}{\widehat {f}}(\xi ){\bigr )}^{\*}.$

If $f$ is purely imaginary, then ${\widehat {f}}$ is [[odd symmetric]] : ${\widehat {f}}(-\xi )=-({\widehat {f}}(\xi ))^{\*}.$

#### Real and imaginary parts

$\operatorname {Re} \{f(x)\}\ \ {\stackrel {\mathcal {F}}{\Longleftrightarrow }}\ \ {\tfrac {1}{2}}\left({\widehat {f}}(\xi )+{\bigl (}{\widehat {f}}(-\xi ){\bigr )}^{\*}\right)$ $\operatorname {Im} \{f(x)\}\ \ {\stackrel {\mathcal {F}}{\Longleftrightarrow }}\ \ {\tfrac {1}{2i}}\left({\widehat {f}}(\xi )-{\bigl (}{\widehat {f}}(-\xi ){\bigr )}^{\*}\right)$

#### Zero frequency component

Substituting $\xi =0$ in the definition, we obtain: ${\widehat {f}}(0)=\int _{-\infty }^{\infty }f(x)\,dx.$

The integral of $f$ over its domain is known as the average value or [[DC bias]] of the function.

### Uniform continuity and the Riemann–Lebesgue lemma

[[]]

The [[rectangular function]] is [[Lebesgue integrable]] .

[[]]

The [[sinc function]] , which is the Fourier transform of the rectangular function, is bounded and continuous, but not Lebesgue integrable.

The Fourier transform may be defined in some cases for non-integrable functions, but the Fourier transforms of integrable functions have several strong properties.

The Fourier transform ${\widehat {f}}$ of any integrable function $f$ is [[uniformly continuous]] and $\left\|{\widehat {f}}\right\|_{\infty }\leq \left\|f\right\|_{1}$

By the Riemann–Lebesgue lemma , ${\widehat {f}}(\xi )\to 0{\text{ as }}|\xi |\to \infty .$

However, ${\widehat {f}}$ need not be integrable. For example, the Fourier transform of the [[rectangular function]] , which is integrable, is the [[sinc function]] , which is not [[Lebesgue integrable]] , because its [[improper integrals]] behave analogously to the [[alternating harmonic series]] , in converging to a sum without being [[absolutely convergent]] .

It is not generally possible to write the inverse transform as a [[Lebesgue integral]] . However, when both $f$ and ${\widehat {f}}$ are integrable, the inverse equality $f(x)=\int _{-\infty }^{\infty }{\widehat {f}}(\xi )e^{i2\pi x\xi }\,d\xi$ holds for almost every `x` . As a result, the Fourier transform is [[injective]] on [[`L1(R)`]] .

### Plancherel theorem and Parseval's theorem

Main articles: [[Plancherel theorem]] and [[Parseval's theorem]]

Let ⁠ $f(x)$ ⁠ and ⁠ $g(x)$ ⁠ be integrable, and let ⁠ ${\widehat {f}}$ ⁠ and ⁠ ${\widehat {g}}$ ⁠ be their Fourier transforms. If ⁠ $f(x)$ ⁠ and ⁠ $g(x)$ ⁠ are also [[square-integrable]] , then the Parseval formula follows: $\langle f,g\rangle _{L^{2}}=\int _{-\infty }^{\infty }f(x){\overline {g(x)}}\,dx=\int _{-\infty }^{\infty }{\widehat {f}}(\xi ){\overline {{\widehat {g}}(\xi )}}\,d\xi ,$ where the bar denotes [[complex conjugation]] .

The [[Plancherel theorem]] , which follows from the above, states that $\|f\|_{L^{2}}^{2}=\int _{-\infty }^{\infty }\left|f(x)\right|^{2}\,dx=\int _{-\infty }^{\infty }\left|{\widehat {f}}(\xi )\right|^{2}\,d\xi .$

Plancherel's theorem makes it possible to extend the Fourier transform, by a continuity argument, to a [[unitary operator]] on ⁠ $L^{2}(\mathbb {R} )$ ⁠ . On ⁠ $L^{1}(\mathbb {R} )\cap L^{2}(\mathbb {R} )$ ⁠ , this extension agrees with original Fourier transform defined on ⁠ $L^{1}(\mathbb {R} )$ ⁠ , thus enlarging the domain of the Fourier transform to ⁠ $L^{1}(\mathbb {R} )+L^{2}(\mathbb {R} )$ ⁠ (and consequently to ⁠ $L^{p}(\mathbb {R} )$ ⁠ for ⁠ $1\leq p\leq 2$ ⁠ ). Plancherel's theorem has the interpretation in the sciences that the Fourier transform preserves the [[energy]] of the original quantity. The terminology of these formulas is not quite standardised. [[Parseval's theorem]] was proved only for Fourier series, and was first proved by Lyapunov. But Parseval's formula makes sense for the Fourier transform as well, and so even though in the context of the Fourier transform it was proved by Plancherel, it is still often referred to as Parseval's formula, or Parseval's relation, or even Parseval's theorem.

See Pontryagin duality for a general formulation of this concept in the context of locally compact abelian groups.

### Convolution theorem

Main article: [[Convolution theorem]]

The Fourier transform translates between [[convolution]] and multiplication of functions. If ⁠ $f(x)$ ⁠ and ⁠ $g(x)$ ⁠ are integrable functions with Fourier transforms ⁠ ${\widehat {f}}$ ⁠ and ⁠ ${\widehat {g}}(\xi )$ ⁠ respectively, then the Fourier transform of the convolution is given by the product of the Fourier transforms ⁠ ${\widehat {f}}$ ⁠ and ⁠ ${\widehat {g}}$ ⁠ (under other conventions for the definition of the Fourier transform a constant factor may appear).

This means that if: $h(x)=(f\*g)(x)=\int _{-\infty }^{\infty }f(y)g(x-y)\,dy,$ where `∗` denotes the convolution operation, then: ${\widehat {h}}(\xi )={\widehat {f}}(\xi )\,{\widehat {g}}(\xi ).$

In [[linear time invariant (LTI) system theory]] , it is common to interpret ⁠ $g(x)$ ⁠ as the [[impulse response]] of an LTI system with input ⁠ $f(x)$ ⁠ and output ⁠ $h(x)$ ⁠ , since substituting the [[unit impulse]] for ⁠ $f(x)$ ⁠ yields ⁠ $h(x)=g(x)$ ⁠ . In this case, ⁠ ${\widehat {g}}(\xi )$ ⁠ represents the [[frequency response]] of the system.

Conversely, if ⁠ $f(x)$ ⁠ can be decomposed as the product of two square integrable functions ⁠ $p(x)$ ⁠ and ⁠ $q(x)$ ⁠ , then the Fourier transform of ⁠ $f(x)$ ⁠ is given by the convolution of the respective Fourier transforms ⁠ ${\widehat {p}}(\xi )$ ⁠ and ⁠ ${\widehat {q}}(\xi )$ ⁠ .

### Cross-correlation theorem

Main articles: [[Cross-correlation]] and [[Wiener–Khinchin theorem]]

In an analogous manner, it can be shown that if ⁠ $h(x)$ ⁠ is the [[cross-correlation]] of ⁠ $f(x)$ ⁠ and ⁠ $g(x)$ ⁠ : $h(x)=(f\star g)(x)=\int _{-\infty }^{\infty }{\overline {f(y)}}g(x+y)\,dy$ then the Fourier transform of ⁠ $h(x)$ ⁠ is: ${\widehat {h}}(\xi )={\overline {{\widehat {f}}(\xi )}}\,{\widehat {g}}(\xi ).$

As a special case, the [[autocorrelation]] of function ⁠ $f(x)$ ⁠ is: $h(x)=(f\star f)(x)=\int _{-\infty }^{\infty }{\overline {f(y)}}f(x+y)\,dy$ for which ${\widehat {h}}(\xi )={\overline {{\widehat {f}}(\xi )}}{\widehat {f}}(\xi )=\left|{\widehat {f}}(\xi )\right|^{2}.$

### Differentiation

Suppose `f(x)` is differentiable [[almost everywhere]] , and both ⁠ $f$ ⁠ and its derivative ⁠ $f'$ ⁠ are integrable (in ⁠ $L^{1}(\mathbb {R} )$ ⁠ ). Then the Fourier transform of the derivative is given by ${\widehat {f'}}(\xi )={\mathcal {F}}\left\{{\frac {d}{dx}}f(x)\right\}=i2\pi \xi {\widehat {f}}(\xi ).$ More generally, the Fourier transformation of the ⁠ $n$ ⁠ th derivative ⁠ $f^{(n)}$ ⁠ is given by ${\widehat {f^{(n)}}}(\xi )={\mathcal {F}}\left\{{\frac {d^{n}}{dx^{n}}}f(x)\right\}=(i2\pi \xi )^{n}{\widehat {f}}(\xi ).$

Analogously, ⁠ ${\mathcal {F}}\left\{{\frac {d^{n}}{d\xi ^{n}}}{\widehat {f}}(\xi )\right\}=(i2\pi x)^{n}f(x)$ ⁠ , so ⁠ ${\mathcal {F}}\left\{x^{n}f(x)\right\}=\left({\frac {i}{2\pi }}\right)^{n}{\frac {d^{n}}{d\xi ^{n}}}{\widehat {f}}(\xi )$ ⁠ .

By applying the Fourier transform and using these formulas, some [[ordinary differential equations]] can be transformed into algebraic equations, which are much easier to solve. These formulas also give rise to the [[rule of thumb]] " ⁠ $f(x)$ ⁠ is smooth [[if and only if]] ⁠ ${\widehat {f}}(\xi )$ ⁠ quickly falls to ⁠ $0$ ⁠ for ⁠ $\vert \xi \vert \to \infty$ ⁠ ". By using the analogous rules for the inverse Fourier transform, one can also say " ⁠ $f(x)$ ⁠ quickly falls to ⁠ $0$ ⁠ for ⁠ $\vert x\vert \to \infty$ ⁠ if and only if ⁠ ${\widehat {f}}(\xi )$ ⁠ is smooth."

### Eigenfunctions

See also: [[Mehler kernel]] and [[Hermite polynomials § Hermite functions as eigenfunctions of the Fourier transform]]

The Fourier transform is a linear transform that has [[eigenfunctions]] obeying ⁠ ${\mathcal {F}}[\psi ]=\lambda \psi$ ⁠ , with ⁠ $\lambda \in \mathbb {C}$ ⁠ .

A set of eigenfunctions is found by noting that the homogeneous differential equation $\left[U\left({\frac {1}{2\pi }}{\frac {d}{dx}}\right)+U(x)\right]\psi (x)=0$ leads to eigenfunctions $\psi (x)$ of the Fourier transform ${\mathcal {F}}$ as long as the form of the equation remains invariant under Fourier transform. In other words, every solution $\psi (x)$ and its Fourier transform ${\widehat {\psi }}(\xi )$ obey the same equation. Assuming [[uniqueness]] of the solutions, every solution $\psi (x)$ must therefore be an eigenfunction of the Fourier transform. The form of the equation remains unchanged under Fourier transform if $U(x)$ can be expanded in a power series in which for all terms the same factor of either one of ⁠ $\pm 1$ ⁠ , ⁠ $\pm i$ ⁠ arises from the factors $i^{n}$ introduced by the [differentiation](#Differentiation) rules upon Fourier transforming the homogeneous differential equation because this factor may then be cancelled. The simplest allowable $U(x)=x$ leads to the [[standard normal distribution]] .

More generally, a set of eigenfunctions is also found by noting that the [differentiation](#Differentiation) rules imply that the [[ordinary differential equation]] $\left[W\left({\frac {i}{2\pi }}{\frac {d}{dx}}\right)+W(x)\right]\psi (x)=C\psi (x)$ with $C$ constant and $W(x)$ being a non-constant even function remains invariant in form when applying the Fourier transform ${\mathcal {F}}$ to both sides of the equation. The simplest example is provided by ⁠ $W(x)=x^{2}$ ⁠ , which is equivalent to considering the Schrödinger equation for the [[quantum harmonic oscillator]] . The corresponding solutions provide an important choice of an orthonormal basis for [[`L2(R)`]] and are given by the "physicist's" [[Hermite functions]] . Equivalently one may use $\psi _{n}(x)={\frac {\sqrt[{4}]{2}}{\sqrt {n!}}}e^{-\pi x^{2}}\mathrm {He} _{n}\left(2x{\sqrt {\pi }}\right),$ where ⁠ $\mathrm {He} _{n}(x)$ ⁠ are the "probabilist's" [[Hermite polynomials]] , defined as $\mathrm {He} _{n}(x)=(-1)^{n}e^{{\frac {1}{2}}x^{2}}\left({\frac {d}{dx}}\right)^{n}e^{-{\frac {1}{2}}x^{2}}.$

Under this convention for the Fourier transform, we have that ${\widehat {\psi }}_{n}(\xi )=(-i)^{n}\psi _{n}(\xi ).$

In other words, the Hermite functions form a complete [[orthonormal]] system of [[eigenfunctions]] for the Fourier transform on ⁠ $L^{2}(\mathbb {R} )$ ⁠ . However, this choice of eigenfunctions is not unique. Because of ${\mathcal {F}}^{4}=\mathrm {id}$ there are only four different [[eigenvalues]] of the Fourier transform (the fourth roots of unity ⁠ $\pm 1$ ⁠ and ⁠ $\pm i$ ⁠ ) and any linear combination of eigenfunctions with the same eigenvalue gives another eigenfunction. As a consequence of this, it is possible to decompose `L2(R)` as a direct sum of four spaces `H0` , `H1` , `H2` , and `H3` where the Fourier transform acts on `Hk` simply by multiplication by `ik` .

Since the complete set of Hermite functions `ψn` provides a resolution of the identity they diagonalize the Fourier operator, i.e. the Fourier transform can be represented by such a sum of terms weighted by the above eigenvalues, and these sums can be explicitly summed: ${\mathcal {F}}[f](\xi )=\int dxf(x)\sum _{n\geq 0}(-i)^{n}\psi _{n}(x)\psi _{n}(\xi )~.$

This approach to define the Fourier transform was first proposed by [[Norbert Wiener]] . Among other properties, Hermite functions decrease exponentially fast in both frequency and time domains, and they are thus used to define a generalization of the Fourier transform, namely the [[fractional Fourier transform]] used in time–frequency analysis. In [[physics]] , this transform was introduced by [[Edward Condon]] . This [[change of basis]] becomes possible because the Fourier transform is a unitary transform when using the right [conventions](#Other_conventions) . Consequently, under the proper conditions it may be expected to result from a self-adjoint generator $N$ via ${\mathcal {F}}[\psi ]=e^{-itN}\psi .$

The operator $N$ is the [[number operator]] of the quantum harmonic oscillator written as $N\equiv {\frac {1}{2}}\left(x-{\frac {\partial }{\partial x}}\right)\left(x+{\frac {\partial }{\partial x}}\right)={\frac {1}{2}}\left(-{\frac {\partial ^{2}}{\partial x^{2}}}+x^{2}-1\right).$

It can be interpreted as the [[generator]] of [[fractional Fourier transforms]] for arbitrary values of `t` , and of the conventional continuous Fourier transform ${\mathcal {F}}$ for the particular value ⁠ $t=\pi /2$ ⁠ , with the [[Mehler kernel]] implementing the corresponding [[active transform]] . The eigenfunctions of $N$ are the [[Hermite functions]] ⁠ $\psi _{n}(x)$ ⁠ , which are therefore also eigenfunctions of ⁠ ${\mathcal {F}}$ ⁠ .

Upon extending the Fourier transform to [[distributions]] the [[Dirac comb]] is also an eigenfunction of the Fourier transform.

### Inversion and periodicity

Further information: [[Fourier inversion theorem]] and [[Fractional Fourier transform]]

Under suitable conditions on the function ⁠ $f$ ⁠ , it can be recovered from its Fourier transform ⁠ ${\widehat {f}}$ ⁠ . Indeed, denoting the Fourier transform operator by ⁠ ${\mathcal {F}}$ ⁠ , so ⁠ ${\mathcal {F}}f:={\widehat {f}}$ ⁠ , then for suitable functions, applying the Fourier transform twice simply flips the function: ⁠ $\left({\mathcal {F}}^{2}f\right)(x)=f(-x)$ ⁠ , which can be interpreted as "reversing time". Since reversing time is two-periodic, applying this twice yields ⁠ ${\mathcal {F}}^{4}(f)=f$ ⁠ , so the Fourier transform operator is four-periodic, and similarly the inverse Fourier transform can be obtained by applying the Fourier transform three times: ⁠ ${\mathcal {F}}^{3}\left({\widehat {f}}\right)=f$ ⁠ . In particular the Fourier transform is invertible (under suitable conditions).

More precisely, defining the parity operator ${\mathcal {P}}$ such that ⁠ $({\mathcal {P}}f)(x)=f(-x)$ ⁠ , we have: ${\begin{aligned}{\mathcal {F}}^{0}&=\mathrm {id} ,\\{\mathcal {F}}^{1}&={\mathcal {F}},\\{\mathcal {F}}^{2}&={\mathcal {P}},\\{\mathcal {F}}^{3}&={\mathcal {F}}^{-1}={\mathcal {P}}\circ {\mathcal {F}}={\mathcal {F}}\circ {\mathcal {P}},\\{\mathcal {F}}^{4}&=\mathrm {id} \end{aligned}}$ These equalities of operators require careful definition of the space of functions in question, defining equality of functions (equality at every point? equality [[almost everywhere]] ?) and defining equality of operators – that is, defining the topology on the function space and operator space in question. These are not true for all functions, but are true under various conditions, which are the content of the various forms of the [[Fourier inversion theorem]] .

This fourfold periodicity of the Fourier transform is similar to a rotation of the plane by 90°, particularly as the two-fold iteration yields a reversal, and in fact this analogy can be made precise. While the Fourier transform can simply be interpreted as switching the time domain and the frequency domain, with the inverse Fourier transform switching them back, more geometrically it can be interpreted as a rotation by 90° in the [[time–frequency domain]] (considering time as the ⁠ $x$ ⁠ -axis and frequency as the ⁠ $y$ ⁠ -axis), and the Fourier transform can be generalized to the [[fractional Fourier transform]] , which involves rotations by other angles. This can be further generalized to [[linear canonical transformations]] , which can be visualized as the action of the [[special linear group]] [[`SL2(R)`]] on the time–frequency plane, with the preserved symplectic form corresponding to the [uncertainty principle](#Uncertainty_principle) , below. This approach is particularly studied in [[signal processing]] , under [[time–frequency analysis]] .

### Connection with the Heisenberg group

The [[Heisenberg group]] is a certain [[group]] of [[unitary operators]] on the [[Hilbert space]] `L2(R)` of square integrable complex valued functions `f` on the real line, generated by the translations `(Ty f)(x) = f (x + y)` and multiplication by `ei2πξx` , `(Mξ f)(x) = ei2πξx f (x)` . These operators do not commute, as their (group) commutator is $\left(M_{\xi }^{-1}T_{y}^{-1}M_{\xi }T_{y}f\right)(x)=e^{i2\pi \xi y}f(x),$ which is multiplication by the constant (independent of `x` ) `ei2πξy ∈ U(1)` (the [[circle group]] of unit modulus complex numbers). As an abstract group, the Heisenberg group is the three-dimensional [[Lie group]] of triples `(x, ξ, z) ∈ R2 × U(1)` , with the group law $\left(x_{1},\xi _{1},t_{1}\right)\cdot \left(x_{2},\xi _{2},t_{2}\right)=\left(x_{1}+x_{2},\xi _{1}+\xi _{2},t_{1}t_{2}e^{-2i\pi x_{1}\xi _{2}}\right).$

Denote the Heisenberg group by `H1` . The above procedure describes not only the group structure, but also a standard [[unitary representation]] of `H1` on a Hilbert space, which we denote by `ρ : H1 → B(L2(R))` . Define the linear automorphism of `R2` by $J{\begin{pmatrix}x\\\xi \end{pmatrix}}={\begin{pmatrix}-\xi \\x\end{pmatrix}}$ so that `J2 = −I` . This `J` can be extended to a unique automorphism of `H1` : $j\left(x,\xi ,t\right)=\left(-\xi ,x,te^{-i2\pi \xi x}\right).$

According to the [[Stone–von Neumann theorem]] , the unitary representations `ρ` and `ρ ∘ j` are unitarily equivalent, so there is a unique intertwiner `W ∈ U(L2(R))` such that $\rho \circ j=W\rho W^{\*}.$ This operator `W` is the Fourier transform.

Many of the standard properties of the Fourier transform are immediate consequences of this more general framework. For example, the square of the Fourier transform, `W2` , is an intertwiner associated with `J2 = −I` , and so we have `(W2f)(x) = f (−x)` is the reflection of the original function `f` .

## Complex domain

The [[integral]] for the Fourier transform ${\widehat {f}}(\xi )=\int _{-\infty }^{\infty }e^{-i2\pi \xi t}f(t)\,dt$ can be studied for [[complex]] values of its argument `ξ` . Depending on the properties of `f` , this might not converge off the real axis at all, or it might converge to a [[complex]] [[analytic function]] for all values of `ξ = σ + iτ` , or something in between.

The [[Paley–Wiener theorem]] says that `f` is smooth (i.e., `n` -times differentiable for all positive integers `n` ) and compactly supported if and only if `f̂ (σ + iτ)` is a [[holomorphic function]] for which there exists a [[constant]] `a > 0` such that for any [[integer]] `n ≥ 0` , $\left\vert \xi ^{n}{\widehat {f}}(\xi )\right\vert \leq Ce^{a\vert \tau \vert }$ for some constant `C` . (In this case, `f` is supported on `[−a, a]` .) This can be expressed by saying that `f̂` is an [[entire function]] that is [[rapidly decreasing]] in `σ` (for fixed `τ` ) and of exponential growth in `τ` (uniformly in `σ` ).

(If `f` is not smooth, but only `L2` , the statement still holds provided `n = 0` . ) The space of such functions of a [[complex variable]] is called the Paley–Wiener space. This theorem has been generalised to semisimple [[Lie groups]] .

If `f` is supported on the half-line `t ≥ 0` , then `f` is said to be "causal" because the [[impulse response function]] of a physically realisable [[filter]] must have this property, as no effect can precede its cause. [[Paley]] and Wiener showed that then `f̂` extends to a [[holomorphic function]] on the complex lower half-plane `τ < 0` that tends to zero as `τ` goes to infinity. The converse is false and it is not known how to characterise the Fourier transform of a causal function.

### Laplace transform

See also: [[Laplace transform § Fourier transform]]

The Fourier transform `f̂(ξ)` is related to the [[Laplace transform]] `F(s)` , which is also used for the solution of [[differential equations]] and the analysis of [[filters]] .

It may happen that a function `f` for which the Fourier integral does not converge on the real axis at all, nevertheless has a complex Fourier transform defined in some region of the [[complex plane]] .

For example, if `f(t)` is of exponential growth, i.e., $\vert f(t)\vert 

The more usual version ("one-sided") of the Laplace transform is $F(s)=\int _{0}^{\infty }f(t)e^{-st}\,dt.$

If `f` is also causal and analytic, then: ⁠ ${\widehat {f}}(i\tau )=F(-2\pi \tau )$ ⁠ . Thus, extending the Fourier transform to the complex domain means it includes the Laplace transform as a special case in the case of causal functions—but with the change of variable `s = i2πξ` .

From another, perhaps more classical viewpoint, the Laplace transform by its form involves an additional exponential regulating term that lets it converge outside of the imaginary line where the Fourier transform is defined. As such it can converge for at most exponentially divergent series and integrals, whereas the original Fourier decomposition cannot, enabling analysis of systems with divergent or critical elements. Two particular examples from linear signal processing are the construction of allpass filter networks from critical comb and mitigating filters via exact pole-zero cancellation on the unit circle. Such designs are common in audio processing, where highly nonlinear [[phase response]] is sought for, as in reverb.

Furthermore, when extended pulselike impulse responses are sought for signal processing work, the easiest way to produce them is to have one circuit that produces a divergent time response, and then to cancel its divergence through a delayed opposite and compensatory response. There, only the delay circuit in-between admits a classical Fourier description, which is critical. Both the circuits to the side are unstable, and do not admit a convergent Fourier decomposition. However, they do admit a Laplace domain description, with identical half-planes of convergence in the complex plane (or in the discrete case, the Z-plane), wherein their effects cancel.

In modern mathematics the Laplace transform is conventionally subsumed under the aegis Fourier methods. Both of them are subsumed by the far more general, and more abstract, idea of [[harmonic analysis]] .

### Inversion

Still with ⁠ $\xi =\sigma +i\tau$ ⁠ , if ${\widehat {f}}$ is complex analytic for `a ≤ τ ≤ b` , then $\int _{-\infty }^{\infty }{\widehat {f}}(\sigma +ia)e^{i2\pi \xi t}\,d\sigma =\int _{-\infty }^{\infty }{\widehat {f}}(\sigma +ib)e^{i2\pi \xi t}\,d\sigma$ by [[Cauchy's integral theorem]] . Therefore, the Fourier inversion formula can use integration along different lines, parallel to the real axis.

Theorem: If `f(t) = 0` for `t < 0` , and `|f(t)| < Cea|t|` for some constants `C, a > 0` , then $f(t)=\int _{-\infty }^{\infty }{\widehat {f}}(\sigma +i\tau )e^{i2\pi \xi t}\,d\sigma ,$ for any `τ < −⁠a/2π⁠` .

This theorem implies the [[Mellin inversion formula]] for the Laplace transformation, $f(t)={\frac {1}{i2\pi }}\int _{b-i\infty }^{b+i\infty }F(s)e^{st}\,ds$ for any `b > a` , where `F(s)` is the Laplace transform of `f(t)` .

The hypotheses can be weakened, as in the results of Carleson and Hunt, to `f(t) e−at` being `L1` , provided that `f` be of bounded variation in a closed neighborhood of `t` (cf. [[Dini test]] ), the value of `f` at `t` be taken to be the [[arithmetic mean]] of the left and right limits, and that the integrals be taken in the sense of Cauchy principal values.

`L2` versions of these inversion formulas are also available.

## Fourier transform on Euclidean space

The Fourier transform can be defined in any arbitrary number of dimensions `n` . As with the one-dimensional case, there are many conventions. For an integrable function `f(x)` , this article takes the definition: ${\widehat {f}}({\boldsymbol {\xi }})={\mathcal {F}}(f)({\boldsymbol {\xi }})=\int _{\mathbb {R} ^{n}}f(\mathbf {x} )e^{-i2\pi {\boldsymbol {\xi }}\cdot \mathbf {x} }\,d\mathbf {x}$ where `x` and `ξ` are `n` -dimensional [[vectors]] , and `x · ξ` is the [[dot product]] of the vectors. Alternatively, `ξ` can be viewed as belonging to the [[dual vector space]] ⁠ $\mathbb {R} ^{n\star }$ ⁠ , in which case the dot product becomes the [[contraction]] of `x` and `ξ` , usually written as `⟨x, ξ⟩` .

All of the basic properties listed above hold for the `n` -dimensional Fourier transform, as do Plancherel's and Parseval's theorem. When the function is integrable, the Fourier transform is still uniformly continuous and the [[Riemann–Lebesgue lemma]] holds.

### Uncertainty principle

Further information: [[Uncertainty principle]]

Generally speaking, the more concentrated `f(x)` is, the more spread out its Fourier transform `f̂(ξ)` must be. In particular, the scaling property of the Fourier transform may be seen as saying: if we squeeze a function in `x` , its Fourier transform stretches out in `ξ` . It is not possible to arbitrarily concentrate both a function and its Fourier transform.

The trade-off between the compaction of a function and its Fourier transform can be formalized in the form of an [[uncertainty principle]] by viewing a function and its Fourier transform as [[conjugate variables]] with respect to the [[symplectic form]] on the [[time–frequency domain]] : from the point of view of the [[linear canonical transformation]] , the Fourier transform is rotation by 90° in the time–frequency domain, and preserves the [[symplectic form]] .

Suppose `f(x)` is an integrable and [[square-integrable]] function. [[Without loss of generality]] , assume that `f(x)` is normalized: $\int _{-\infty }^{\infty }|f(x)|^{2}\,dx=1.$

It follows from the [[Plancherel theorem]] that `f̂(ξ)` is also normalized.

The spread around `x = 0` may be measured by the dispersion about zero defined by $D_{0}(f)=\int _{-\infty }^{\infty }x^{2}|f(x)|^{2}\,dx.$

In probability terms, this is the [[second moment]] of `|f(x)|2` about zero.

The uncertainty principle states that, if `f(x)` is absolutely continuous and the functions `x·f(x)` and `f′(x)` are square integrable, then $D_{0}(f)D_{0}({\widehat {f}})\geq {\frac {1}{16\pi ^{2}}}.$

The equality is attained only in the case ${\begin{aligned}f(x)&=C_{1}\,e^{-\pi {\frac {x^{2}}{\sigma ^{2}}}}\\\therefore {\widehat {f}}(\xi )&=\sigma C_{1}\,e^{-\pi \sigma ^{2}\xi ^{2}}\end{aligned}}$ where `σ > 0` is arbitrary and `C1 = ⁠4√2/√σ⁠` so that `f` is `L2` -normalized. In other words, where `f` is a (normalized) [[Gaussian function]] with variance `σ2/2π` , centered at zero, and its Fourier transform is a Gaussian function with variance `σ−2/2π` . Gaussian functions are examples of [[Schwartz functions]] (see the discussion on tempered distributions below).

In fact, this inequality implies that: $\left(\int _{-\infty }^{\infty }(x-x_{0})^{2}|f(x)|^{2}\,dx\right)\left(\int _{-\infty }^{\infty }(\xi -\xi _{0})^{2}\left|{\widehat {f}}(\xi )\right|^{2}\,d\xi \right)\geq {\frac {1}{16\pi ^{2}}},\quad \forall x_{0},\xi _{0}\in \mathbb {R} .$ In [[quantum mechanics]] , the [[momentum]] and position [[wave functions]] are Fourier transform pairs, up to a factor of the [[Planck constant]] . With this constant properly taken into account, the inequality above becomes the statement of the [[Heisenberg uncertainty principle]] .

A stronger uncertainty principle is the [[Hirschman uncertainty principle]] , which is expressed as: $H\left(\left|f\right|^{2}\right)+H\left(\left|{\widehat {f}}\right|^{2}\right)\geq \log \left({\frac {e}{2}}\right)$ where `H(p)` is the [[differential entropy]] of the [[probability density function]] `p(x)` : $H(p)=-\int _{-\infty }^{\infty }p(x)\log {\bigl (}p(x){\bigr )}\,dx$ where the logarithms may be in any base that is consistent. The equality is attained for a Gaussian, as in the previous case.

### Sine and cosine transforms

Main article: [[Sine and cosine transforms]]

Fourier's original formulation of the transform did not use complex numbers, but rather sines and cosines. Statisticians and others still use this form. An absolutely integrable function `f` for which Fourier inversion holds can be expanded in terms of genuine frequencies (avoiding negative frequencies, which are sometimes considered hard to interpret physically ) `λ` by $f(t)=\int _{0}^{\infty }{\bigl (}a(\lambda )\cos(2\pi \lambda t)+b(\lambda )\sin(2\pi \lambda t){\bigr )}\,d\lambda .$

This is called an expansion as a [[trigonometric integral]] , or a Fourier integral expansion. The coefficient functions `a` and `b` can be found by using variants of the Fourier cosine transform and the Fourier sine transform (the normalisations are, again, not standardised): $a(\lambda )=2\int _{-\infty }^{\infty }f(t)\cos(2\pi \lambda t)\,dt$ and $b(\lambda )=2\int _{-\infty }^{\infty }f(t)\sin(2\pi \lambda t)\,dt.$

Older literature refers to the two transform functions, the Fourier cosine transform, `a` , and the Fourier sine transform, `b` .

The function `f` can be recovered from the sine and cosine transform using $f(t)=2\int _{0}^{\infty }\int _{-\infty }^{\infty }f(\tau )\cos {\bigl (}2\pi \lambda (\tau -t){\bigr )}\,d\tau \,d\lambda .$ together with trigonometric identities. This is referred to as Fourier's integral formula.

### Spherical harmonics

Let the set of [[homogeneous]] [[harmonic]] [[polynomials]] of degree `k` on `Rn` be denoted by `Ak` . The set `Ak` consists of the [[solid spherical harmonics]] of degree `k` . The solid spherical harmonics play a similar role in higher dimensions to the Hermite polynomials in dimension one. Specifically, if `f(x) = e−π|x|2P(x)` for some `P(x)` in `Ak` , then ⁠ ${\widehat {f}}(\xi )=i^{-k}f(\xi )$ ⁠ . Let the set `Hk` be the closure in `L2(Rn)` of linear combinations of functions of the form `f(|x|)P(x)` where `P(x)` is in `Ak` . The space `L2(Rn)` is then a direct sum of the spaces `Hk` and the Fourier transform maps each space `Hk` to itself and it is possible to characterize the action of the Fourier transform on each space `Hk` .

Let `f(x) = f0(|x|)P(x)` (with `P(x)` in `Ak` ), then ${\widehat {f}}(\xi )=F_{0}(|\xi |)P(\xi )$ where $F_{0}(r)=2\pi i^{-k}r^{-{\frac {n+2k-2}{2}}}\int _{0}^{\infty }f_{0}(s)J_{\frac {n+2k-2}{2}}(2\pi rs)s^{\frac {n+2k}{2}}\,ds.$

Here `J(n + 2k − 2)/2` denotes the [[Bessel function]] of the first kind with order `⁠n + 2k − 2/2⁠` . When `k = 0` this gives a useful formula for the Fourier transform of a radial function. This is essentially the [[Hankel transform]] . Moreover, there is a simple recursion relating the cases `n + 2` and `n` allowing to compute, e.g., the three-dimensional Fourier transform of a radial function from the one-dimensional one.

### Restriction problems

See also: [[Fourier extension operator]]

In higher dimensions it becomes interesting to study restriction problems for the Fourier transform. The Fourier transform of an integrable function is continuous and the restriction of this function to any set is defined. But for a square-integrable function the Fourier transform could be a general class of square integrable functions. As such, the restriction of the Fourier transform of an `L2(Rn)` function cannot be defined on sets of measure 0. It is still an active area of study to understand restriction problems in `Lp` for `1 < p < 2` . It is possible in some cases to define the restriction of a Fourier transform to a set `S` , provided `S` has non-zero curvature. The case when `S` is the unit sphere in `Rn` is of particular interest. In this case the Tomas– [[Stein]] restriction theorem states that the restriction of the Fourier transform to the unit sphere in `Rn` is a bounded operator on `Lp` provided `1 ≤ p ≤ ⁠2n + 2/n + 3⁠` .

One notable difference between the Fourier transform in 1 dimension versus higher dimensions concerns the partial sum operator. Consider an increasing collection of measurable sets `ER` indexed by `R ∈ (0, ∞)` : such as balls of radius `R` centered at the origin, or cubes of side `2R` . For a given integrable function `f` , consider the function `fR` defined by: $f_{R}(x)=\int _{E_{R}}{\widehat {f}}(\xi )e^{i2\pi x\cdot \xi }\,d\xi ,\quad x\in \mathbb {R} ^{n}.$

Suppose in addition that `f ∈ Lp(Rn)` . For `n = 1` and `1 < p < ∞` , if one takes `ER = (−R, R)` , then `fR` converges to `f` in `Lp` as `R` tends to infinity, by the boundedness of the [[Hilbert transform]] . Naively one may hope the same holds true for `n > 1` . In the case that `ER` is taken to be a cube with side length `R` , then convergence still holds. Another natural candidate is the Euclidean ball `ER = {ξ : |ξ| < R}` . In order for this partial sum operator to converge, it is necessary that the [[multiplier]] for the unit ball be bounded in `Lp(Rn)` . For `n ≥ 2` it is a celebrated theorem of [[Charles Fefferman]] that the multiplier for the unit ball is never bounded unless `p = 2` . In fact, when `p ≠ 2` , this shows that not only may `fR` fail to converge to `f` in `Lp` , but for some functions `f ∈ Lp(Rn)` , `fR` is not even an element of `Lp` .

## Fourier transform on function spaces

See also: [[Riesz–Thorin theorem]]

The definition of the Fourier transform naturally extends from $L^{1}(\mathbb {R} )$ to ⁠ $L^{1}(\mathbb {R} ^{n})$ ⁠ . That is, if $f\in L^{1}(\mathbb {R} ^{n})$ then the Fourier transform ${\mathcal {F}}:L^{1}(\mathbb {R} ^{n})\to L^{\infty }(\mathbb {R} ^{n})$ is given by $f(x)\mapsto {\widehat {f}}(\xi )=\int _{\mathbb {R} ^{n}}f(x)e^{-i2\pi \xi \cdot x}\,dx,\quad \forall \xi \in \mathbb {R} ^{n}.$ This operator is [[bounded]] as $\sup _{\xi \in \mathbb {R} ^{n}}\left\vert {\widehat {f}}(\xi )\right\vert \leq \int _{\mathbb {R} ^{n}}\vert f(x)\vert \,dx,$ which shows that its [[operator norm]] is bounded by `1` . The [[Riemann–Lebesgue lemma]] shows that if $f\in L^{1}(\mathbb {R} ^{n})$ then its Fourier transform actually belongs to the [[space of continuous functions that vanish at infinity]] , i.e., ⁠ ${\widehat {f}}\in C_{0}(\mathbb {R} ^{n})\subset L^{\infty }(\mathbb {R} ^{n})$ ⁠ . Furthermore, the [[image]] of $L^{1}$ under ${\mathcal {F}}$ is a strict subset of ⁠ $C_{0}(\mathbb {R} ^{n})$ ⁠ .

Similarly to the case of one variable, the Fourier transform can be defined on ⁠ $L^{2}(\mathbb {R} ^{n})$ ⁠ . The Fourier transform in $L^{2}(\mathbb {R} ^{n})$ is no longer given by an ordinary Lebesgue integral, although it can be computed by an [[improper integral]] , i.e., ${\widehat {f}}(\xi )=\lim _{R\to \infty }\int _{|x|\leq R}f(x)e^{-i2\pi \xi \cdot x}\,dx$ where the limit is taken in the `L2` sense.

Furthermore, ${\mathcal {F}}:L^{2}(\mathbb {R} ^{n})\to L^{2}(\mathbb {R} ^{n})$ is a [[unitary operator]] . For an operator to be unitary it is sufficient to show that it is bijective and preserves the inner product, so in this case these follow from the Fourier inversion theorem combined with the fact that for any `f, g ∈ L2(Rn)` we have $\int _{\mathbb {R} ^{n}}f(x){\mathcal {F}}g(x)\,dx=\int _{\mathbb {R} ^{n}}{\mathcal {F}}f(x)g(x)\,dx.$

In particular, the image of `L2(Rn)` is itself under the Fourier transform.

### On other L p

For ⁠ $1 , the Fourier transform can be defined on $L^{p}(\mathbb {R} )$ by [[Marcinkiewicz interpolation]] , which amounts to decomposing such functions into a fat tail part in `L2` plus a fat body part in `L1` . In each of these spaces, the Fourier transform of a function in `Lp(Rn)` is in `Lq(Rn)` , where `q = ⁠p/p − 1⁠` is the [[Hölder conjugate]] of `p` (by the [[Hausdorff–Young inequality]] ). However, except for `p = 2` , the image is not easily characterized. Further extensions become more technical. The Fourier transform of functions in `Lp` for the range `2 < p < ∞` requires the study of distributions. In fact, it can be shown that there are functions in `Lp` with `p > 2` so that the Fourier transform is not defined as a function.

### Tempered distributions

Main article: [[Distribution (mathematics) § Tempered distributions and Fourier transform]]

See also: [[Rigged Hilbert space]]

One might consider enlarging the domain of the Fourier transform from $L^{1}+L^{2}$ by considering [[generalized functions]] , or distributions. A distribution on $\mathbb {R} ^{n}$ is a continuous linear functional on the space $C_{c}^{\infty }(\mathbb {R} ^{n})$ of compactly supported smooth functions (i.e. [[bump functions]] ), equipped with a suitable topology. Since $C_{c}^{\infty }(\mathbb {R} ^{n})$ is dense in ⁠ $L^{2}(\mathbb {R} ^{n})$ ⁠ , the [[Plancherel theorem]] allows one to extend the definition of the Fourier transform to general functions in $L^{2}(\mathbb {R} ^{n})$ by continuity arguments. The strategy is then to consider the action of the Fourier transform on $C_{c}^{\infty }(\mathbb {R} ^{n})$ and pass to distributions by duality. The obstruction to doing this is that the Fourier transform does not map $C_{c}^{\infty }(\mathbb {R} ^{n})$ to ⁠ $C_{c}^{\infty }(\mathbb {R} ^{n})$ ⁠ . In fact the Fourier transform of an element in $C_{c}^{\infty }(\mathbb {R} ^{n})$ can not vanish on an open set; see the above discussion on the uncertainty principle.

The Fourier transform can also be defined for [[tempered distributions]] ⁠ ${\mathcal {S}}'(\mathbb {R} ^{n})$ ⁠ , dual to the space of [[Schwartz functions]] ⁠ ${\mathcal {S}}(\mathbb {R} ^{n})$ ⁠ . A Schwartz function is a smooth function that decays at infinity, along with all of its derivatives, hence $C_{c}^{\infty }(\mathbb {R} ^{n})\subset {\mathcal {S}}(\mathbb {R} ^{n})$ and: ${\mathcal {F}}:C_{c}^{\infty }(\mathbb {R} ^{n})\rightarrow {\mathcal {S}}(\mathbb {R} ^{n})\setminus C_{c}^{\infty }(\mathbb {R} ^{n}).$ The Fourier transform is an [[automorphism]] of the Schwartz space and, by duality, also an automorphism of the space of tempered distributions. The tempered distributions include well-behaved functions of polynomial growth, distributions of compact support as well as all the integrable functions mentioned above.

For the definition of the Fourier transform of a tempered distribution, let $f$ and $g$ be integrable functions, and let ${\widehat {f}}$ and ${\widehat {g}}$ be their Fourier transforms respectively. Then the Fourier transform obeys the following multiplication formula, $\int _{\mathbb {R} ^{n}}{\widehat {f}}(x)g(x)\,dx=\int _{\mathbb {R} ^{n}}f(x){\widehat {g}}(x)\,dx.$

Every integrable function $f$ defines (induces) a distribution $T_{f}$ by the relation $T_{f}(\varphi )=\int _{\mathbb {R} ^{n}}f(x)\varphi (x)\,dx,\quad \forall \varphi \in {\mathcal {S}}(\mathbb {R} ^{n}).$ So it makes sense to define the Fourier transform of a tempered distribution $T_{f}\in {\mathcal {S}}'(\mathbb {R} )$ by the duality: $\langle {\widehat {T}}_{f},\varphi \rangle =\langle T_{f},{\widehat {\varphi }}\rangle ,\quad \forall \varphi \in {\mathcal {S}}(\mathbb {R} ^{n}).$ Extending this to all tempered distributions $T$ gives the general definition of the Fourier transform.

Distributions can be differentiated and the above-mentioned compatibility of the Fourier transform with differentiation and convolution remains true for tempered distributions.

## Generalizations

### Fourier–Stieltjes transform on measurable spaces

See also: [[Bochner–Minlos theorem]] , [[Riesz–Markov–Kakutani representation theorem]] , and [[Fourier series § Fourier-Stieltjes series]]

The Fourier transform of a [[finite]] [[Borel measure]] `μ` on `Rn` , given by the bounded, uniformly continuous function: ${\widehat {\mu }}(\xi )=\int _{\mathbb {R} ^{n}}e^{-i2\pi x\cdot \xi }\,d\mu ,$ is called the Fourier–Stieltjes transform due to its connection with the [[Riemann-Stieltjes integral]] representation of [[(Radon) measures]] . If $\mu$ is the [[probability distribution]] of a [[random variable]] $X$ then its Fourier–Stieltjes transform is, by definition, a [[characteristic function]] . If, in addition, the probability distribution has a [[probability density function]] , this definition is subject to the usual Fourier transform. Stated more generally, when $\mu$ is [[absolutely continuous]] with respect to the Lebesgue measure, i.e., $d\mu =f(x)\,dx,$ then ${\widehat {\mu }}(\xi )={\widehat {f}}(\xi ),$ and the Fourier-Stieltjes transform reduces to the usual definition of the Fourier transform. That is, the notable difference with the Fourier transform of integrable functions is that the Fourier-Stieltjes transform need not vanish at infinity, i.e., the [[Riemann–Lebesgue lemma]] fails for measures.

[[Bochner's theorem]] characterizes which functions may arise as the Fourier–Stieltjes transform of a positive measure on the circle.

One example of a finite Borel measure that is not a function is the [[Dirac measure]] . Its Fourier transform is a constant function (whose value depends on the form of the Fourier transform used).

### Locally compact abelian groups

Main article: [[Pontryagin duality]]

The Fourier transform may be generalized to any [[locally compact abelian group]] , i.e., an [[abelian group]] that is also a [[locally compact Hausdorff space]] such that the group operation is continuous. If `G` is a locally compact abelian group, it has a translation invariant measure `μ` , called [[Haar measure]] . For a locally compact abelian group `G` , the set of irreducible, i.e. one-dimensional, unitary representations are called its [[characters]] . With its natural group structure and the topology of uniform convergence on compact sets (that is, the topology induced by the [[compact-open topology]] on the space of all continuous functions from $G$ to the [[circle group]] ), the set of characters `Ĝ` is itself a locally compact abelian group, called the Pontryagin dual of `G` . For a function `f` in `L1(G)` , its Fourier transform is defined by ${\widehat {f}}(\xi )=\int _{G}{\overline {\xi (x)}}f(x)\,d\mu \quad {\text{for any }}\xi \in {\widehat {G}}.$

The Riemann–Lebesgue lemma holds in this case; `f̂(ξ)` is a function vanishing at infinity on `Ĝ` .

The Fourier transform on `T` = R/Z is an example; here `T` is a locally compact abelian group, and the Haar measure `μ` on `T` can be thought of as the Lebesgue measure on [0,1). Consider a representation of `T` on the complex plane `C` thought of as a 1-dimensional complex vector space. There is a group of such representations (which are irreducible since `C` is 1-dim) $\{e_{k}:T\rightarrow GL_{1}(C)=C^{\*}\mid k\in Z\}$ where $e_{k}(x)=e^{i2\pi kx}$ for ⁠ $x\in T$ ⁠ .

The character of such representation, that is the trace of $e_{k}(x)$ (thought of as a one-by-one matrix) for each $x\in T$ and ⁠ $k\in Z$ ⁠ , is $e^{i2\pi kx}$ itself. Now, in the case of representations of finite groups, the character table of a group `G` consists of rows of vectors such that each row is the character of one irreducible representation of `G` , and these vectors form an orthonormal basis of the space of class (meaning conjugation-invariant) functions that map from `G` to `C` by Schur's lemma. The group `T` is no longer finite but still compact, and it preserves the orthonormality of the character table. Each row of the table is the function $e_{k}(x)$ of ⁠ $x\in T$ ⁠ , and the inner product between two class functions (all functions being class functions since `T` is abelian) $f,g\in L^{2}(T,d\mu )$ is defined as with the normalizing factor ⁠ $\vert T\vert =1$ ⁠ . The sequence $\{e_{k}\mid k\in Z\}$ is an orthonormal basis of the space of class functions ⁠ $L^{2}(T,d\mu )$ ⁠ .

For any representation `V` of a finite group `G` , $\chi _{v}$ can be expressed as the span ( $V_{i}$ are the irreducible representations of `G` ), such that ⁠ $\textstyle \left\langle \chi _{v},\chi _{v_{i}}\right\rangle ={\frac {1}{\vert G\vert }}\sum _{g\in G}\chi _{v}(g){\overline {\chi }}_{v_{i}}(g)$ ⁠ . Similarly for $G=T$ and ⁠ $f\in L^{2}(T,d\mu )$ ⁠ , ⁠ $\textstyle f(x)=\sum _{k\in Z}{\widehat {f}}(k)e_{k}$ ⁠ . The Pontriagin dual ${\widehat {T}}$ is $\{e_{k}\}(k\in Z)$ and for ⁠ $f\in L^{2}(T,d\mu )$ ⁠ , is its Fourier transform for ⁠ $e_{k}\in {\widehat {T}}$ ⁠ .

### Gelfand transform

Main article: [[Gelfand representation]]

The Fourier transform is also a special case of the [[Gelfand transform]] . In this particular context, it is closely related to the Pontryagin duality map defined above.

Given an abelian [[locally compact]] [[Hausdorff]] [[topological group]] `G` , as before we consider the space `L1(G)` , defined using a Haar measure. With convolution as multiplication, `L1(G)` is an abelian [[Banach algebra]] . It also has an [[involution]] \* given by $f^{\*}(g)={\overline {f\left(g^{-1}\right)}}.$

Taking the completion with respect to the largest possible `C\*` -norm gives its enveloping `C\*` -algebra, called the group `C\*` -algebra `C\*(G)` of `G` . (Any `C\*` -norm on `L1(G)` is bounded by the `L1` norm, therefore their supremum exists.)

Given any abelian `C\*` -algebra `A` , the Gelfand transform gives an isomorphism between `A` and `C0(A^)` , where `A^` is the multiplicative linear functionals, i.e. one-dimensional representations, on `A` with the weak-\* topology. The map is simply given by $a\mapsto {\bigl (}\varphi \mapsto \varphi (a){\bigr )}.$ It turns out that the multiplicative linear functionals of `C\*(G)` , after suitable identification, are exactly the characters of `G` , and the Gelfand transform, when restricted to the dense subset `L1(G)` , is the Fourier–Pontryagin transform.

### Compact non-abelian groups

The Fourier transform can also be defined for functions on a non-abelian group, provided that the group is [[compact]] . Removing the assumption that the underlying group is abelian, irreducible unitary representations need not always be one-dimensional. This means the Fourier transform on a non-abelian group takes values as Hilbert space operators. The Fourier transform on compact groups is a major tool in [[representation theory]] and [[non-commutative harmonic analysis]] .

Let `G` be a compact [[Hausdorff]] [[topological group]] . Let `Σ` denote the collection of all isomorphism classes of finite-dimensional irreducible [[unitary representations]] , along with a definite choice of representation `U(σ)` on the [[Hilbert space]] `Hσ` of finite dimension `dσ` for each `σ ∈ Σ` . If `μ` is a finite [[Borel measure]] on `G` , then the Fourier–Stieltjes transform of `μ` is the operator on `Hσ` defined by $\left\langle {\widehat {\mu }}\xi ,\eta \right\rangle _{H_{\sigma }}=\int _{G}\left\langle {\overline {U}}_{g}^{(\sigma )}\xi ,\eta \right\rangle \,d\mu (g)$ where `U(σ)` is the complex-conjugate representation of `U(σ)` acting on `Hσ` . If `μ` is [[absolutely continuous]] with respect to the [[left-invariant probability measure]] `λ` on `G` , [[represented]] as $d\mu =f\,d\lambda$ for some `f ∈ L1(λ)` , one identifies the Fourier transform of `f` with the Fourier–Stieltjes transform of `μ` .

The mapping $\mu \mapsto {\widehat {\mu }}$ defines an isomorphism between the [[Banach space]] `M(G)` of finite Borel measures (see Rca space ) and a closed subspace of the Banach space `C∞(Σ)` consisting of all sequences `E = (Eσ)` indexed by `Σ` of (bounded) linear operators `Eσ : Hσ → Hσ` for which the norm $\|E\|=\sup _{\sigma \in \Sigma }\left\|E_{\sigma }\right\|$ is finite. The " [[convolution theorem]] " asserts that, furthermore, this isomorphism of Banach spaces is in fact an isometric isomorphism of [[C\*-algebras]] into a subspace of `C∞(Σ)` . Multiplication on `M(G)` is given by [[convolution]] of measures and the involution \* defined by $f^{\*}(g)={\overline {f\left(g^{-1}\right)}},$ and `C∞(Σ)` has a natural `C\*` -algebra structure as Hilbert space operators.

The [[Peter–Weyl theorem]] holds, and a version of the Fourier inversion formula ( [[Plancherel's theorem]] ) follows: if `f ∈ L2(G)` , then $f(g)=\sum _{\sigma \in \Sigma }d_{\sigma }\operatorname {tr} \left({\widehat {f}}(\sigma )U_{g}^{(\sigma )}\right)$ where the summation is understood as convergent in the `L2` sense.

The generalization of the Fourier transform to the noncommutative situation has also in part contributed to the development of [[noncommutative geometry]] . [ citation needed ] In this context, a categorical generalization of the Fourier transform to noncommutative groups is [[Tannaka–Krein duality]] , which replaces the group of characters with the category of representations. However, this loses the connection with harmonic functions.

## Alternatives

In [[signal processing]] terms, a function (of time) is a representation of a signal with perfect time resolution , but no frequency information, while the Fourier transform has perfect frequency resolution , but no time information: the magnitude of the Fourier transform at a point is how much frequency content there is, but location is only given by phase (argument of the Fourier transform at a point), and [[standing waves]] are not localized in time – a sine wave continues out to infinity, without decaying. This limits the usefulness of the Fourier transform for analyzing signals that are localized in time, notably [[transients]] , or any signal of finite extent.

As alternatives to the Fourier transform, in [[time–frequency analysis]] , one uses time–frequency transforms or time–frequency distributions to represent signals in a form that has some time information and some frequency information – by the uncertainty principle, there is a trade-off between these. These can be generalizations of the Fourier transform, such as the [[short-time Fourier transform]] , [[fractional Fourier transform]] , synchrosqueezing Fourier transform, or other functions to represent signals, as in [[wavelet transforms]] and [[chirplet transforms]] , with the wavelet analog of the (continuous) Fourier transform being the [[continuous wavelet transform]] .

## Example

The following figures provide a visual illustration of how the Fourier transform's integral measures whether a frequency is present in a particular function. The first image depicts the function ⁠ $f(t)=\cos(2\pi \ 3t)\ e^{-\pi t^{2}}$ ⁠ , which is a 3 [[Hz]] cosine wave (the first term) shaped by a [[Gaussian]] [[envelope function]] (the second term) that smoothly turns the wave on and off. The next 2 images show the product ⁠ $f(t)e^{-i2\pi 3t}$ ⁠ , which must be integrated to calculate the Fourier transform at +3 Hz. The real part of the integrand has a non-negative average value, because the alternating signs of $f(t)$ and $\operatorname {Re} (e^{-i2\pi 3t})$ oscillate at the same rate and in phase, whereas $f(t)$ and $\operatorname {Im} (e^{-i2\pi 3t})$ oscillate at the same rate but with orthogonal phase. The absolute value of the Fourier transform at +3 Hz is 0.5, which is relatively large. When added to the Fourier transform at -3 Hz (which is identical because we started with a real signal), we find that the amplitude of the 3 Hz frequency component is 1.

[[]]

Original function, which has a strong 3 Hz component. Real and imaginary parts of the integrand of its Fourier transform at +3 Hz.

However, when you try to measure a frequency that is not present, both the real and imaginary component of the integral vary rapidly between positive and negative values. For instance, the red curve is looking for 5 Hz. The absolute value of its integral is nearly zero, indicating that almost no 5 Hz component was in the signal. The general situation is usually more complicated than this, but heuristically this is how the Fourier transform measures how much of an individual frequency is present in a function ⁠ $f(t)$ ⁠ .

- [[]]

 Real and imaginary parts of the integrand for its Fourier transform at +5 Hz. - [[]]

 Magnitude of its Fourier transform, with +3 and +5 Hz labeled.

To re-enforce an earlier point, the reason for the response at $\xi =-3$ Hz is because $\cos(2\pi 3t)$ and $\cos(2\pi (-3)t)$ are indistinguishable. The transform of $e^{i2\pi 3t}\cdot e^{-\pi t^{2}}$ would have just one response, whose amplitude is the integral of the smooth envelope: ⁠ $e^{-\pi t^{2}}$ ⁠ , whereas $\operatorname {Re} (f(t)\cdot e^{-i2\pi 3t})$ is ⁠ $e^{-\pi t^{2}}(1+\cos(2\pi 6t))/2$ ⁠ .

## Applications

See also: [[Spectral density § Applications]]

[[]]

Some problems, such as certain differential equations, become easier to solve when the Fourier transform is applied. In that case the solution to the original problem is recovered using the inverse Fourier transform.

Linear operations performed in one domain (time or frequency) have corresponding operations in the other domain, which are sometimes easier to perform. The operation of [[differentiation]] in the time domain corresponds to multiplication by the frequency, so some [[differential equations]] are easier to analyze in the frequency domain. Also, [[convolution]] in the time domain corresponds to ordinary multiplication in the frequency domain (see Convolution theorem ). After performing the desired operations, transformation of the result can be made back to the time domain. [[Harmonic analysis]] is the systematic study of the relationship between the frequency and time domains, including the kinds of functions or operations that are "simpler" in one or the other, and has deep connections to many areas of modern mathematics.

### Analysis of differential equations

Perhaps the most important use of the Fourier transformation is to solve [[partial differential equations]] . Many of the equations of the mathematical physics of the nineteenth century can be treated this way. Fourier studied the heat equation, which in one dimension and in dimensionless units is ${\frac {\partial ^{2}y(x,t)}{\partial ^{2}x}}={\frac {\partial y(x,t)}{\partial t}}.$ The example we will give, a slightly more difficult one, is the wave equation in one dimension, ${\frac {\partial ^{2}y(x,t)}{\partial ^{2}x}}={\frac {\partial ^{2}y(x,t)}{\partial ^{2}t}}.$

As usual, the problem is not to find a solution: there are infinitely many. The problem is that of the so-called "boundary problem": find a solution that satisfies the 'boundary conditions' $y(x,0)=f(x),\qquad {\frac {\partial y(x,0)}{\partial t}}=g(x).$

Here, `f` and `g` are given functions. For the heat equation, only one boundary condition can be required (usually the first one). But for the wave equation, there are still infinitely many solutions `y` that satisfy the first boundary condition. But when one imposes both conditions, there is only one possible solution.

It is easier to find the Fourier transform `ŷ` of the solution than to find the solution directly. This is because the Fourier transformation takes differentiation into multiplication by the Fourier-dual variable, and so a partial differential equation applied to the original function is transformed into multiplication by polynomial functions of the dual variables applied to the transformed function. After `ŷ` is determined, we can apply the inverse Fourier transformation to find `y` .

Fourier's method is as follows. First, note that any function of the forms $\cos {\bigl (}2\pi \xi (x\pm t){\bigr )}{\text{ or }}\sin {\bigl (}2\pi \xi (x\pm t){\bigr )}$ satisfies the wave equation. These are called the elementary solutions.

Second, note that therefore any integral ${\begin{aligned}y(x,t)=\int _{0}^{\infty }d\xi {\Bigl [}&a_{+}(\xi )\cos {\bigl (}2\pi \xi (x+t){\bigr )}+a_{-}(\xi )\cos {\bigl (}2\pi \xi (x-t){\bigr )}+{}\\&b_{+}(\xi )\sin {\bigl (}2\pi \xi (x+t){\bigr )}+b_{-}(\xi )\sin \left(2\pi \xi (x-t)\right){\Bigr ]}\end{aligned}}$ satisfies the wave equation for arbitrary `a+, a−, b+, b−` . This integral may be interpreted as a continuous linear combination of solutions for the linear equation.

Now this resembles the formula for the Fourier synthesis of a function. In fact, this is the real inverse Fourier transform of `a±` and `b±` in the variable `x` .

The third step is to examine how to find the specific unknown coefficient functions `a±` and `b±` that will lead to `y` satisfying the boundary conditions. We are interested in the values of these solutions at `t = 0` . So we will set `t = 0` . Assuming that the conditions needed for Fourier inversion are satisfied, we can then find the Fourier sine and cosine transforms (in the variable `x` ) of both sides and obtain $2\int _{-\infty }^{\infty }y(x,0)\cos(2\pi \xi x)\,dx=a_{+}+a_{-}$ and $2\int _{-\infty }^{\infty }y(x,0)\sin(2\pi \xi x)\,dx=b_{+}+b_{-}.$

Similarly, taking the derivative of `y` with respect to `t` and then applying the Fourier sine and cosine transformations yields $2\int _{-\infty }^{\infty }{\frac {\partial y(u,0)}{\partial t}}\sin(2\pi \xi x)\,dx=(2\pi \xi )\left(-a_{+}+a_{-}\right)$ and $2\int _{-\infty }^{\infty }{\frac {\partial y(u,0)}{\partial t}}\cos(2\pi \xi x)\,dx=(2\pi \xi )\left(b_{+}-b_{-}\right).$

These are four linear equations for the four unknowns `a±` and `b±` , in terms of the Fourier sine and cosine transforms of the boundary conditions, which are easily solved by elementary algebra, provided that these transforms can be found.

In summary, we chose a set of elementary solutions, parametrized by `ξ` , of which the general solution would be a (continuous) linear combination in the form of an integral over the parameter `ξ` . But this integral was in the form of a Fourier integral. The next step was to express the boundary conditions in terms of these integrals, and set them equal to the given functions `f` and `g` . But these expressions also took the form of a Fourier integral because of the properties of the Fourier transform of a derivative. The last step was to exploit Fourier inversion by applying the Fourier transformation to both sides, thus obtaining expressions for the coefficient functions `a±` and `b±` in terms of the given boundary conditions `f` and `g` .

From a higher point of view, Fourier's procedure can be reformulated more conceptually. Since there are two variables, we will use the Fourier transformation in both `x` and `t` rather than operate as Fourier did, who only transformed in the spatial variables. Note that `ŷ` must be considered in the sense of a distribution since `y(x, t)` is not going to be `L1` : as a wave, it will persist through time and thus is not a transient phenomenon. But it will be bounded and so its Fourier transform can be defined as a distribution. The operational properties of the Fourier transformation that are relevant to this equation are that it takes differentiation in `x` to multiplication by `i2πξ` and differentiation with respect to `t` to multiplication by `i2πf` where `f` is the frequency. Then the wave equation becomes an algebraic equation in `ŷ` : $\xi ^{2}{\widehat {y}}(\xi ,f)=f^{2}{\widehat {y}}(\xi ,f).$ This is equivalent to requiring `ŷ(ξ, f) = 0` unless `ξ = ±f` . Right away, this explains why the choice of elementary solutions we made earlier worked so well: obviously `ŷ = δ(ξ ± f)` will be solutions. Applying Fourier inversion to these delta functions, we obtain the elementary solutions we picked earlier. But from the higher point of view, one does not pick elementary solutions, but rather considers the space of all distributions that are supported on the (degenerate) conic `ξ2 − f2 = 0` .

We may as well consider the distributions supported on the conic that are given by distributions of one variable on the line `ξ = f` plus distributions on the line `ξ = −f` as follows: if `Φ` is any test function, $\iint {\widehat {y}}\varphi (\xi ,f)\,d\xi \,df=\int s_{+}\varphi (\xi ,\xi )\,d\xi +\int s_{-}\varphi (\xi ,-\xi )\,d\xi ,$ where `s+` , and `s−` , are distributions of one variable.

Then Fourier inversion gives, for the boundary conditions, something very similar to what we had more concretely above (put `Φ(ξ, f) = ei2π(xξ+tf)` , which is clearly of polynomial growth): $y(x,0)=\int {\bigl \{}s_{+}(\xi )+s_{-}(\xi ){\bigr \}}e^{i2\pi \xi x+0}\,d\xi$ and ${\frac {\partial y(x,0)}{\partial t}}=\int {\bigl \{}s_{+}(\xi )-s_{-}(\xi ){\bigr \}}i2\pi \xi e^{i2\pi \xi x+0}\,d\xi .$

Now, as before, applying the one-variable Fourier transformation in the variable `x` to these functions of `x` yields two equations in the two unknown distributions `s±` (which can be taken to be ordinary functions if the boundary conditions are `L1` or `L2` ).

From a calculational point of view, the drawback of course is that one must first calculate the Fourier transforms of the boundary conditions, then assemble the solution from these, and then calculate an inverse Fourier transform. Closed form formulas are rare, except when there is some geometric symmetry that can be exploited, and the numerical calculations are difficult because of the oscillatory nature of the integrals, which makes convergence slow and hard to estimate. For practical calculations, other methods are often used.

#### Nonlinear Fourier transform

Main article: [[Inverse scattering transform]]

The twentieth century has seen application of these methods to all linear partial differential equations with polynomial coefficients as well as an extension to certain classes of [[nonlinear partial differential equations]] . Specifically, nonlinear evolution equations (i.e. those equations that describe how a particular quantity evolves in time from a specified initial state) that can be associated with linear eigenvalue problems whose eigenvalues are integrals of the nonlinear equations. As it may be considered an extension of Fourier analysis to nonlinear problems, the solution method is called the **nonlinear Fourier transform** (or **[[inverse scattering transform]]** ) method.

### Fourier-transform spectroscopy

Main article: [[Fourier-transform spectroscopy]]

The Fourier transform is also used in [[nuclear magnetic resonance]] (NMR) and in other kinds of [[spectroscopy]] , e.g. infrared ( [[FTIR]] ). In NMR an exponentially shaped free induction decay (FID) signal is acquired in the time domain and Fourier-transformed to a Lorentzian line-shape in the frequency domain. The Fourier transform is also used in [[magnetic resonance imaging]] (MRI) and [[mass spectrometry]] .

### Quantum mechanics

The Fourier transform is useful in [[quantum mechanics]] in at least two different ways. To begin with, the basic conceptual structure of quantum mechanics postulates the existence of pairs of [[complementary variables]] , connected by the [[Heisenberg uncertainty principle]] . For example, in one dimension, the spatial variable `q` of, say, a particle, can only be measured by the quantum mechanical " [[position operator]] " at the cost of losing information about the momentum `p` of the particle. Therefore, the physical state of the particle can either be described by a function, called "the wave function", of `q` or by a function of `p` but not by a function of both variables. The variable `p` is called the conjugate variable to `q` .

In classical mechanics, the physical state of a particle (existing in one dimension, for simplicity of exposition) would be given by assigning definite values to both `p` and `q` simultaneously. Thus, the set of all possible physical states is the two-dimensional real vector space with a `p` -axis and a `q` -axis called the [[phase space]] . In contrast, quantum mechanics chooses a polarisation of this space in the sense that it picks a subspace of one-half the dimension, for example, the `q` -axis alone, but instead of considering only points, takes the set of all complex-valued "wave functions" on this axis. Nevertheless, choosing the `p` -axis is an equally valid polarisation, yielding a different representation of the set of possible physical states of the particle. Both representations of the wavefunction are related by a Fourier transform, such that $\varphi (p)=\int dq\,\psi (q)e^{-ipq/h},$ or, equivalently, $\psi (q)=\int dp\,\varphi (p)e^{ipq/h}.$

Physically realisable states are `L2` , and so by the [[Plancherel theorem]] , their Fourier transforms are also `L2` . (Note that since `q` is in units of distance and `p` is in units of momentum, the presence of the Planck constant in the exponent makes the exponent [[dimensionless]] , as it should be.)

Therefore, the Fourier transform can be used to pass from one way of representing the state of the particle, by a wave function of position, to another way of representing the state of the particle: by a wave function of momentum. Infinitely many different polarisations are possible, and all are equally valid. Being able to transform states from one representation to another by the Fourier transform is not only convenient but also the underlying reason of the Heisenberg [uncertainty principle](#Uncertainty_principle) .

The other use of the Fourier transform in both quantum mechanics and [[quantum field theory]] is to solve the applicable wave equation. In non-relativistic quantum mechanics, the [[Schrödinger equation]] for a time-varying wave function in one-dimension, not subject to external forces, is $-{\frac {\partial ^{2}}{\partial x^{2}}}\psi (x,t)=i{\frac {h}{2\pi }}{\frac {\partial }{\partial t}}\psi (x,t).$

This is the same as the heat equation except for the presence of the imaginary unit `i` . Fourier methods can be used to solve this equation.

In the presence of a potential, given by the potential energy function `V(x)` , the equation becomes $-{\frac {\partial ^{2}}{\partial x^{2}}}\psi (x,t)+V(x)\psi (x,t)=i{\frac {h}{2\pi }}{\frac {\partial }{\partial t}}\psi (x,t).$

The "elementary solutions", as we referred to them above, are the so-called "stationary states" of the particle, and Fourier's algorithm, as described above, can still be used to solve the boundary value problem of the future evolution of `ψ` given its values for `t = 0` . Neither of these approaches is of much practical use in quantum mechanics. Boundary value problems and the time-evolution of the wave function is not of much practical interest: it is the stationary states that are most important.

In relativistic quantum mechanics, the Schrödinger equation becomes a wave equation as was usual in classical physics, except that complex-valued waves are considered. A simple example, in the absence of interactions with other particles or fields, is the free one-dimensional Klein–Gordon–Schrödinger–Fock equation, this time in dimensionless units, $\left({\frac {\partial ^{2}}{\partial x^{2}}}+1\right)\psi (x,t)={\frac {\partial ^{2}}{\partial t^{2}}}\psi (x,t).$

This is, from the mathematical point of view, the same as the wave equation of classical physics solved above (but with a complex-valued wave, which makes no difference in the methods). This is of great use in quantum field theory: each separate Fourier component of a wave can be treated as a separate harmonic oscillator and then quantized, a procedure known as "second quantization". Fourier methods have been adapted to also deal with non-trivial interactions.

Finally, the [[number operator]] of the [[quantum harmonic oscillator]] can be interpreted, for example via the [[Mehler kernel]] , as the [[generator]] of the [Fourier transform](#Eigenfunctions)

⁠ ${\mathcal {F}}$ ⁠ .

### Signal processing

The Fourier transform is used for the spectral analysis of time-series. The subject of statistical signal processing does not, however, usually apply the Fourier transformation to the signal itself. Even if a real signal is indeed transient, it has been found in practice advisable to model a signal by a function (or, alternatively, a stochastic process) that is stationary in the sense that its characteristic properties are constant over all time. The Fourier transform of such a function does not exist in the usual sense, and it has been found more useful for the analysis of signals to instead take the Fourier transform of its autocorrelation function.

The autocorrelation function `R` of a function `f` is defined by $R_{f}(\tau )=\lim _{T\rightarrow \infty }{\frac {1}{2T}}\int _{-T}^{T}f(t)f(t+\tau )\,dt.$

This function is a function of the time-lag `τ` elapsing between the values of `f` to be correlated.

For most functions `f` that occur in practice, `R` is a bounded even function of the time-lag `τ` and for typical noisy signals it turns out to be uniformly continuous with a maximum at `τ = 0` .

The autocorrelation function, more properly called the autocovariance function unless it is normalized in some appropriate fashion, measures the strength of the correlation between the values of `f` separated by a time lag. This is a way of searching for the correlation of `f` with its own past. It is useful even for other statistical tasks besides the analysis of signals. For example, if `f(t)` represents the temperature at time `t` , one expects a strong correlation with the temperature at a time lag of 24 hours.

It possesses a Fourier transform, $P_{f}(\xi )=\int _{-\infty }^{\infty }R_{f}(\tau )e^{-i2\pi \xi \tau }\,d\tau .$

This Fourier transform is called the [[power spectral density]] function of `f` . (Unless all periodic components are first filtered out from `f` , this integral will diverge, but it is easy to filter out such periodicities.)

The power spectrum, as indicated by this density function `P` , measures the amount of variance contributed to the data by the frequency `ξ` . In electrical signals, the variance is proportional to the average power (energy per unit time), and so the power spectrum describes how much the different frequencies contribute to the average power of the signal. This process is called the spectral analysis of time-series and is analogous to the usual analysis of variance of data that is not a time-series ( [[ANOVA]] ).

Knowledge of which frequencies are "important" in this sense is crucial for the proper design of filters and for the proper evaluation of measuring apparatuses. It can also be useful for the scientific analysis of the phenomena responsible for producing the data.

The power spectrum of a signal can also be approximately measured directly by measuring the average power that remains in a signal after all the frequencies outside a narrow band have been filtered out.

Spectral analysis is carried out for visual signals as well. The power spectrum ignores all phase relations, which is good enough for many purposes, but for video signals other types of spectral analysis must also be employed, still using the Fourier transform as a tool.

## Other notations

Other common notations for ${\widehat {f}}(\xi )$ include: ${\tilde {f}}(\xi ),\ F(\xi ),\ {\mathcal {F}}\left(f\right)(\xi ),\ \left({\mathcal {F}}f\right)(\xi ),\ {\mathcal {F}}(f),\ {\mathcal {F}}\{f\},\ {\mathcal {F}}{\bigl (}f(t){\bigr )},\ {\mathcal {F}}{\bigl \{}f(t){\bigr \}}.$

In the sciences and engineering it is also common to make substitutions like these: $\xi \rightarrow f,\quad x\rightarrow t,\quad f\rightarrow x,\quad {\widehat {f}}\rightarrow X.$

So the transform pair $f(x)\ {\stackrel {\mathcal {F}}{\Longleftrightarrow }}\ {\widehat {f}}(\xi )$ can become $x(t)\ {\stackrel {\mathcal {F}}{\Longleftrightarrow }}\ X(f)$

A disadvantage of the capital letter notation is when expressing a transform such as ${\widehat {f}}\cdot g$ or ⁠ ${\widehat {f}}'$ ⁠ , which become the more awkward ${\mathcal {F}}\{f\cdot g\}$ and ⁠ ${\mathcal {F}}\{f'\}$ ⁠ .

In some contexts such as particle physics, the same symbol $f$ may be used for both for a function as well as it Fourier transform, with the two only distinguished by their [[argument]] I.e. $f(k_{1}+k_{2})$ would refer to the Fourier transform because of the momentum argument, while $f(x_{0}+\pi {\vec {r}})$ would refer to the original function because of the positional argument. Although tildes may be used as in ${\tilde {f}}$ to indicate Fourier transforms, tildes may also be used to indicate a modification of a quantity with a more [[Lorentz invariant]] form, such as ⁠ ${\tilde {dk}}={\frac {dk}{(2\pi )^{3}2\omega }}$ ⁠ , so care must be taken. Similarly, ${\widehat {f}}$ often denotes the [[Hilbert transform]] of ⁠ $f$ ⁠ .

The interpretation of the complex function `f̂(ξ)` may be aided by expressing it in [[polar coordinate]] form ${\widehat {f}}(\xi )=A(\xi )e^{i\varphi (\xi )}$ in terms of the two real functions `A(ξ)` and `φ(ξ)` where: $A(\xi )=\left|{\widehat {f}}(\xi )\right|,$ is the [[amplitude]] and $\varphi (\xi )=\arg \left({\widehat {f}}(\xi )\right),$ is the [[phase]] (see Arg ).

Then the inverse transform can be written: $f(x)=\int _{-\infty }^{\infty }A(\xi )\ e^{i{\bigl (}2\pi \xi x+\varphi (\xi ){\bigr )}}\,d\xi ,$ which is a recombination of all the frequency components of `f(x)` . Each component is a complex [[sinusoid]] of the form `e2πixξ` whose amplitude is `A(ξ)` and whose initial [[phase angle]] (at `x = 0` ) is `φ(ξ)` .

The Fourier transform may be thought of as a mapping on function spaces. This mapping is here denoted F and `F(f)` is used to denote the Fourier transform of the function `f` . This mapping is linear, which means that F can also be seen as a linear transformation on the function space and implies that the standard notation in linear algebra of applying a linear transformation to a vector (here the function `f` ) can be used to write `F f` instead of `F(f)` . Since the result of applying the Fourier transform is again a function, we can be interested in the value of this function evaluated at the value `ξ` for its variable, and this is denoted either as `F f(ξ)` or as `(F f)(ξ)` . Notice that in the former case, it is implicitly understood that F is applied first to `f` and then the resulting function is evaluated at `ξ` , not the other way around.

In mathematics and various applied sciences, it is often necessary to distinguish between a function `f` and the value of `f` when its variable equals `x` , denoted `f(x)` . This means that a notation like `F(f(x))` formally can be interpreted as the Fourier transform of the values of `f` at `x` . Despite this flaw, the previous notation appears frequently, often when a particular function or a function of a particular variable is to be transformed. For example, ${\mathcal {F}}{\bigl (}\operatorname {rect} (x){\bigr )}=\operatorname {sinc} (\xi )$ is sometimes used to express that the Fourier transform of a [[rectangular function]] is a [[sinc function]] , or ${\mathcal {F}}{\bigl (}f(x+x_{0}){\bigr )}={\mathcal {F}}{\bigl (}f(x){\bigr )}\,e^{i2\pi x_{0}\xi }$ is used to express the shift property of the Fourier transform.

Notice, that the last example is only correct under the assumption that the transformed function is a function of `x` , not of `x0` .

As discussed above, the [[characteristic function]] of a random variable is the same as the [Fourier–Stieltjes transform](#Fourier–Stieltjes_transform) of its distribution measure, but in this context it is typical to take a different convention for the constants. Typically characteristic function is defined $E\left(e^{it\cdot X}\right)=\int e^{it\cdot x}\,d\mu _{X}(x).$

As in the case of the "non-unitary angular frequency" convention above, the factor of 2 `π` appears in neither the normalizing constant nor the exponent. Unlike any of the conventions appearing above, this convention takes the opposite sign in the exponent.

## Computation methods

The appropriate computation method largely depends how the original mathematical function is represented and the desired form of the output function. In this section we consider both functions of a continuous variable, ⁠ $f(x)$ ⁠ , and functions of a discrete variable (i.e. ordered pairs of $x$ and $f$ values). For discrete-valued ⁠ $x$ ⁠ , the transform integral becomes a summation of sinusoids, which is still a continuous function of frequency ( ⁠ $\xi$ ⁠ or ⁠ $\omega$ ⁠ ). When the sinusoids are harmonically related (i.e. when the $x$ -values are spaced at integer multiples of an interval), the transform is called [[discrete-time Fourier transform]] (DTFT).

### Discrete Fourier transforms and fast Fourier transforms

Sampling the DTFT at equally-spaced values of frequency is the most common modern method of computation. Efficient procedures, depending on the frequency resolution needed, are described at [[Discrete-time Fourier transform § Sampling the DTFT]] . The [[discrete Fourier transform]] (DFT), used there, is usually computed by a [[fast Fourier transform]] (FFT) algorithm.

### Symbolic integration of closed-form functions

Tables of [[closed-form]] Fourier transforms, such as [§ Square-integrable functions, one-dimensional](#Square-integrable_functions,_one-dimensional) and [[§ Table of discrete-time Fourier transforms]] , are created by mathematically evaluating the Fourier analysis integral (or summation) into another closed-form function of frequency ( ⁠ $\xi$ ⁠ or ⁠ $\omega$ ⁠ ). When mathematically possible, this provides a transform for a continuum of frequency values.

Many computer algebra systems such as [[Matlab]] and [[Mathematica]] that are capable of [[symbolic integration]] are capable of computing Fourier transforms symbolically. <https://en.wikipedia.org/wiki/Help:Edit_summary>

### Numerical integration of closed-form continuous functions

Discrete sampling of the Fourier transform can also be done by [[numerical integration]] of the definition at each value of frequency for which transform is desired. The numerical integration approach works on a much broader class of functions than the analytic approach.

### Numerical integration of a series of ordered pairs

If the input function is a series of ordered pairs, numerical integration reduces to just a summation over the set of data pairs. The DTFT is a common subcase of this more general situation.

## Tables of important Fourier transforms

The following tables record some closed-form Fourier transforms. For functions `f(x)` and `g(x)` denote their Fourier transforms by `f̂` and `ĝ` . Only the three most common conventions are included. It may be useful to notice that entry 105 gives a relationship between the Fourier transform of a function and the original function, which can be seen as relating the Fourier transform and its inverse.

### Functional relationships, one-dimensional

The Fourier transforms in this table may be found in [Erdélyi (1954)](#CITEREFErdélyi1954) or [Kammler (2000](#CITEREFKammler2000) , appendix).

| | Function | Fourier transform unitary, ordinary frequency | Fourier transform unitary, angular frequency | Fourier transform non-unitary, angular frequency | Remarks | | --- | --- | --- | --- | --- | --- | | | $f(x)$ | ${\begin{aligned}&{\widehat {f}}(\xi )\triangleq {\widehat {f}}_{1}(\xi )\\&=\int _{-\infty }^{\infty }f(x)e^{-i2\pi \xi x}\,dx\end{aligned}}$ | ${\begin{aligned}&{\widehat {f}}(\omega )\triangleq {\widehat {f}}_{2}(\omega )\\&={\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{\infty }f(x)e^{-i\omega x}\,dx\end{aligned}}$ | ${\begin{aligned}&{\widehat {f}}(\omega )\triangleq {\widehat {f}}_{3}(\omega )\\&=\int _{-\infty }^{\infty }f(x)e^{-i\omega x}\,dx\end{aligned}}$ | Definitions | | 101 | $a\,f(x)+b\,g(x)$ | $a\,{\widehat {f}}(\xi )+b\,{\widehat {g}}(\xi )$ | $a\,{\widehat {f}}(\omega )+b\,{\widehat {g}}(\omega )$ | $a\,{\widehat {f}}(\omega )+b\,{\widehat {g}}(\omega )$ | Linearity | | 102 | $f(x-a)$ | $e^{-i2\pi \xi a}{\widehat {f}}(\xi )$ | $e^{-ia\omega }{\widehat {f}}(\omega )$ | $e^{-ia\omega }{\widehat {f}}(\omega )$ | Shift in time domain | | 103 | $f(x)e^{iax}$ | ${\widehat {f}}\left(\xi -{\frac {a}{2\pi }}\right)$ | ${\widehat {f}}(\omega -a)$ | ${\widehat {f}}(\omega -a)$ | Shift in frequency domain, dual of 102 | | 104 | $f(ax)$ | ${\frac {1}{|a|}}{\widehat {f}}\left({\frac {\xi }{a}}\right)$ | ${\frac {1}{|a|}}{\widehat {f}}\left({\frac {\omega }{a}}\right)$ | ${\frac {1}{|a|}}{\widehat {f}}\left({\frac {\omega }{a}}\right)$ | Scaling in the time domain. If `|a|` is large, then `f(ax)` is concentrated around `0` and spreads out and flattens. | | 105 | ${\widehat {f}}_{n}(x)$ | ${\widehat {f}}_{1}(x)\ {\stackrel {{\mathcal {F}}_{1}}{\longleftrightarrow }}\ f(-\xi )$ | ${\widehat {f}}_{2}(x)\ {\stackrel {{\mathcal {F}}_{2}}{\longleftrightarrow }}\ f(-\omega )$ | ${\widehat {f}}_{3}(x)\ {\stackrel {{\mathcal {F}}_{3}}{\longleftrightarrow }}\ 2\pi f(-\omega )$ | The same transform is applied twice, but `x` replaces the frequency variable ( `ξ` or `ω` ) after the first transform. | | 106 | ${\frac {d^{n}f(x)}{dx^{n}}}$ | $(i2\pi \xi )^{n}{\widehat {f}}(\xi )$ | $(i\omega )^{n}{\widehat {f}}(\omega )$ | $(i\omega )^{n}{\widehat {f}}(\omega )$ | `n` th-order derivative. As `f` is a [[Schwartz function]] | | 106.5 | $\int _{-\infty }^{x}f(\tau )d\tau$ | ${\frac {{\widehat {f}}(\xi )}{i2\pi \xi }}+C\,\delta (\xi )$ | ${\frac {{\widehat {f}}(\omega )}{i\omega }}+{\sqrt {2\pi }}C\delta (\omega )$ | ${\frac {{\widehat {f}}(\omega )}{i\omega }}+2\pi C\delta (\omega )$ | Integration. Note: $\delta$ is the [[Dirac delta function]] and $C$ is the average ( [[DC]] ) value of $f(x)$ such that | | 107 | $x^{n}f(x)$ | $\left({\frac {i}{2\pi }}\right)^{n}{\frac {d^{n}{\widehat {f}}(\xi )}{d\xi ^{n}}}$ | $i^{n}{\frac {d^{n}{\widehat {f}}(\omega )}{d\omega ^{n}}}$ | $i^{n}{\frac {d^{n}{\widehat {f}}(\omega )}{d\omega ^{n}}}$ | This is the dual of 106 | | 108 | $(f\*g)(x)$ | ${\widehat {f}}(\xi ){\widehat {g}}(\xi )$ | ${\sqrt {2\pi }}\ {\widehat {f}}(\omega ){\widehat {g}}(\omega )$ | ${\widehat {f}}(\omega ){\widehat {g}}(\omega )$ | The notation `f ∗ g` denotes the [[convolution]] of `f` and `g` – this rule is the [[convolution theorem]] | | 109 | $f(x)g(x)$ | $\left({\widehat {f}}\*{\widehat {g}}\right)(\xi )$ | ${\frac {1}{\sqrt {2\pi }}}\left({\widehat {f}}\*{\widehat {g}}\right)(\omega )$ | ${\frac {1}{2\pi }}\left({\widehat {f}}\*{\widehat {g}}\right)(\omega )$ | This is the dual of 108 | | 110 | For `f(x)` purely real | ${\widehat {f}}(-\xi )={\overline {{\widehat {f}}(\xi )}}$ | ${\widehat {f}}(-\omega )={\overline {{\widehat {f}}(\omega )}}$ | ${\widehat {f}}(-\omega )={\overline {{\widehat {f}}(\omega )}}$ | Hermitian symmetry. `z` indicates the [[complex conjugate]] . | | 113 | For `f(x)` purely imaginary | ${\widehat {f}}(-\xi )=-{\overline {{\widehat {f}}(\xi )}}$ | ${\widehat {f}}(-\omega )=-{\overline {{\widehat {f}}(\omega )}}$ | ${\widehat {f}}(-\omega )=-{\overline {{\widehat {f}}(\omega )}}$ | `z` indicates the [[complex conjugate]] . | | 114 | ${\overline {f(x)}}$ | ${\overline {{\widehat {f}}(-\xi )}}$ | ${\overline {{\widehat {f}}(-\omega )}}$ | ${\overline {{\widehat {f}}(-\omega )}}$ | [[Complex conjugation]] , generalization of 110 and 113 | | 115 | $f(x)\cos(ax)$ | ${\frac {{\widehat {f}}\left(\xi -{\frac {a}{2\pi }}\right)+{\widehat {f}}\left(\xi +{\frac {a}{2\pi }}\right)}{2}}$ | ${\frac {{\widehat {f}}(\omega -a)+{\widehat {f}}(\omega +a)}{2}}$ | ${\frac {{\widehat {f}}(\omega -a)+{\widehat {f}}(\omega +a)}{2}}$ | This follows from rules 101 and 103 using [[Euler's formula]] : ⁠ $\cos(ax)={\tfrac {e^{iax}+e^{-iax}}{2}}$ ⁠ . | | 116 | $f(x)\sin(ax)$ | ${\frac {{\widehat {f}}\left(\xi -{\frac {a}{2\pi }}\right)-{\widehat {f}}\left(\xi +{\frac {a}{2\pi }}\right)}{2i}}$ | ${\frac {{\widehat {f}}(\omega -a)-{\widehat {f}}(\omega +a)}{2i}}$ | ${\frac {{\widehat {f}}(\omega -a)-{\widehat {f}}(\omega +a)}{2i}}$ | This follows from 101 and 103 using [[Euler's formula]] : ⁠ $\sin(ax)={\tfrac {e^{iax}-e^{-iax}}{2i}}$ ⁠ . |

### Square-integrable functions, one-dimensional

The Fourier transforms in this table may be found in [Campbell & Foster (1948)](#CITEREFCampbellFoster1948) , [Erdélyi (1954)](#CITEREFErdélyi1954) , or [Kammler (2000](#CITEREFKammler2000) , appendix).

| | Function | Fourier transform unitary, ordinary frequency | Fourier transform unitary, angular frequency | Fourier transform non-unitary, angular frequency | Remarks | | --- | --- | --- | --- | --- | --- | | | $f(x)$ | ${\begin{aligned}&{\widehat {f}}(\xi )\triangleq {\widehat {f}}_{1}(\xi )\\&=\int _{-\infty }^{\infty }f(x)e^{-i2\pi \xi x}\,dx\end{aligned}}$ | ${\begin{aligned}&{\widehat {f}}(\omega )\triangleq {\widehat {f}}_{2}(\omega )\\&={\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{\infty }f(x)e^{-i\omega x}\,dx\end{aligned}}$ | ${\begin{aligned}&{\widehat {f}}(\omega )\triangleq {\widehat {f}}_{3}(\omega )\\&=\int _{-\infty }^{\infty }f(x)e^{-i\omega x}\,dx\end{aligned}}$ | Definitions | | 201 | $\operatorname {rect} (ax)$ | ${\frac {1}{|a|}}\,\operatorname {sinc} \left({\frac {\xi }{a}}\right)$ | ${\frac {1}{\sqrt {2\pi a^{2}}}}\,\operatorname {sinc} \left({\frac {\omega }{2\pi a}}\right)$ | ${\frac {1}{|a|}}\,\operatorname {sinc} \left({\frac {\omega }{2\pi a}}\right)$ | The [[rectangular pulse]] and the normalized [[sinc function]] , here defined as `sinc(x) = ⁠sin(πx)/πx⁠` | | 202 | $\operatorname {sinc} (ax)$ | ${\frac {1}{|a|}}\,\operatorname {rect} \left({\frac {\xi }{a}}\right)$ | ${\frac {1}{\sqrt {2\pi a^{2}}}}\,\operatorname {rect} \left({\frac {\omega }{2\pi a}}\right)$ | ${\frac {1}{|a|}}\,\operatorname {rect} \left({\frac {\omega }{2\pi a}}\right)$ | Dual of rule 201. The [[rectangular function]] is an ideal [[low-pass filter]] , and the [[sinc function]] is the [[non-causal]] impulse response of such a filter. The [[sinc function]] is defined here as `sinc(x) = ⁠sin(πx)/πx⁠` . | | 203 | $\operatorname {sinc} ^{2}(ax)$ | ${\frac {1}{|a|}}\,\operatorname {tri} \left({\frac {\xi }{a}}\right)$ | ${\frac {1}{\sqrt {2\pi a^{2}}}}\,\operatorname {tri} \left({\frac {\omega }{2\pi a}}\right)$ | ${\frac {1}{|a|}}\,\operatorname {tri} \left({\frac {\omega }{2\pi a}}\right)$ | The function `tri(x)` is the [[triangular function]] | | 204 | $\operatorname {tri} (ax)$ | ${\frac {1}{|a|}}\,\operatorname {sinc} ^{2}\left({\frac {\xi }{a}}\right)$ | ${\frac {1}{\sqrt {2\pi a^{2}}}}\,\operatorname {sinc} ^{2}\left({\frac {\omega }{2\pi a}}\right)$ | ${\frac {1}{|a|}}\,\operatorname {sinc} ^{2}\left({\frac {\omega }{2\pi a}}\right)$ | Dual of rule 203. | | 205 | $e^{-ax}u(x)$ | ${\frac {1}{a+i2\pi \xi }}$ | ${\frac {1}{{\sqrt {2\pi }}(a+i\omega )}}$ | ${\frac {1}{a+i\omega }}$ | The function `u(x)` is the [[Heaviside unit step function]] and `a > 0` . | | 206 | $e^{-\alpha x^{2}}$ | ${\sqrt {\frac {\pi }{\alpha }}}\,e^{-{\frac {(\pi \xi )^{2}}{\alpha }}}$ | ${\frac {1}{\sqrt {2\alpha }}}\,e^{-{\frac {\omega ^{2}}{4\alpha }}}$ | ${\sqrt {\frac {\pi }{\alpha }}}\,e^{-{\frac {\omega ^{2}}{4\alpha }}}$ | This shows that, for the unitary Fourier transforms, the [[Gaussian function]] `e−αx2` is its own Fourier transform for some choice of `α` . For this to be integrable we must have `Re(α) > 0` . | | 208 | $e^{-a|x|}$ | ${\frac {2a}{a^{2}+4\pi ^{2}\xi ^{2}}}$ | ${\sqrt {\frac {2}{\pi }}}\,{\frac {a}{a^{2}+\omega ^{2}}}$ | ${\frac {2a}{a^{2}+\omega ^{2}}}$ | For `Re(a) > 0` . That is, the Fourier transform of a [[two-sided decaying exponential function]] is a [[Lorentzian function]] . | | 209 | $\operatorname {sech} (ax)$ | ${\frac {\pi }{a}}\operatorname {sech} \left({\frac {\pi ^{2}}{a}}\xi \right)$ | ${\frac {1}{a}}{\sqrt {\frac {\pi }{2}}}\operatorname {sech} \left({\frac {\pi }{2a}}\omega \right)$ | ${\frac {\pi }{a}}\operatorname {sech} \left({\frac {\pi }{2a}}\omega \right)$ | [[Hyperbolic secant]] is its own Fourier transform | | 210 | $e^{-{\frac {a^{2}x^{2}}{2}}}H_{n}(ax)$ | ${\frac {{\sqrt {2\pi }}(-i)^{n}}{a}}e^{-{\frac {2\pi ^{2}\xi ^{2}}{a^{2}}}}H_{n}\left({\frac {2\pi \xi }{a}}\right)$ | ${\frac {(-i)^{n}}{a}}e^{-{\frac {\omega ^{2}}{2a^{2}}}}H_{n}\left({\frac {\omega }{a}}\right)$ | ${\frac {(-i)^{n}{\sqrt {2\pi }}}{a}}e^{-{\frac {\omega ^{2}}{2a^{2}}}}H_{n}\left({\frac {\omega }{a}}\right)$ | `Hn` is the `n` th-order [[Hermite polynomial]] . If `a = 1` then the Gauss–Hermite functions are [[eigenfunctions]] of the Fourier transform operator. For a derivation, see Hermite polynomials § Hermite functions as eigenfunctions of the Fourier transform . The formula reduces to 206 for `n = 0` . |

### Distributions, one-dimensional

The Fourier transforms in this table may be found in [Erdélyi (1954)](#CITEREFErdélyi1954) or [Kammler (2000](#CITEREFKammler2000) , appendix).

| | Function | Fourier transform unitary, ordinary frequency | Fourier transform unitary, angular frequency | Fourier transform non-unitary, angular frequency | Remarks | | --- | --- | --- | --- | --- | --- | | | $f(x)$ | ${\begin{aligned}&{\widehat {f}}(\xi )\triangleq {\widehat {f}}_{1}(\xi )\\&=\int _{-\infty }^{\infty }f(x)e^{-i2\pi \xi x}\,dx\end{aligned}}$ | ${\begin{aligned}&{\widehat {f}}(\omega )\triangleq {\widehat {f}}_{2}(\omega )\\&={\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{\infty }f(x)e^{-i\omega x}\,dx\end{aligned}}$ | ${\begin{aligned}&{\widehat {f}}(\omega )\triangleq {\widehat {f}}_{3}(\omega )\\&=\int _{-\infty }^{\infty }f(x)e^{-i\omega x}\,dx\end{aligned}}$ | Definitions | | 301 | $1$ | $\delta (\xi )$ | ${\sqrt {2\pi }}\,\delta (\omega )$ | $2\pi \delta (\omega )$ | The distribution `δ(ξ)` denotes the [[Dirac delta function]] . | | 302 | $\delta (x)$ | $1$ | ${\frac {1}{\sqrt {2\pi }}}$ | $1$ | Dual of rule 301. | | 303 | $e^{iax}$ | $\delta \left(\xi -{\frac {a}{2\pi }}\right)$ | ${\sqrt {2\pi }}\,\delta (\omega -a)$ | $2\pi \delta (\omega -a)$ | This follows from 103 and 301. | | 304 | $\cos(ax)$ | ${\frac {\delta \left(\xi -{\frac {a}{2\pi }}\right)+\delta \left(\xi +{\frac {a}{2\pi }}\right)}{2}}$ | ${\sqrt {2\pi }}\,{\frac {\delta (\omega -a)+\delta (\omega +a)}{2}}$ | $\pi \left(\delta (\omega -a)+\delta (\omega +a)\right)$ | This follows from rules 101 and 303 using [[Euler's formula]] : ⁠ $\cos(ax)={\tfrac {e^{iax}+e^{-iax}}{2}}$ ⁠ . | | 305 | $\sin(ax)$ | ${\frac {\delta \left(\xi -{\frac {a}{2\pi }}\right)-\delta \left(\xi +{\frac {a}{2\pi }}\right)}{2i}}$ | ${\sqrt {2\pi }}\,{\frac {\delta (\omega -a)-\delta (\omega +a)}{2i}}$ | $-i\pi {\bigl (}\delta (\omega -a)-\delta (\omega +a){\bigr )}$ | This follows from 101 and 303 using ⁠ $\sin(ax)={\tfrac {e^{iax}-e^{-iax}}{2i}}$ ⁠ . | | 306 | $\cos \left(ax^{2}\right)$ | ${\sqrt {\frac {\pi }{a}}}\cos \left({\frac {\pi ^{2}\xi ^{2}}{a}}-{\frac {\pi }{4}}\right)$ | ${\frac {1}{\sqrt {2a}}}\cos \left({\frac {\omega ^{2}}{4a}}-{\frac {\pi }{4}}\right)$ | ${\sqrt {\frac {\pi }{a}}}\cos \left({\frac {\omega ^{2}}{4a}}-{\frac {\pi }{4}}\right)$ | This follows from 101 and 207 using ⁠ $\cos(ax^{2})={\tfrac {e^{iax^{2}}+e^{-iax^{2}}}{2}}$ ⁠ . | | 307 | $\sin \left(ax^{2}\right)$ | $-{\sqrt {\frac {\pi }{a}}}\sin \left({\frac {\pi ^{2}\xi ^{2}}{a}}-{\frac {\pi }{4}}\right)$ | ${\frac {-1}{\sqrt {2a}}}\sin \left({\frac {\omega ^{2}}{4a}}-{\frac {\pi }{4}}\right)$ | $-{\sqrt {\frac {\pi }{a}}}\sin \left({\frac {\omega ^{2}}{4a}}-{\frac {\pi }{4}}\right)$ | This follows from 101 and 207 using ⁠ $\sin(ax^{2})={\tfrac {e^{iax^{2}}-e^{-iax^{2}}}{2i}}$ ⁠ . | | 308 | $e^{-\pi i\alpha x^{2}}$ | ${\frac {1}{\sqrt {\alpha }}}\,e^{-i{\frac {\pi }{4}}}e^{i{\frac {\pi \xi ^{2}}{\alpha }}}$ | ${\frac {1}{\sqrt {2\pi \alpha }}}\,e^{-i{\frac {\pi }{4}}}e^{i{\frac {\omega ^{2}}{4\pi \alpha }}}$ | ${\frac {1}{\sqrt {\alpha }}}\,e^{-i{\frac {\pi }{4}}}e^{i{\frac {\omega ^{2}}{4\pi \alpha }}}$ | Here it is assumed $\alpha$ is real. For the case that alpha is complex see table entry 206 above. | | 309 | $x^{n}$ | $\left({\frac {i}{2\pi }}\right)^{n}\delta ^{(n)}(\xi )$ | $i^{n}{\sqrt {2\pi }}\delta ^{(n)}(\omega )$ | $2\pi i^{n}\delta ^{(n)}(\omega )$ | Here, `n` is a [[natural number]] and `δ(n)(ξ)` is the `n` th distribution derivative of the Dirac delta function. This rule follows from rules 107 and 301. Combining this rule with 101, we can transform all [[polynomials]] . | | 310 | $\delta ^{(n)}(x)$ | $(i2\pi \xi )^{n}$ | ${\frac {(i\omega )^{n}}{\sqrt {2\pi }}}$ | $(i\omega )^{n}$ | Dual of rule 309. `δ(n)(ξ)` is the `n` th distribution derivative of the Dirac delta function. This rule follows from 106 and 302. | | 311 | ${\frac {1}{x}}$ | $-i\pi \operatorname {sgn} (\xi )$ | $-i{\sqrt {\frac {\pi }{2}}}\operatorname {sgn} (\omega )$ | $-i\pi \operatorname {sgn} (\omega )$ | Here `sgn(ξ)` is the [[sign function]] . Note that `⁠1/x⁠` is not a distribution. It is necessary to use the [[Cauchy principal value]] when testing against [[Schwartz functions]] . This rule is useful in studying the [[Hilbert transform]] . | | 312 | ${\begin{aligned}&{\frac {1}{x^{n}}}\\&:={\frac {(-1)^{n-1}}{(n-1)!}}{\frac {d^{n}}{dx^{n}}}\log |x|\end{aligned}}$ | $-i\pi {\frac {(-i2\pi \xi )^{n-1}}{(n-1)!}}\operatorname {sgn} (\xi )$ | $-i{\sqrt {\frac {\pi }{2}}}\,{\frac {(-i\omega )^{n-1}}{(n-1)!}}\operatorname {sgn} (\omega )$ | $-i\pi {\frac {(-i\omega )^{n-1}}{(n-1)!}}\operatorname {sgn} (\omega )$ | `⁠1/xn⁠` is the [[homogeneous distribution]] defined by the distributional derivative ${\tfrac {(-1)^{n-1}}{(n-1)!}}{\tfrac {d^{n}}{dx^{n}}}\log |x|$ | | 313 | $|x|^{\alpha }$ | $-{\frac {2\sin \left({\frac {\pi \alpha }{2}}\right)\Gamma (\alpha +1)}{|2\pi \xi |^{\alpha +1}}}$ | ${\frac {-2}{\sqrt {2\pi }}}\,{\frac {\sin \left({\frac {\pi \alpha }{2}}\right)\Gamma (\alpha +1)}{|\omega |^{\alpha +1}}}$ | $-{\frac {2\sin \left({\frac {\pi \alpha }{2}}\right)\Gamma (\alpha +1)}{|\omega |^{\alpha +1}}}$ | This formula is valid for `−1 < α < 0` . For `α > 0` some singular terms arise at the origin that can be found by differentiating 320. If `Re α > −1` , then `|x|α` is a locally integrable function, and so a tempered distribution. The function `α ↦ |x|α` is a holomorphic function from the right half-plane to the space of tempered distributions. It admits a unique meromorphic extension to a tempered distribution, also denoted `|x|α` for `α ≠ −1, −3, ...` (see Homogeneous distribution ). | | | ${\frac {1}{\sqrt {|x|}}}$ | ${\frac {1}{\sqrt {|\xi |}}}$ | ${\frac {1}{\sqrt {|\omega |}}}$ | ${\frac {\sqrt {2\pi }}{\sqrt {|\omega |}}}$ | Special case of 313 | | 314 | $\operatorname {sgn} (x)$ | ${\frac {1}{i\pi \xi }}$ | ${\sqrt {\frac {2}{\pi }}}{\frac {1}{i\omega }}$ | ${\frac {2}{i\omega }}$ | The dual of rule 311. This time the Fourier transforms need to be considered as a [[Cauchy principal value]] . | | 315 | $u(x)$ | ${\frac {1}{2}}\left({\frac {1}{i\pi \xi }}+\delta (\xi )\right)$ | ${\sqrt {\frac {\pi }{2}}}\left({\frac {1}{i\pi \omega }}+\delta (\omega )\right)$ | $\pi \left({\frac {1}{i\pi \omega }}+\delta (\omega )\right)$ | The function `u(x)` is the Heaviside [[unit step function]] ; this follows from rules 101, 301, and 314. | | 316 | $\sum _{n=-\infty }^{\infty }\delta (x-nT)$ | ${\frac {1}{T}}\sum _{k=-\infty }^{\infty }\delta \left(\xi -{\frac {k}{T}}\right)$ | ${\frac {\sqrt {2\pi }}{T}}\sum _{k=-\infty }^{\infty }\delta \left(\omega -{\frac {2\pi k}{T}}\right)$ | ${\frac {2\pi }{T}}\sum _{k=-\infty }^{\infty }\delta \left(\omega -{\frac {2\pi k}{T}}\right)$ | This function is known as the [[Dirac comb]] function. This result can be derived from 302 and 102, together with the fact that as distributions. | | 317 | $J_{0}(x)$ | ${\frac {2\,\operatorname {rect} (\pi \xi )}{\sqrt {1-4\pi ^{2}\xi ^{2}}}}$ | ${\sqrt {\frac {2}{\pi }}}\,{\frac {\operatorname {rect} \left({\frac {\omega }{2}}\right)}{\sqrt {1-\omega ^{2}}}}$ | ${\frac {2\,\operatorname {rect} \left({\frac {\omega }{2}}\right)}{\sqrt {1-\omega ^{2}}}}$ | The function `J0(x)` is the zeroth order [[Bessel function]] of first kind. | | 318 | $J_{n}(x)$ | ${\frac {2(-i)^{n}T_{n}(2\pi \xi )\operatorname {rect} (\pi \xi )}{\sqrt {1-4\pi ^{2}\xi ^{2}}}}$ | ${\sqrt {\frac {2}{\pi }}}{\frac {(-i)^{n}T_{n}(\omega )\operatorname {rect} \left({\frac {\omega }{2}}\right)}{\sqrt {1-\omega ^{2}}}}$ | ${\frac {2(-i)^{n}T_{n}(\omega )\operatorname {rect} \left({\frac {\omega }{2}}\right)}{\sqrt {1-\omega ^{2}}}}$ | This is a generalization of 317. The function `Jn(x)` is the `n` th order [[Bessel function]] of first kind. The function `Tn(x)` is the [[Chebyshev polynomial of the first kind]] . | | 319 | $\log \left|x\right|$ | $-{\frac {1}{2}}{\frac {1}{\left|\xi \right|}}-\gamma \delta \left(\xi \right)$ | $-{\frac {\sqrt {\frac {\pi }{2}}}{\left|\omega \right|}}-{\sqrt {2\pi }}\gamma \delta \left(\omega \right)$ | $-{\frac {\pi }{\left|\omega \right|}}-2\pi \gamma \delta \left(\omega \right)$ | `γ` is the [[Euler–Mascheroni constant]] . It is necessary to use a finite part integral when testing `⁠1/|ξ|⁠` or `⁠1/|ω|⁠` against [[Schwartz functions]] . The details of this might change the coefficient of the delta function. | | 320 | $\left(\mp ix\right)^{-\alpha }$ | ${\frac {\left(2\pi \right)^{\alpha }}{\Gamma \left(\alpha \right)}}u\left(\pm \xi \right)\left(\pm \xi \right)^{\alpha -1}$ | ${\frac {\sqrt {2\pi }}{\Gamma \left(\alpha \right)}}u\left(\pm \omega \right)\left(\pm \omega \right)^{\alpha -1}$ | ${\frac {2\pi }{\Gamma \left(\alpha \right)}}u\left(\pm \omega \right)\left(\pm \omega \right)^{\alpha -1}$ | This formula is valid for `0 < α < 1` . Use differentiation to derive formula for higher exponents. `u` is the Heaviside function. |

### Two-dimensional functions

| | Function | Fourier transform unitary, ordinary frequency | Fourier transform unitary, angular frequency | Fourier transform non-unitary, angular frequency | Remarks | | --- | --- | --- | --- | --- | --- | | 400 | $f(x,y)$ | ${\begin{aligned}&{\widehat {f}}(\xi _{x},\xi _{y})\triangleq \\&\iint f(x,y)e^{-i2\pi (\xi _{x}x+\xi _{y}y)}\,dx\,dy\end{aligned}}$ | ${\begin{aligned}&{\widehat {f}}(\omega _{x},\omega _{y})\triangleq \\&{\frac {1}{2\pi }}\iint f(x,y)e^{-i(\omega _{x}x+\omega _{y}y)}\,dx\,dy\end{aligned}}$ | ${\begin{aligned}&{\widehat {f}}(\omega _{x},\omega _{y})\triangleq \\&\iint f(x,y)e^{-i(\omega _{x}x+\omega _{y}y)}\,dx\,dy\end{aligned}}$ | The variables `ξx` , `ξy` , `ωx` , `ωy` are real numbers. The integrals are taken over the entire plane. | | 401 | $e^{-\pi \left(a^{2}x^{2}+b^{2}y^{2}\right)}$ | ${\frac {1}{|ab|}}e^{-\pi \left({\frac {\xi _{x}^{2}}{a^{2}}}+{\frac {\xi _{y}^{2}}{b^{2}}}\right)}$ | ${\frac {1}{2\pi \,|ab|}}e^{-{\frac {1}{4\pi }}\left({\frac {\omega _{x}^{2}}{a^{2}}}+{\frac {\omega _{y}^{2}}{b^{2}}}\right)}$ | ${\frac {1}{|ab|}}e^{-{\frac {1}{4\pi }}\left({\frac {\omega _{x}^{2}}{a^{2}}}+{\frac {\omega _{y}^{2}}{b^{2}}}\right)}$ | Both functions are Gaussians, which may not have unit volume. | | 402 | $\operatorname {circ} \left({\sqrt {x^{2}+y^{2}}}\right)$ | ${\frac {J_{1}\left(2\pi {\sqrt {\xi _{x}^{2}+\xi _{y}^{2}}}\right)}{\sqrt {\xi _{x}^{2}+\xi _{y}^{2}}}}$ | ${\frac {J_{1}\left({\sqrt {\omega _{x}^{2}+\omega _{y}^{2}}}\right)}{\sqrt {\omega _{x}^{2}+\omega _{y}^{2}}}}$ | ${\frac {2\pi J_{1}\left({\sqrt {\omega _{x}^{2}+\omega _{y}^{2}}}\right)}{\sqrt {\omega _{x}^{2}+\omega _{y}^{2}}}}$ | The function is defined by `circ(r) = 1` for `0 ≤ r ≤ 1` , and is 0 otherwise. The result is the amplitude distribution of the [[Airy disk]] , and is expressed using `J1` (the order-1 [[Bessel function]] of the first kind). | | 403 | ${\frac {1}{\sqrt {x^{2}+y^{2}}}}$ | ${\frac {1}{\sqrt {\xi _{x}^{2}+\xi _{y}^{2}}}}$ | ${\frac {1}{\sqrt {\omega _{x}^{2}+\omega _{y}^{2}}}}$ | ${\frac {2\pi }{\sqrt {\omega _{x}^{2}+\omega _{y}^{2}}}}$ | This is the [[Hankel transform]] of `r−1` , a 2-D Fourier "self-transform". | | 404 | ${\frac {i}{x+iy}}$ | ${\frac {1}{\xi _{x}+i\xi _{y}}}$ | ${\frac {1}{\omega _{x}+i\omega _{y}}}$ | ${\frac {2\pi }{\omega _{x}+i\omega _{y}}}$ | |

### Formulas for general `n` -dimensional functions

| | Function | Fourier transform unitary, ordinary frequency | Fourier transform unitary, angular frequency | Fourier transform non-unitary, angular frequency | Remarks | | --- | --- | --- | --- | --- | --- | | 500 | $f(\mathbf {x} )$ | ${\begin{aligned}&{\widehat {f}}_{1}({\boldsymbol {\xi }})\triangleq \\&\int _{\mathbb {R} ^{n}}f(\mathbf {x} )e^{-i2\pi {\boldsymbol {\xi }}\cdot \mathbf {x} }\,d\mathbf {x} \end{aligned}}$ | ${\begin{aligned}&{\widehat {f}}_{2}({\boldsymbol {\omega }})\triangleq \\&{\frac {1}{{(2\pi )}^{\frac {n}{2}}}}\int _{\mathbb {R} ^{n}}f(\mathbf {x} )e^{-i{\boldsymbol {\omega }}\cdot \mathbf {x} }\,d\mathbf {x} \end{aligned}}$ | ${\begin{aligned}&{\widehat {f}}_{3}({\boldsymbol {\omega }})\triangleq \\&\int _{\mathbb {R} ^{n}}f(\mathbf {x} )e^{-i{\boldsymbol {\omega }}\cdot \mathbf {x} }\,d\mathbf {x} \end{aligned}}$ | | | 501 | $\chi _{[0,1]}(|\mathbf {x} |)\left(1-|\mathbf {x} |^{2}\right)^{\delta }$ | ${\frac {\Gamma (\delta +1)}{\pi ^{\delta }\,|{\boldsymbol {\xi }}|^{{\frac {n}{2}}+\delta }}}J_{{\frac {n}{2}}+\delta }(2\pi |{\boldsymbol {\xi }}|)$ | $2^{\delta }\,{\frac {\Gamma (\delta +1)}{\left|{\boldsymbol {\omega }}\right|^{{\frac {n}{2}}+\delta }}}J_{{\frac {n}{2}}+\delta }(|{\boldsymbol {\omega }}|)$ | ${\frac {\Gamma (\delta +1)}{\pi ^{\delta }}}\left|{\frac {\boldsymbol {\omega }}{2\pi }}\right|^{-{\frac {n}{2}}-\delta }J_{{\frac {n}{2}}+\delta }(\!|{\boldsymbol {\omega }}|\!)$ | The function `χ[0, 1]` is the [[indicator function]] of the interval `[0, 1]` . The function `Γ(x)` is the gamma function. The function `J⁠n/2⁠+δ` is a Bessel function of the first kind, with order `⁠n/2⁠ + δ` . Taking `n = 2` and `δ = 0` produces 402. | | 502 | $|\mathbf {x} |^{-\alpha },\quad 0<\operatorname {Re} \alpha ${\frac {(2\pi )^{\alpha }}{c_{n,\alpha }}}|{\boldsymbol {\xi }}|^{-(n-\alpha )}$ | ${\frac {(2\pi )^{\frac {n}{2}}}{c_{n,\alpha }}}|{\boldsymbol {\omega }}|^{-(n-\alpha )}$ | ${\frac {(2\pi )^{n}}{c_{n,\alpha }}}|{\boldsymbol {\omega }}|^{-(n-\alpha )}$ | See Riesz potential , where the constant is given by ⁠ $\textstyle c_{n,\alpha }=\pi ^{\tfrac {n}{2}}2^{\alpha }{\Gamma \left({\frac {\alpha }{2}}\right)}/{\Gamma \left({\frac {n-\alpha }{2}}\right)}$ ⁠ . The formula also holds for all `α ≠ n, n + 2, ...` by analytic continuation, but then the function and its Fourier transforms need to be understood as suitably regularized tempered distributions (see Homogeneous distribution ). | | | 503 | ${\frac {1}{\left|{\boldsymbol {\sigma }}\right|\left(2\pi \right)^{\frac {n}{2}}}}e^{-{\frac {1}{2}}\mathbf {x} ^{\mathrm {T} }{\boldsymbol {\sigma }}^{-\mathrm {T} }{\boldsymbol {\sigma }}^{-1}\mathbf {x} }$ | $e^{-2\pi ^{2}{\boldsymbol {\xi }}^{\mathrm {T} }{\boldsymbol {\sigma }}{\boldsymbol {\sigma }}^{\mathrm {T} }{\boldsymbol {\xi }}}$ | $(2\pi )^{-{\frac {n}{2}}}e^{-{\frac {1}{2}}{\boldsymbol {\omega }}^{\mathrm {T} }{\boldsymbol {\sigma }}{\boldsymbol {\sigma }}^{\mathrm {T} }{\boldsymbol {\omega }}}$ | $e^{-{\frac {1}{2}}{\boldsymbol {\omega }}^{\mathrm {T} }{\boldsymbol {\sigma }}{\boldsymbol {\sigma }}^{\mathrm {T} }{\boldsymbol {\omega }}}$ | This is the formula for a [[multivariate normal distribution]] normalized to 1 with a mean of 0. Bold variables are vectors or matrices. Following the notation of the aforementioned page, `Σ = σ σT` and `Σ−1 = σ−T σ−1` | | 504 | $e^{-2\pi \alpha |\mathbf {x} |}$ | ${\frac {c_{n}\alpha }{\left(\alpha ^{2}+|{\boldsymbol {\xi }}|^{2}\right)^{\frac {n+1}{2}}}}$ | ${\frac {c_{n}(2\pi )^{\frac {n+2}{2}}\alpha }{\left(4\pi ^{2}\alpha ^{2}+|{\boldsymbol {\omega }}|^{2}\right)^{\frac {n+1}{2}}}}$ | ${\frac {c_{n}(2\pi )^{n+1}\alpha }{\left(4\pi ^{2}\alpha ^{2}+|{\boldsymbol {\omega }}|^{2}\right)^{\frac {n+1}{2}}}}$ | Here ⁠ $\textstyle c_{n}={\Gamma \left({\frac {n+1}{2}}\right)}/{\pi ^{\frac {n+1}{2}}}$ ⁠ , `Re(α) > 0` |

## See also

- [[Analog signal processing]] – Signal processing conducted on analog signals - [[Beevers–Lipson strip]] – Mathematical tool in crystallography - [[Constant-Q transform]] – Short-time Fourier transform with variable resolution - [[DFT matrix]] – Discrete fourier transform expressed as a matrix - [[Discrete Fourier transform]] – Function in discrete mathematics - [[Fast Fourier transform]] – Discrete Fourier transform algorithm - [[Fourier integral operator]] – Class of differential and integral operators - [[Fourier inversion theorem]] – Mathematical theorem about functions - [[Fourier multiplier]] – Type of operator in Fourier analysis Pages displaying short descriptions of redirect targets - [[Fourier series]] – Decomposition of periodic functions - [[Fourier sine transform]] – Variant Fourier transforms Pages displaying short descriptions of redirect targets - [[Fourier–Deligne transform]] - [[Fourier–Mukai transform]] - [[Fractional Fourier transform]] – Mathematical operation - [[Indirect Fourier transform]] - [[Integral transform]] – Mapping involving integration between function spaces - [[Hankel transform]] – Mathematical operation - [[Hartley transform]] – Integral transform closely related to the Fourier transform - [[Laplace transform]] – Integral transform useful in probability theory, physics, and engineering - [[Least-squares spectral analysis]] – Periodicity computation method - [[Linear canonical transform]] - [[List of Fourier-related transforms]] - [[Mellin transform]] – Mathematical operation - [[Multidimensional transform]] – Mathematical analysis of frequency content of signals - [[NGC 4622]] – Especially the image NGC 4622 Fourier transform `m = 2` . - [[Nonlocal operator]] – Class of operator mapping - [[Quadratic Fourier transform]] - [[Quantum Fourier transform]] – Change of basis applied in quantum computing - [[Short-time Fourier transform]] – Fourier-related transform for signals that change over time - [[Spectral density]] – Relative importance of certain frequencies in a composite signal - [[Spectral density estimation]] – Signal processing technique - [[Symbolic integration]] – Computation of an antiderivatives - [[Time stretch dispersive Fourier transform]] - [[Transform (mathematics)]] – Function that applies a set to itself Pages displaying short descriptions of redirect targets

## Notes

1. **[^](#cite_ref-1)**

 Sentence structure is often sufficient to distinguish the intended meaning: for example, "Apply the Fourier transform to [an input]" refers to the operation, whereas "The Fourier transform of [an input]" refers to its output. 2. **[^](#cite_ref-2)**

 Depending on the application a [[Lebesgue integral]] , [[distributional]] , or other approach may be most appropriate. 3. **[^](#cite_ref-3)**

 [Vretblad (2000)](#CITEREFVretblad2000) provides solid justification for these formal procedures without going too deeply into [[functional analysis]] or the [[theory of distributions]] . 4. **[^](#cite_ref-4)**

 In [[relativistic quantum mechanics]] one encounters vector-valued Fourier transforms of multi-component wave functions. In [[quantum field theory]] , operator-valued Fourier transforms of operator-valued functions of spacetime are in frequent use, see for example [Greiner & Reinhardt (1996)](#CITEREFGreinerReinhardt1996) . 5. **[^](#cite_ref-18)**

 A possible source of confusion is the [frequency-shifting property](#Frequency_shifting) ; i.e. the transform of function $f(x)e^{-i2\pi \xi _{0}x}$ is ⁠ ${\widehat {f}}(\xi +\xi _{0})$ ⁠ . The value of this function at $\xi =0$ is ⁠ ${\widehat {f}}(\xi _{0})$ ⁠ , meaning that a frequency $\xi _{0}$ has been shifted to zero (also see Negative frequency § Simplifying the Fourier transform ). 6. **[^](#cite_ref-27)**

 The operator is defined by replacing $x$ by in the [[Taylor expansion]] of ⁠ $U(x)$ ⁠ . 7. **[^](#cite_ref-61)**

 More generally, one can take a sequence of functions that are in the intersection of `L1` and `L2` and that converges to `f` in the `L2` -norm, and define the Fourier transform of `f` as the `L2` -limit of the Fourier transforms of these functions. 8. **[^](#cite_ref-78)**

 Up to an imaginary constant factor whose magnitude depends on what Fourier transform convention is used. 9. **[^](#cite_ref-83)**

 For example, to compute the Fourier transform of `cos(6πt) e−πt2` one might enter the command `integrate cos(6*pi*t) exp(−pi*t^2) exp(-i*2*pi*f*t) from -inf to inf` into [[Wolfram Alpha]] . The direct command `fourier transform of cos(6*pi*t) exp(−pi*t^2)` would also work for Wolfram Alpha, although the options for the convention (see § Other conventions ) must be changed away from the default option, which is actually equivalent to `integrate cos(6*pi*t) exp(−pi*t^2) exp(i*omega*t) /sqrt(2*pi) from -inf to inf` . 10. **[^](#cite_ref-92)**

 In [Gelfand & Shilov 1964](#CITEREFGelfandShilov1964) , p. 363, with the non-unitary conventions of this table, the transform of $|\mathbf {x} |^{\lambda }$ is given to be ⁠ $\textstyle 2^{\lambda +n}\pi ^{{\tfrac {1}{2}}n}{\Gamma ({\frac {\lambda +n}{2}})}/{\Gamma (-{\frac {\lambda }{2}})}\vert {\boldsymbol {\omega }}\vert ^{-\lambda -n}$ ⁠ from which this follows, with ⁠ $\lambda =-\alpha$ ⁠ .

## Citations

1. **[^](#cite_ref-FOOTNOTEPinsky200291_5-0)**

 [Pinsky 2002](#CITEREFPinsky2002) , p. 91 2. **[^](#cite_ref-FOOTNOTELiebLoss2001123–125_6-0)**

 [Lieb & Loss 2001](#CITEREFLiebLoss2001) , pp. 123–125 3. **[^](#cite_ref-FOOTNOTEGelfandShilov1968128_7-0)**

 [Gelfand & Shilov 1968](#CITEREFGelfandShilov1968) , p. 128 4. **[^](#cite_ref-8)**

 [Fourier 1822](#CITEREFFourier1822) , p. 525 5. **[^](#cite_ref-9)**

 [Fourier 1878](#CITEREFFourier1878) , p. 408 6. **[^](#cite_ref-10)**

 [Jordan 1883](#CITEREFJordan1883) proves on pp. 216–226 the [[Fourier integral theorem]] before studying Fourier series. 7. **[^](#cite_ref-11)**

 [Titchmarsh 1986](#CITEREFTitchmarsh1986) , p. 1 8. **[^](#cite_ref-12)**

 [Rahman 2011](#CITEREFRahman2011) , p. 10 9. **[^](#cite_ref-13)**

 [Oppenheim, Schafer & Buck 1999](#CITEREFOppenheimSchaferBuck1999) , p. 58 10. **[^](#cite_ref-FOOTNOTEStade2005298–299_14-0)**

 [Stade 2005](#CITEREFStade2005) , pp. 298–299 11. **[^](#cite_ref-FOOTNOTEHowe1980_15-0)**

 [Howe 1980](#CITEREFHowe1980) 12. **[^](#cite_ref-16)**

 [Folland 1989](#CITEREFFolland1989) 13. **[^](#cite_ref-17)**

 [Fourier 1822](#CITEREFFourier1822) 14. **[^](#cite_ref-19)**

 [Arfken 1985](#CITEREFArfken1985) 15. ^ [a](#cite_ref-Pinsky-2002_20-0) [b](#cite_ref-Pinsky-2002_20-1)

 [Pinsky 2002](#CITEREFPinsky2002) 16. **[^](#cite_ref-FOOTNOTEProakisManolakis1996[httpsarchiveorgdetailsdigitalsignalpro00proapage291_291]_21-0)**

 [Proakis & Manolakis 1996](#CITEREFProakisManolakis1996) , p. [291](https://archive.org/details/digitalsignalpro00proa/page/291) 17. **[^](#cite_ref-FOOTNOTEKatznelson2004153_22-0)**

 [Katznelson 2004](#CITEREFKatznelson2004) , p. 153 18. **[^](#cite_ref-FOOTNOTESteinWeiss19712_23-0)**

 [Stein & Weiss 1971](#CITEREFSteinWeiss1971) , p. 2 19. ^ [a](#cite_ref-Stein-Weiss-1971_24-0) [b](#cite_ref-Stein-Weiss-1971_24-1) [c](#cite_ref-Stein-Weiss-1971_24-2) [d](#cite_ref-Stein-Weiss-1971_24-3) [e](#cite_ref-Stein-Weiss-1971_24-4) [f](#cite_ref-Stein-Weiss-1971_24-5)

 [Stein & Weiss 1971](#CITEREFSteinWeiss1971) 20. **[^](#cite_ref-25)**

 [Rudin 1987](#CITEREFRudin1987) , p. 187 21. **[^](#cite_ref-26)**

 [Rudin 1987](#CITEREFRudin1987) , p. 186 22. **[^](#cite_ref-28)**

 [Folland 1992](#CITEREFFolland1992) , p. 216 23. **[^](#cite_ref-29)**

 [Wolf 1979](#CITEREFWolf1979) , p. 307ff 24. **[^](#cite_ref-30)**

 [Folland 1989](#CITEREFFolland1989) , p. 53 25. **[^](#cite_ref-31)**

 [Celeghini, Gadella & del Olmo 2021](#CITEREFCeleghiniGadelladel_Olmo2021) 26. **[^](#cite_ref-Duoandikoetxea-2001_32-0)**

 [Duoandikoetxea 2001](#CITEREFDuoandikoetxea2001) 27. ^ [a](#cite_ref-Boashash-2003_33-0) [b](#cite_ref-Boashash-2003_33-1)

 [Boashash 2003](#CITEREFBoashash2003) 28. **[^](#cite_ref-34)**

 [Condon 1937](#CITEREFCondon1937) 29. **[^](#cite_ref-35)**

 [Wolf 1979](#CITEREFWolf1979) , p. 320 30. ^ [a](#cite_ref-auto_36-0) [b](#cite_ref-auto_36-1)

 [Wolf 1979](#CITEREFWolf1979) , p. 312 31. **[^](#cite_ref-37)**

 [Folland 1989](#CITEREFFolland1989) , p. 52 32. **[^](#cite_ref-38)**

 [Howe 1980](#CITEREFHowe1980) 33. **[^](#cite_ref-39)**

 [Paley & Wiener 1934](#CITEREFPaleyWiener1934) 34. **[^](#cite_ref-40)**

 [Gelfand & Vilenkin 1964](#CITEREFGelfandVilenkin1964) 35. **[^](#cite_ref-41)**

 [Kirillov & Gvishiani 1982](#CITEREFKirillovGvishiani1982) 36. **[^](#cite_ref-42)**

 [Clozel & Delorme 1985](#CITEREFClozelDelorme1985) , pp. 331–333 37. **[^](#cite_ref-43)**

 [de Groot & Mazur 1984](#CITEREFde_GrootMazur1984) , p. 146 38. **[^](#cite_ref-44)**

 [Champeney 1987](#CITEREFChampeney1987) , p. 80 39. ^ [a](#cite_ref-Kolmogorov-Fomin-1999_45-0) [b](#cite_ref-Kolmogorov-Fomin-1999_45-1) [c](#cite_ref-Kolmogorov-Fomin-1999_45-2)

 [Kolmogorov & Fomin 1999](#CITEREFKolmogorovFomin1999) 40. **[^](#cite_ref-46)**

 [Wiener 1949](#CITEREFWiener1949) 41. **[^](#cite_ref-47)**

 [Champeney 1987](#CITEREFChampeney1987) , p. 63 42. **[^](#cite_ref-48)**

 [Widder & Wiener 1938](#CITEREFWidderWiener1938) , p. 537 43. **[^](#cite_ref-49)**

 [Pinsky 2002](#CITEREFPinsky2002) , chpt. 2.4.3 The Uncertainty Principle 44. **[^](#cite_ref-50)**

 [Stein & Shakarchi 2003](#CITEREFSteinShakarchi2003) , chpt. 5.4 The Heisenberg uncertainty principle 45. **[^](#cite_ref-51)**

 [Chatfield 2004](#CITEREFChatfield2004) , p. 113 46. **[^](#cite_ref-52)**

 [Fourier 1822](#CITEREFFourier1822) , p. 441 47. **[^](#cite_ref-53)**

 [Poincaré 1895](#CITEREFPoincaré1895) , p. 102 48. **[^](#cite_ref-54)**

 [Whittaker & Watson 1927](#CITEREFWhittakerWatson1927) , p. 188 49. **[^](#cite_ref-55)**

 [Grafakos 2004](#CITEREFGrafakos2004) 50. **[^](#cite_ref-56)**

 [Grafakos & Teschl 2013](#CITEREFGrafakosTeschl2013) 51. **[^](#cite_ref-57)**

 [Duoandikoetxea 2001](#CITEREFDuoandikoetxea2001) , Thm. 8.3 52. **[^](#cite_ref-FOOTNOTESteinWeiss19711–2_58-0)**

 [Stein & Weiss 1971](#CITEREFSteinWeiss1971) , pp. 1–2 53. **[^](#cite_ref-FOOTNOTERudin1987182–183_59-0)**

 [Rudin 1987](#CITEREFRudin1987) , pp. 182–183 54. **[^](#cite_ref-FOOTNOTEChandrasekharan19897–8,_84_60-0)**

 [Chandrasekharan 1989](#CITEREFChandrasekharan1989) , pp. 7–8, 84 55. **[^](#cite_ref-62)**

 ["Applied Fourier Analysis and Elements of Modern Signal Processing Lecture 3"](https://web.archive.org/web/20201003042302/https://statweb.stanford.edu/~candes/teaching/math262/Lectures/Lecture03.pdf)

 (PDF) . January 12, 2016. Archived from [the original](https://statweb.stanford.edu/~candes/teaching/math262/Lectures/Lecture03.pdf)

 (PDF) on 2020-10-03 . Retrieved 2019-10-11 . 56. **[^](#cite_ref-FOOTNOTESteinWeiss1971Thm._2.3_63-0)**

 [Stein & Weiss 1971](#CITEREFSteinWeiss1971) , Thm. 2.3 57. ^ [a](#cite_ref-FOOTNOTEKatznelson2004_64-0) [b](#cite_ref-FOOTNOTEKatznelson2004_64-1)

 [Katznelson 2004](#CITEREFKatznelson2004) 58. **[^](#cite_ref-FOOTNOTEMallat200945_65-0)**

 [Mallat 2009](#CITEREFMallat2009) , p. 45 59. **[^](#cite_ref-FOOTNOTEStrichartz1994150_66-0)**

 [Strichartz 1994](#CITEREFStrichartz1994) , p. 150 60. **[^](#cite_ref-FOOTNOTEHunter2014_67-0)**

 [Hunter 2014](#CITEREFHunter2014) 61. **[^](#cite_ref-FOOTNOTEPinsky2002256_68-0)**

 [Pinsky 2002](#CITEREFPinsky2002) , p. 256 62. **[^](#cite_ref-FOOTNOTERudin199115_69-0)**

 [Rudin 1991](#CITEREFRudin1991) , p. 15 63. **[^](#cite_ref-FOOTNOTEEdwards198253,_67,_72–73_70-0)**

 [Edwards 1982](#CITEREFEdwards1982) , pp. 53, 67, 72–73 64. **[^](#cite_ref-71)**

 [Katznelson 2004](#CITEREFKatznelson2004) , p. 173The typical conventions in probability theory take `eiξx` instead of `e−i2πξx` . 65. **[^](#cite_ref-FOOTNOTEBillingsley1995345_72-0)**

 [Billingsley 1995](#CITEREFBillingsley1995) , p. 345 66. **[^](#cite_ref-FOOTNOTEKatznelson200440,_155,_164_73-0)**

 [Katznelson 2004](#CITEREFKatznelson2004) , pp. 40, 155, 164 67. **[^](#cite_ref-FOOTNOTEEdwards198253_74-0)**

 [Edwards 1982](#CITEREFEdwards1982) , p. 53 68. **[^](#cite_ref-75)**

 [Hewitt & Ross 1970](#CITEREFHewittRoss1970) , Chapter 8 69. **[^](#cite_ref-76)**

 [Knapp 2001](#CITEREFKnapp2001) 70. **[^](#cite_ref-FOOTNOTECorreiaJustoAngélico2024_77-0)**

 [Correia, Justo & Angélico 2024](#CITEREFCorreiaJustoAngélico2024) 71. **[^](#cite_ref-FOOTNOTEAblowitzKaupNewellSegur1974249–315_79-0)**

 [Ablowitz et al. 1974](#CITEREFAblowitzKaupNewellSegur1974) , pp. 249–315 72. **[^](#cite_ref-FOOTNOTELax1968467–490_80-0)**

 [Lax 1968](#CITEREFLax1968) , pp. 467–490 73. **[^](#cite_ref-FOOTNOTEYousefiKschischang20144312–4328_81-0)**

 [Yousefi & Kschischang 2014](#CITEREFYousefiKschischang2014) , pp. 4312–4328 74. **[^](#cite_ref-Zwillinger-2014_82-0)**

 [Gradshteyn et al. 2015](#CITEREFGradshteynRyzhikGeronimusTseytlin2015) 75. **[^](#cite_ref-84)**

 [Press et al. 1992](#CITEREFPressFlanneryTeukolskyVetterling1992) 76. **[^](#cite_ref-85)**

 [Bailey & Swarztrauber 1994](#CITEREFBaileySwarztrauber1994) 77. **[^](#cite_ref-86)**

 [Lado 1971](#CITEREFLado1971) 78. **[^](#cite_ref-87)**

 [Simonen & Olkkonen 1985](#CITEREFSimonenOlkkonen1985) 79. **[^](#cite_ref-88)**

 ["The Integration Property of the Fourier Transform"](https://www.thefouriertransform.com/transform/integration.php) . The Fourier Transform .com . 2015 [2010]. [Archived](https://web.archive.org/web/20220126171340/https://www.thefouriertransform.com/transform/integration.php) from the original on 2022-01-26 . Retrieved 2023-08-20 . 80. **[^](#cite_ref-89)**

 [Stein & Weiss 1971](#CITEREFSteinWeiss1971) , Thm. IV.3.3 81. **[^](#cite_ref-90)**

 [Easton 2010](#CITEREFEaston2010) 82. **[^](#cite_ref-91)**

 [Stein & Weiss 1971](#CITEREFSteinWeiss1971) , Thm. 4.15 83. **[^](#cite_ref-93)**

 [Stein & Weiss 1971](#CITEREFSteinWeiss1971) , p. 6

## References

- Ablowitz, Mark J.; Kaup, David J.; Newell, Alan C.; Segur, Harvey (1974). ["The Inverse Scattering Transform‐Fourier Analysis for Nonlinear Problems"](https://onlinelibrary.wiley.com/doi/10.1002/sapm1974534249) . Studies in Applied Mathematics . **53** (4): 249– 315. [[doi]] : [10.1002/sapm1974534249](https://doi.org/10.1002%2Fsapm1974534249) . [[ISSN]] [0022-2526](https://search.worldcat.org/issn/0022-2526)

 . Retrieved 2025-09-21 . - Arfken, George (1985), Mathematical Methods for Physicists (3rd ed.), Academic Press, [[ISBN]] [[978-0-12-059820-5]] - Bailey, David H.; Swarztrauber, Paul N. (1994), ["A fast method for the numerical evaluation of continuous Fourier and Laplace transforms"](https://web.archive.org/web/20080720002714/http://crd.lbl.gov/~dhbailey/dhbpapers/fourint.pdf)

 (PDF) , SIAM Journal on Scientific Computing , **15** (5): 1105– 1110, [[Bibcode]] : [1994SJSC...15.1105B](https://ui.adsabs.harvard.edu/abs/1994SJSC...15.1105B) , [[CiteSeerX]] [10.1.1.127.1534](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.127.1534) , [[doi]] : [10.1137/0915067](https://doi.org/10.1137%2F0915067) , archived from [the original](http://crd.lbl.gov/~dhbailey/dhbpapers/fourint.pdf)

 (PDF) on 2008-07-20 , retrieved 2017-11-01 - Billingsley, Patrick (1995), Probability and measure , New York, NY: Wiley, [[ISBN]] [[978-0-471-00710-4]] - Boashash, B., ed. (2003), Time–Frequency Signal Analysis and Processing: A Comprehensive Reference , Oxford: Elsevier Science, [[ISBN]] [[978-0-08-044335-5]] - [[Bochner, S.]] ; [[Chandrasekharan, K.]] (1949), Fourier Transforms , [[Princeton University Press]] - Bracewell, R. N. (2000), The Fourier Transform and Its Applications (3rd ed.), Boston: McGraw-Hill, [[ISBN]] [[978-0-07-116043-8]] - Campbell, George; Foster, Ronald (1948), Fourier Integrals for Practical Applications , New York: D. Van Nostrand Company, Inc. - Celeghini, Enrico; Gadella, Manuel; del Olmo, Mariano A. (2021), "Hermite Functions and Fourier Series", Symmetry , **13** (5): 853, [[arXiv]] : [2007.10406](https://arxiv.org/abs/2007.10406) , [[Bibcode]] : [2021Symm...13..853C](https://ui.adsabs.harvard.edu/abs/2021Symm...13..853C) , [[doi]] : [10.3390/sym13050853](https://doi.org/10.3390%2Fsym13050853) - Champeney, D.C. (1987), A Handbook of Fourier Theorems , [[Cambridge University Press]] , [[Bibcode]] : [1987hft..book.....C](https://ui.adsabs.harvard.edu/abs/1987hft..book.....C) - Chandrasekharan, Komaravolu (1989), [Classical Fourier Transforms](http://link.springer.com/10.1007/978-3-642-74029-9) , Berlin, Heidelberg: Springer Berlin Heidelberg, [[doi]] : [10.1007/978-3-642-74029-9](https://doi.org/10.1007%2F978-3-642-74029-9) , [[ISBN]] [[978-3-540-50248-7]] - Chatfield, Chris (2004), [The Analysis of Time Series: An Introduction](https://books.google.com/books?id=qKzyAbdaDFAC&q=%22Fourier+transform%22) , Texts in Statistical Science (6th ed.), London: Chapman & Hall/CRC, [[ISBN]] [[978-0-203-49168-3]] - Clozel, Laurent; Delorme, Patrice (1985), "Sur le théorème de Paley-Wiener invariant pour les groupes de Lie réductifs réels", Comptes Rendus de l'Académie des Sciences, Série I , **300** : 331– 333 - [[Condon, E. U.]] (1937), "Immersion of the Fourier transform in a continuous group of functional transformations", Proc. Natl. Acad. Sci. , **23** (3): 158– 164, [[Bibcode]] : [1937PNAS...23..158C](https://ui.adsabs.harvard.edu/abs/1937PNAS...23..158C) , [[doi]] : [10.1073/pnas.23.3.158](https://doi.org/10.1073%2Fpnas.23.3.158) , [[PMC]] [1076889](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1076889) , [[PMID]] [16588141](https://pubmed.ncbi.nlm.nih.gov/16588141) - Correia, L. B.; Justo, J. F.; Angélico, B. A. (2024). "Polynomial Adaptive Synchrosqueezing Fourier Transform: A method to optimize multiresolution". Digital Signal Processing . **150** 104526. [[Bibcode]] : [2024DSPRJ.15004526C](https://ui.adsabs.harvard.edu/abs/2024DSPRJ.15004526C) . [[doi]] : [10.1016/j.dsp.2024.104526](https://doi.org/10.1016%2Fj.dsp.2024.104526) . - de Groot, Sybren R.; Mazur, Peter (1984), Non-Equilibrium Thermodynamics (2nd ed.), New York: [[Dover]] - Duoandikoetxea, Javier (2001), Fourier Analysis , [[American Mathematical Society]] , [[ISBN]] [[978-0-8218-2172-5]] - [[Dym, H.]] ; McKean, H. (1985), Fourier Series and Integrals , [[Academic Press]] , [[ISBN]] [[978-0-12-226451-1]] - Easton, Roger L. Jr. (2010), [Fourier Methods in Imaging](https://books.google.com/books?id=wCoDDQAAQBAJ) , John Wiley & Sons, [[ISBN]] [[978-0-470-68983-7]] , retrieved 26 May 2020 - Edwards, R. E. (1979). Fourier Series . Graduate Texts in Mathematics. Vol. 64. New York, NY: Springer New York. [[doi]] : [10.1007/978-1-4612-6208-4](https://doi.org/10.1007%2F978-1-4612-6208-4) . [[ISBN]] [[978-1-4612-6210-7]] . - Edwards, R. E. (1982). Fourier Series . Graduate Texts in Mathematics. Vol. 85. New York, NY: Springer New York. [[doi]] : [10.1007/978-1-4613-8156-3](https://doi.org/10.1007%2F978-1-4613-8156-3) . [[ISBN]] [[978-1-4613-8158-7]] . - Erdélyi, Arthur, ed. (1954), Tables of Integral Transforms , vol. 1, McGraw-Hill - [[Feller, William]] (1971), An Introduction to Probability Theory and Its Applications , vol. II (2nd ed.), New York: [[Wiley]] , [[MR]] [0270403](https://mathscinet.ams.org/mathscinet-getitem?mr=0270403) - Folland, Gerald (1989), Harmonic analysis in phase space , [[Princeton University Press]] - Folland, Gerald (1992), Fourier analysis and its applications , [[Wadsworth & Brooks/Cole]] - [[Fourier, J.B. Joseph]] (1822), [Théorie analytique de la chaleur](https://books.google.com/books?id=TDQJAAAAIAAJ&q=%22c%27est-%C3%A0-dire+qu%27on+a+l%27%C3%A9quation%22&pg=PA525) (in French), Paris: Firmin Didot, père et fils, [[OCLC]] [2688081](https://search.worldcat.org/oclc/2688081) - [[Fourier, J.B. Joseph]] (1878) [1822], ["The Analytical Theory of Heat"](https://books.google.com/books?id=-N8EAAAAYAAJ&q=%22that+is+to+say%2C+that+we+have+the+equation%22&pg=PA408) , Nature , **18** (451), translated by Alexander Freeman, The University Press: 192, [[Bibcode]] : [1878Natur..18Q.192.](https://ui.adsabs.harvard.edu/abs/1878Natur..18Q.192.) , [[doi]] : [10.1038/018192a0](https://doi.org/10.1038%2F018192a0)

 (translated from French) - [[Gradshteyn, Izrail Solomonovich]] ; [[Ryzhik, Iosif Moiseevich]] ; [[Geronimus, Yuri Veniaminovich]] ; [[Tseytlin, Michail Yulyevich]] ; Jeffrey, Alan (2015), Zwillinger, Daniel; [[Moll, Victor Hugo]] (eds.), [[Table of Integrals, Series, and Products]] , translated by Scripta Technica, Inc. (8th ed.), [[Academic Press]] , [[ISBN]] [[978-0-12-384933-5]] - Grafakos, Loukas (2004), Classical and Modern Fourier Analysis , Prentice-Hall, [[ISBN]] [[978-0-13-035399-3]] - Grafakos, Loukas; [[Teschl, Gerald]] (2013), "On Fourier transforms of radial functions and distributions", J. Fourier Anal. Appl. , **19** (1): 167– 179, [[arXiv]] : [1112.5469](https://arxiv.org/abs/1112.5469) , [[Bibcode]] : [2013JFAA...19..167G](https://ui.adsabs.harvard.edu/abs/2013JFAA...19..167G) , [[doi]] : [10.1007/s00041-012-9242-5](https://doi.org/10.1007%2Fs00041-012-9242-5) , [[S2CID]] [1280745](https://api.semanticscholar.org/CorpusID:1280745) - Greiner, W.; Reinhardt, J. (1996), [Field Quantization](https://archive.org/details/fieldquantizatio0000grei) , [[Springer]] , [[ISBN]] [[978-3-540-59179-5]] - [[Gelfand, I.M.]] ; [[Shilov, G.E.]] (1964), Generalized Functions , vol. 1, New York: [[Academic Press]]

 (translated from Russian) - [[Gelfand, I.M.]] ; [[Shilov, G.E.]] (1968), Generalized Functions , vol. 2, New York: [[Academic Press]]

 (translated from Russian) - [[Gelfand, I.M.]] ; [[Vilenkin, N.Y.]] (1964), Generalized Functions , vol. 4, New York: [[Academic Press]]

 (translated from Russian) - Hewitt, Edwin; Ross, Kenneth A. (1970), Abstract harmonic analysis: Structure and analysis for compact groups. Analysis on locally compact Abelian groups , Die Grundlehren der mathematischen Wissenschaften, Band 152, vol. II, [[Springer]] , [[MR]] [0262773](https://mathscinet.ams.org/mathscinet-getitem?mr=0262773) - [[Hörmander, L.]] (1976), Linear Partial Differential Operators , vol. 1, [[Springer]] , [[ISBN]] [[978-3-540-00662-6]] - Howe, Roger (1980), "On the role of the Heisenberg group in harmonic analysis", Bulletin of the American Mathematical Society , **3** (2): 821– 844, [[doi]] : [10.1090/S0273-0979-1980-14825-9](https://doi.org/10.1090%2FS0273-0979-1980-14825-9) , [[MR]] [0578375](https://mathscinet.ams.org/mathscinet-getitem?mr=0578375) - Hunter, J.K. (2014), ["Appendix: The Fourier transform"](https://www.math.ucdavis.edu/~hunter/pdes/pdes.html) , Lecture Notes on PDEs , retrieved January 12, 2025 - James, J.F. (2011), A Student's Guide to Fourier Transforms (3rd ed.), [[Cambridge University Press]] , [[Bibcode]] : [2011sgft.book.....J](https://ui.adsabs.harvard.edu/abs/2011sgft.book.....J) , [[ISBN]] [[978-0-521-17683-5]] - [[Jordan, Camille]] (1883), Cours d'Analyse de l'École Polytechnique , vol. II, Calcul Intégral: Intégrales définies et indéfinies (2nd ed.), Paris

 `{{ [[citation]] }}` : CS1 maint: location missing publisher ( [[link]] ) - Kaiser, Gerald (1994), ["A Friendly Guide to Wavelets"](https://books.google.com/books?id=rfRnrhJwoloC&q=%22becomes+the+Fourier+%28integral%29+transform%22&pg=PA29) , Physics Today , **48** (7): 57– 58, [[Bibcode]] : [1995PhT....48g..57K](https://ui.adsabs.harvard.edu/abs/1995PhT....48g..57K) , [[doi]] : [10.1063/1.2808105](https://doi.org/10.1063%2F1.2808105) , [[ISBN]] [[978-0-8176-3711-8]]

 `{{ [[citation]] }}` : CS1 maint: work parameter with ISBN ( [[link]] ) - Kammler, David (2000), A First Course in Fourier Analysis , Prentice Hall, [[ISBN]] [[978-0-13-578782-3]] - Katznelson, Yitzhak (2004), [An Introduction to Harmonic Analysis](https://www.cambridge.org/core/product/identifier/9781139165372/type/book) , Cambridge University Press, [[doi]] : [10.1017/cbo9781139165372](https://doi.org/10.1017%2Fcbo9781139165372) , [[ISBN]] [[978-0-521-83829-0]] - Khare, Kedar; Butola, Mansi; Rajora, Sunaina (2023), "Chapter 2.3 Fourier Transform as a Limiting Case of Fourier Series", Fourier Optics and Computational Imaging (2nd ed.), Springer, [[doi]] : [10.1007/978-3-031-18353-9](https://doi.org/10.1007%2F978-3-031-18353-9) , [[ISBN]] [[978-3-031-18353-9]] , [[S2CID]] [255676773](https://api.semanticscholar.org/CorpusID:255676773) - [[Kirillov, Alexandre]] ; Gvishiani, Alexei D. (1982) [1979], Theorems and Problems in Functional Analysis , [[Springer]]

 (translated from Russian) - Knapp, Anthony W. (2001), [Representation Theory of Semisimple Groups: An Overview Based on Examples](https://books.google.com/books?id=QCcW1h835pwC) , [[Princeton University Press]] , [[ISBN]] [[978-0-691-09089-4]] - [[Kolmogorov, Andrey Nikolaevich]] ; [[Fomin, Sergei Vasilyevich]] (1999) [1957], [Elements of the Theory of Functions and Functional Analysis](http://store.doverpublications.com/0486406830.html) , [[Dover]]

 (translated from Russian) - Lado, F. (1971), ["Numerical Fourier transforms in one, two, and three dimensions for liquid state calculations"](https://www.lib.ncsu.edu/resolver/1840.2/2465) , Journal of Computational Physics , **8** (3): 417– 433, [[Bibcode]] : [1971JCoPh...8..417L](https://ui.adsabs.harvard.edu/abs/1971JCoPh...8..417L) , [[doi]] : [10.1016/0021-9991(71)90021-0](https://doi.org/10.1016%2F0021-9991%2871%2990021-0) - Lax, Peter D. (1968). ["Integrals of nonlinear equations of evolution and solitary waves"](https://www.osti.gov/biblio/4522657) . Communications on Pure and Applied Mathematics . **21** (5): 467– 490. [[doi]] : [10.1002/cpa.3160210503](https://doi.org/10.1002%2Fcpa.3160210503) . [[ISSN]] [0010-3640](https://search.worldcat.org/issn/0010-3640)

 . Retrieved 2025-09-21 . - [[Mallat, Stéphane]] (2009), A wavelet tour of signal processing: the sparse way , Amsterdam Boston: Elsevier/Academic Press, [[doi]] : [10.1016/B978-0-12-374370-1.X0001-8](https://doi.org/10.1016%2FB978-0-12-374370-1.X0001-8) , [[ISBN]] [[978-0-12-374370-1]] - Lieb, Elliott H.; Loss, Michael (2001). Analysis . Providence (R. I.): American Mathematical Soc. [[ISBN]] [[0-8218-2783-9]] . - Müller, Meinard (2015), [The Fourier Transform in a Nutshell.](https://web.archive.org/web/20160408083515/https://www.audiolabs-erlangen.de/content/05-fau/professor/00-mueller/04-bookFMP/2015_Mueller_FundamentalsMusicProcessing_Springer_Section2-1_SamplePages.pdf)

 (PDF) , [[Springer]] , [[doi]] : [10.1007/978-3-319-21945-5](https://doi.org/10.1007%2F978-3-319-21945-5) , [[ISBN]] [[978-3-319-21944-8]] , [[S2CID]] [8691186](https://api.semanticscholar.org/CorpusID:8691186) , archived from [the original](https://www.audiolabs-erlangen.de/content/05-fau/professor/00-mueller/04-bookFMP/2015_Mueller_FundamentalsMusicProcessing_Springer_Section2-1_SamplePages.pdf)

 (PDF) on 2016-04-08 , retrieved 2016-03-28

 ; also available at [Fundamentals of Music Processing](http://www.music-processing.de) , Section 2.1, pages 40–56 - [[Oppenheim, Alan V.]] ; [[Schafer, Ronald W.]] ; Buck, John R. (1999), [Discrete-time signal processing](https://archive.org/details/discretetimesign00alan) (2nd ed.), Upper Saddle River, N.J.: Prentice Hall, [[ISBN]] [[0-13-754920-2]] - [[Paley, R.E.A.C.]] ; [[Wiener, Norbert]] (1934), Fourier Transforms in the Complex Domain , American Mathematical Society Colloquium Publications, Providence, Rhode Island: [[American Mathematical Society]] - Pinsky, Mark (2002), [Introduction to Fourier Analysis and Wavelets](https://books.google.com/books?id=PyISCgAAQBAJ&q=%22The+Fourier+transform+of+the+measure%22&pg=PA256) , Brooks/Cole, [[ISBN]] [[978-0-534-37660-4]] - [[Poincaré, Henri]] (1895), [Théorie analytique de la propagation de la chaleur](https://gallica.bnf.fr/ark:/12148/bpt6k5500702f) , Paris: Carré - Polyanin, A. D.; Manzhirov, A. V. (1998), Handbook of Integral Equations , Boca Raton: [[CRC Press]] , [[ISBN]] [[978-0-8493-2876-3]] - Press, William H.; Flannery, Brian P.; Teukolsky, Saul A.; Vetterling, William T. (1992), Numerical Recipes in C: The Art of Scientific Computing, Second Edition (2nd ed.), [[Cambridge University Press]] - Proakis, John G.; [[Manolakis, Dimitri G.]] (1996). [Digital Signal Processing: Principles, Algorithms and Applications](https://archive.org/details/digitalsignalpro00proa) (3rd ed.). New Jersey: Prentice-Hall International. [[Bibcode]] : [1996dspp.book.....P](https://ui.adsabs.harvard.edu/abs/1996dspp.book.....P) . [[ISBN]] [[978-0-13-373762-2]] . sAcfAQAAIAAJ. - Rahman, Matiur (2011), [Applications of Fourier Transforms to Generalized Functions](https://books.google.com/books?id=k_rdcKaUdr4C&pg=PA10) , WIT Press, [[ISBN]] [[978-1-84564-564-9]] - Rudin, Walter (1991), Fourier Analysis on Groups , New York, NY: John Wiley & Sons, [[ISBN]] [[978-0-471-52364-2]] - Rudin, Walter (1987), Real and Complex Analysis (3rd ed.), Singapore: McGraw Hill, [[ISBN]] [[978-0-07-100276-9]] - Simonen, P.; Olkkonen, H. (1985), "Fast method for computing the Fourier integral transform via Simpson's numerical integration", Journal of Biomedical Engineering , **7** (4): 337– 340, [[doi]] : [10.1016/0141-5425(85)90067-6](https://doi.org/10.1016%2F0141-5425%2885%2990067-6) , [[PMID]] [4057997](https://pubmed.ncbi.nlm.nih.gov/4057997) - Smith, Julius O. ["Mathematics of the Discrete Fourier Transform (DFT), with Audio Applications --- Second Edition"](https://ccrma.stanford.edu/~jos/mdft/Positive_Negative_Frequencies.html) . ccrma.stanford.edu . Retrieved 2022-12-29 . " We may think of a real sinusoid as being the sum of a positive-frequency and a negative-frequency complex sinusoid. " - Stade, Eric (2005). Fourier Analysis . Wiley. [[doi]] : [10.1002/9781118165508](https://doi.org/10.1002%2F9781118165508) . [[ISBN]] [[978-0-471-66984-5]] . - Stein, Elias; Shakarchi, Rami (2003), [Fourier Analysis: An introduction](https://books.google.com/books?id=FAOc24bTfGkC&q=%22The+mathematical+thrust+of+the+principle%22&pg=PA158) , [[Princeton University Press]] , [[ISBN]] [[978-0-691-11384-5]] - [[Stein, Elias]] ; [[Weiss, Guido]] (1971), [Introduction to Fourier Analysis on Euclidean Spaces](https://books.google.com/books?id=YUCV678MNAIC&q=editions:xbArf-TFDSEC) , Princeton, N.J.: [[Princeton University Press]] , [[ISBN]] [[978-0-691-08078-9]] - [[Strichartz, Robert S.]] (1994), A guide to distribution theory and Fourier transforms , Boca Raton: CRC Press, [[ISBN]] [[0-8493-8273-4]] - Taneja, H.C. (2008), ["Chapter 18: Fourier integrals and Fourier transforms"](https://books.google.com/books?id=X-RFRHxMzvYC&q=%22The+Fourier+integral+can+be+regarded+as+an+extension+of+the+concept+of+Fourier+series%22&pg=PA192) , Advanced Engineering Mathematics , vol. 2, New Delhi, India: I. K. International Pvt Ltd, [[ISBN]] [[978-81-89866-56-3]] - [[Titchmarsh, E.]] (1986) [1948], Introduction to the theory of Fourier integrals (2nd ed.), Oxford University: [[Clarendon Press]] , [[ISBN]] [[978-0-8284-0324-5]] - Vretblad, Anders (2000), Fourier Analysis and its Applications , [[Graduate Texts in Mathematics]] , vol. 223, New York: [[Springer]] , [[ISBN]] [[978-0-387-00836-3]] - [[Whittaker, E. T.]] ; [[Watson, G. N.]] (1927), [[A Course of Modern Analysis]] (4th ed.), [[Cambridge University Press]] - Widder, David Vernon; [[Wiener, Norbert]] (August 1938), ["Remarks on the Classical Inversion Formula for the Laplace Integral"](https://projecteuclid.org/euclid.bams/1183500627) , Bulletin of the American Mathematical Society , **44** (8): 573– 575, [[doi]] : [10.1090/s0002-9904-1938-06812-7](https://doi.org/10.1090%2Fs0002-9904-1938-06812-7) - [[Wiener, Norbert]] (1949). [Extrapolation, Interpolation, and Smoothing of Stationary Time Series: With Engineering Applications](https://direct.mit.edu/books/oa-monograph/4361/Extrapolation-Interpolation-and-Smoothing-of) . [[MIT Press]] . [[ISBN]] [[978-0-262-25719-0]] .

 `{{ [[cite book]] }}` :

 ISBN / Date incompatibility ( [[help]] ) - Wilson, R. G. (1995), Fourier Series and Optical Transform Techniques in Contemporary Optics , New York: [[Wiley]] , [[ISBN]] [[978-0-471-30357-2]] - Wolf, Kurt B. (1979), [Integral Transforms in Science and Engineering](https://www.fis.unam.mx/~bwolf/integraleng.html) , [[Springer]] , [[doi]] : [10.1007/978-1-4757-0872-1](https://doi.org/10.1007%2F978-1-4757-0872-1) , [[ISBN]] [[978-1-4757-0874-5]] - [[Yosida, K.]] (1968), Functional Analysis , [[Springer]] , [[ISBN]] [[978-3-540-58654-8]] - Yousefi, Mansoor I; Kschischang, Frank R (2014). ["Information Transmission Using the Nonlinear Fourier Transform, Part I: Mathematical Tools"](http://arxiv.org/pdf/1202.3653) . IEEE Transactions on Information Theory . **60** (7): 4312– 4328. [[arXiv]] : [1202.3653](https://arxiv.org/abs/1202.3653) . [[doi]] : [10.1109/TIT.2014.2321143](https://doi.org/10.1109%2FTIT.2014.2321143) . [[ISSN]] [0018-9448](https://search.worldcat.org/issn/0018-9448)

 . Retrieved 2025-09-21 .

## External links

- [[]] Media related to [Fourier transformation](https://commons.wikimedia.org/wiki/Category:Fourier_transformation "commons:Category:Fourier transformation") at Wikimedia Commons - [Encyclopedia of Mathematics](https://www.encyclopediaofmath.org/index.php/Fourier_transform) - [[Weisstein, Eric W.]] ["Fourier Transform"](https://mathworld.wolfram.com/FourierTransform.html) . MathWorld . - [Fourier Transform in Crystallography](https://www.xtal.iqf.csic.es/Cristalografia/parte_05-en.html)