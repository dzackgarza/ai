https://en.wikipedia.org/wiki/Wave_equation

# Wave equation

[![](//upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Wave_equation_1D_fixed_endpoints.gif/250px-Wave_equation_1D_fixed_endpoints.gif)](https://en.wikipedia.org/wiki/File:Wave_equation_1D_fixed_endpoints.gif)

A [pulse](https://en.wikipedia.org/wiki/Pulse_(physics) "Pulse (physics)") traveling through a string with fixed endpoints as modeled by the wave equation

[![](//upload.wikimedia.org/wikipedia/commons/1/12/Spherical_wave2.gif)](https://en.wikipedia.org/wiki/File:Spherical_wave2.gif)

Spherical waves coming from a point source

[![](//upload.wikimedia.org/wikipedia/commons/b/bb/2D_Wave_Function_resize.gif)](https://en.wikipedia.org/wiki/File:2D_Wave_Function_resize.gif)

A solution to the 2D wave equation

The **wave equation** is a second-order linear [partial differential equation](https://en.wikipedia.org/wiki/Partial_differential_equation "Partial differential equation") for the description of [waves](https://en.wikipedia.org/wiki/Wave "Wave") or [standing wave](https://en.wikipedia.org/wiki/Standing_wave "Standing wave") fields such as [mechanical waves](https://en.wikipedia.org/wiki/Mechanical_waves "Mechanical waves") (e.g. [water](https://en.wikipedia.org/wiki/Water "Water") waves, [sound waves](https://en.wikipedia.org/wiki/Sound_waves "Sound waves") and [seismic waves](https://en.wikipedia.org/wiki/Seismic_waves "Seismic waves")) or [electromagnetic waves](https://en.wikipedia.org/wiki/Electromagnetic_radiation "Electromagnetic radiation") (including [light](https://en.wikipedia.org/wiki/Light "Light") waves). It arises in fields like [acoustics](https://en.wikipedia.org/wiki/Acoustics "Acoustics"), [electromagnetism](https://en.wikipedia.org/wiki/Electromagnetism "Electromagnetism"), and [fluid dynamics](https://en.wikipedia.org/wiki/Fluid_dynamics "Fluid dynamics").

This article focuses on waves in [classical physics](https://en.wikipedia.org/wiki/Classical_physics "Classical physics"). Quantum physics uses an operator-based [wave equation](https://en.wikipedia.org/wiki/Schrodinger_equation "Schrodinger equation") often as a [relativistic wave equation](https://en.wikipedia.org/wiki/Relativistic_wave_equation "Relativistic wave equation").

## Introduction

The wave equation is a [hyperbolic partial differential equation](https://en.wikipedia.org/wiki/Hyperbolic_partial_differential_equation "Hyperbolic partial differential equation") describing waves, including traveling and [standing waves](https://en.wikipedia.org/wiki/Standing_waves "Standing waves"); the latter can be considered as [linear superpositions](https://en.wikipedia.org/wiki/Superposition_principle "Superposition principle") of waves traveling in opposite directions. This article mostly focuses on the scalar wave equation describing waves in [scalars](https://en.wikipedia.org/wiki/Scalar_field "Scalar field") by scalar functions ${\displaystyle u=u(x,y,z,t)}$${\displaystyle u=u(x,y,z,t)}$ of a time variable ${\displaystyle t}$${\displaystyle t}$ (a variable representing time) and one or more spatial variables ${\displaystyle x,y,z}$${\displaystyle x,y,z}$ (variables representing a position in a space under discussion). At the same time, there are vector wave equations describing waves in [vectors](https://en.wikipedia.org/wiki/Vector_field "Vector field") such as [waves for an electrical field, magnetic field, and magnetic vector potential](https://en.wikipedia.org/wiki/Inhomogeneous_electromagnetic_wave_equation "Inhomogeneous electromagnetic wave equation") and [elastic waves](#Elastic_waves). By comparison with vector wave equations, the scalar wave equation can be seen as a special case of the vector wave equations; in the [Cartesian coordinate system](https://en.wikipedia.org/wiki/Cartesian_coordinate_system "Cartesian coordinate system"), the scalar wave equation is the equation to be satisfied by each component (for each coordinate axis, such as the ${\displaystyle x}$${\displaystyle x}$ component for the *x* axis) of a vector wave without sources of waves in the considered domain (i.e., space and time). For example, in the Cartesian coordinate system, for ${\displaystyle (E\_{x},E\_{y},E\_{z})}$${\displaystyle (E\_{x},E\_{y},E\_{z})}$ as the representation of an electric vector field wave ${\displaystyle {\vec {E}}}$${\displaystyle {\vec {E}}}$ in the absence of wave sources, each coordinate axis component ${\displaystyle E\_{i},i=x,y,z,}$${\displaystyle E\_{i},i=x,y,z,}$ must satisfy the scalar wave equation. Other scalar wave equation solutions u are for [physical quantities](https://en.wikipedia.org/wiki/Physical_quantity "Physical quantity") in [scalars](https://en.wikipedia.org/wiki/Scalar_field "Scalar field") such as [pressure](https://en.wikipedia.org/wiki/Acoustic_wave_equation#Equation "Acoustic wave equation") in a liquid or gas, or the [displacement](https://en.wikipedia.org/wiki/Displacement_(vector) "Displacement (vector)") along some specific direction of particles of a vibrating solid away from their resting (equilibrium) positions.

The scalar wave equation is

${\displaystyle {\frac {\partial ^{2}u}{\partial t^{2}}}=c^{2}\left({\frac {\partial ^{2}u}{\partial x^{2}}}+{\frac {\partial ^{2}u}{\partial y^{2}}}+{\frac {\partial ^{2}u}{\partial z^{2}}}\right)}$${\displaystyle {\frac {\partial ^{2}u}{\partial t^{2}}}=c^{2}\left({\frac {\partial ^{2}u}{\partial x^{2}}}+{\frac {\partial ^{2}u}{\partial y^{2}}}+{\frac {\partial ^{2}u}{\partial z^{2}}}\right)}$

where

* ${\displaystyle c}$${\displaystyle c}$ is a fixed non-negative [real](https://en.wikipedia.org/wiki/Real_number "Real number") [coefficient](https://en.wikipedia.org/wiki/Coefficient "Coefficient") representing the [propagation speed](https://en.wikipedia.org/wiki/Wave#Wave_velocity "Wave") of the wave
* ${\displaystyle u}$${\displaystyle u}$ is a [scalar field](https://en.wikipedia.org/wiki/Scalar_field "Scalar field") representing the displacement or, more generally, the conserved quantity (e.g. [pressure](https://en.wikipedia.org/wiki/Pressure "Pressure") or [density](https://en.wikipedia.org/wiki/Density "Density"))
* ${\displaystyle x,y,}$${\displaystyle x,y,}$ and ${\displaystyle z}$${\displaystyle z}$ are the three spatial coordinates and ${\displaystyle t}$${\displaystyle t}$ being the time coordinate.

The equation states that, at any given point, the second derivative of ${\displaystyle u}$${\displaystyle u}$ with respect to time is proportional to the sum of the second derivatives of ${\displaystyle u}$${\displaystyle u}$ with respect to space, with the constant of proportionality being the square of the speed of the wave.

Using notations from [vector calculus](https://en.wikipedia.org/wiki/Vector_calculus "Vector calculus"), the wave equation can be written compactly as
${\displaystyle u\_{tt}=c^{2}\Delta u,}$${\displaystyle u\_{tt}=c^{2}\Delta u,}$
or
${\displaystyle \Box u=0,}$${\displaystyle \Box u=0,}$
where the double subscript denotes the second-order [partial derivative](https://en.wikipedia.org/wiki/Partial_derivative "Partial derivative") with respect to time, ${\displaystyle \Delta }$${\displaystyle \Delta }$ is the [Laplace operator](https://en.wikipedia.org/wiki/Laplace_operator "Laplace operator") and ${\displaystyle \Box }$${\displaystyle \Box }$ the [d'Alembert operator](https://en.wikipedia.org/wiki/D%27Alembert_operator "D'Alembert operator"), defined as:
${\displaystyle u\_{tt}={\frac {\partial ^{2}u}{\partial t^{2}}},\qquad \Delta ={\frac {\partial ^{2}}{\partial x^{2}}}+{\frac {\partial ^{2}}{\partial y^{2}}}+{\frac {\partial ^{2}}{\partial z^{2}}},\qquad \Box ={\frac {1}{c^{2}}}{\frac {\partial ^{2}}{\partial t^{2}}}-\Delta .}$${\displaystyle u\_{tt}={\frac {\partial ^{2}u}{\partial t^{2}}},\qquad \Delta ={\frac {\partial ^{2}}{\partial x^{2}}}+{\frac {\partial ^{2}}{\partial y^{2}}}+{\frac {\partial ^{2}}{\partial z^{2}}},\qquad \Box ={\frac {1}{c^{2}}}{\frac {\partial ^{2}}{\partial t^{2}}}-\Delta .}$

A solution to this (two-way) wave equation can be quite complicated. Still, it can be analyzed as a [linear combination](https://en.wikipedia.org/wiki/Linear_combination "Linear combination") of simple solutions that are [sinusoidal](https://en.wikipedia.org/wiki/Sinusoidal "Sinusoidal") [plane waves](https://en.wikipedia.org/wiki/Plane_wave "Plane wave") with various directions of propagation and wavelengths but all with the same propagation speed ${\displaystyle c}$${\displaystyle c}$. This analysis is possible because the wave equation is [linear](https://en.wikipedia.org/wiki/Linear_differential_equation "Linear differential equation") and homogeneous, so that any multiple of a solution is also a solution, and the sum of any two solutions is again a solution. This property is called the [superposition principle](https://en.wikipedia.org/wiki/Superposition_principle "Superposition principle") in physics.

The wave equation alone does not specify a physical solution; a unique solution is usually obtained by setting a problem with further conditions, such as [initial conditions](https://en.wikipedia.org/wiki/Initial_conditions "Initial conditions"), which prescribe the amplitude and phase of the wave. Another important class of problems occurs in enclosed spaces specified by [boundary conditions](https://en.wikipedia.org/wiki/Boundary_conditions "Boundary conditions"), for which the solutions represent [standing waves](https://en.wikipedia.org/wiki/Standing_waves "Standing waves"), or [harmonics](https://en.wikipedia.org/wiki/Harmonics "Harmonics"), analogous to the harmonics of musical instruments.

## Wave equation in one space dimension

[![](//upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Maurice_Quentin_de_La_Tour_-_Portrait_de_Jean_Le_Rond_d%27Alembert.jpg/250px-Maurice_Quentin_de_La_Tour_-_Portrait_de_Jean_Le_Rond_d%27Alembert.jpg)](https://en.wikipedia.org/wiki/File:Maurice_Quentin_de_La_Tour_-_Portrait_de_Jean_Le_Rond_d%27Alembert.jpg)

French scientist [Jean-Baptiste le Rond d'Alembert](https://en.wikipedia.org/wiki/Jean-Baptiste_le_Rond_d%27Alembert "Jean-Baptiste le Rond d'Alembert") discovered the wave equation in one space dimension.

The wave equation in one spatial dimension can be written as follows:
${\displaystyle {\frac {\partial ^{2}u}{\partial t^{2}}}=c^{2}{\frac {\partial ^{2}u}{\partial x^{2}}}.}$${\displaystyle {\frac {\partial ^{2}u}{\partial t^{2}}}=c^{2}{\frac {\partial ^{2}u}{\partial x^{2}}}.}$This equation is typically described as having only one spatial dimension ${\displaystyle x}$${\displaystyle x}$, because the only other [independent variable](https://en.wikipedia.org/wiki/Independent_variable "Independent variable") is the time ${\displaystyle t}$${\displaystyle t}$.

### Derivation

The wave equation in one space dimension can be derived in a variety of different physical settings. Most famously, it can be derived for the case of a [string vibrating](https://en.wikipedia.org/wiki/String_vibration "String vibration") in a two-dimensional plane, with each of its elements being pulled in opposite directions by the force of [tension](https://en.wikipedia.org/wiki/Tension_(physics) "Tension (physics)").

Another physical setting for derivation of the wave equation in one space dimension uses [Hooke's law](https://en.wikipedia.org/wiki/Hooke%27s_law "Hooke's law"). In the [theory of elasticity](https://en.wikipedia.org/wiki/Theory_of_elasticity "Theory of elasticity"), Hooke's law is an approximation for certain materials, stating that the amount by which a material body is deformed (the [strain](https://en.wikipedia.org/wiki/Deformation_(mechanics) "Deformation (mechanics)")) is linearly related to the force causing the deformation (the [stress](https://en.wikipedia.org/wiki/Stress_(mechanics) "Stress (mechanics)")).

#### Hooke's law

The wave equation in the one-dimensional case can be derived from [Hooke's law](https://en.wikipedia.org/wiki/Hooke%27s_law "Hooke's law") in the following way: imagine an array of little weights of mass ${\displaystyle m}$${\displaystyle m}$ interconnected with massless springs of length ⁠${\displaystyle h}$${\displaystyle h}$⁠. The springs have a [spring constant](https://en.wikipedia.org/wiki/Stiffness "Stiffness") of ⁠${\displaystyle k}$${\displaystyle k}$⁠:

:   [![](//upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Array_of_masses.svg/330px-Array_of_masses.svg.png)](https://en.wikipedia.org/wiki/File:Array_of_masses.svg)

Here the dependent variable ${\displaystyle u(x)}$${\displaystyle u(x)}$ measures the distance from the equilibrium of the mass situated at ⁠${\displaystyle x}$${\displaystyle x}$⁠, so that ${\displaystyle u(x)}$${\displaystyle u(x)}$ essentially measures the magnitude of a disturbance (i.e. strain) that is traveling in an elastic material. The resulting force exerted on the mass ${\displaystyle m}$${\displaystyle m}$ at the location ${\displaystyle x+h}$${\displaystyle x+h}$ is:
${\displaystyle {\begin{aligned}F\_{\text{Hooke}}&=F\_{x+2h}-F\_{x}=k[u(x+2h,t)-u(x+h,t)]-k[u(x+h,t)-u(x,t)].\end{aligned}}}$${\displaystyle {\begin{aligned}F\_{\text{Hooke}}&=F\_{x+2h}-F\_{x}=k[u(x+2h,t)-u(x+h,t)]-k[u(x+h,t)-u(x,t)].\end{aligned}}}$

By equating the latter equation with
${\displaystyle {\begin{aligned}F\_{\text{Newton}}&=m\,a(t)=m\,{\frac {\partial ^{2}}{\partial t^{2}}}u(x+h,t),\end{aligned}}}$${\displaystyle {\begin{aligned}F\_{\text{Newton}}&=m\,a(t)=m\,{\frac {\partial ^{2}}{\partial t^{2}}}u(x+h,t),\end{aligned}}}$

the equation of motion for the weight at the location ⁠${\displaystyle x+h}$${\displaystyle x+h}$⁠ is obtained:
${\displaystyle {\frac {\partial ^{2}}{\partial t^{2}}}u(x+h,t)={\frac {k}{m}}[u(x+2h,t)-u(x+h,t)-u(x+h,t)+u(x,t)].}$${\displaystyle {\frac {\partial ^{2}}{\partial t^{2}}}u(x+h,t)={\frac {k}{m}}[u(x+2h,t)-u(x+h,t)-u(x+h,t)+u(x,t)].}$
If the array of weights consists of ${\displaystyle N}$${\displaystyle N}$ weights spaced evenly over the length ${\displaystyle L=Nh}$${\displaystyle L=Nh}$ of total mass ⁠${\displaystyle M=Nm}$${\displaystyle M=Nm}$⁠, and the total [spring constant](https://en.wikipedia.org/wiki/Stiffness "Stiffness") of the array ⁠${\displaystyle K=k/N}$${\displaystyle K=k/N}$⁠, we can write the above equation as
${\displaystyle {\frac {\partial ^{2}}{\partial t^{2}}}u(x+h,t)={\frac {KL^{2}}{M}}{\frac {[u(x+2h,t)-2u(x+h,t)+u(x,t)]}{h^{2}}}.}$${\displaystyle {\frac {\partial ^{2}}{\partial t^{2}}}u(x+h,t)={\frac {KL^{2}}{M}}{\frac {[u(x+2h,t)-2u(x+h,t)+u(x,t)]}{h^{2}}}.}$

Taking the limit ${\displaystyle N\rightarrow \infty ,h\rightarrow 0}$${\displaystyle N\rightarrow \infty ,h\rightarrow 0}$ and assuming smoothness, one gets
${\displaystyle {\frac {\partial ^{2}u(x,t)}{\partial t^{2}}}={\frac {KL^{2}}{M}}{\frac {\partial ^{2}u(x,t)}{\partial x^{2}}},}$${\displaystyle {\frac {\partial ^{2}u(x,t)}{\partial t^{2}}}={\frac {KL^{2}}{M}}{\frac {\partial ^{2}u(x,t)}{\partial x^{2}}},}$
which is from the definition of a [second derivative](https://en.wikipedia.org/wiki/Second_derivative "Second derivative"). ${\displaystyle KL^{2}/M}$${\displaystyle KL^{2}/M}$ is the square of the propagation speed in this particular case.

[![](//upload.wikimedia.org/wikipedia/commons/thumb/8/8f/1d_wave_equation_animation.gif/250px-1d_wave_equation_animation.gif)](https://en.wikipedia.org/wiki/File:1d_wave_equation_animation.gif)

1-d standing wave as a superposition of two waves traveling in opposite directions

#### Stress pulse in a bar

In the case of a stress pulse propagating longitudinally through a bar, the bar acts much like an infinite number of springs in series and can be taken as an extension of the equation derived for Hooke's law. A uniform bar, i.e. of constant cross-section, made from a linear elastic material has a stiffness ${\displaystyle K}$${\displaystyle K}$ given by
${\displaystyle K={\frac {EA}{L}},}$${\displaystyle K={\frac {EA}{L}},}$
where ${\displaystyle A}$${\displaystyle A}$ is the cross-sectional area, and ${\displaystyle E}$${\displaystyle E}$ is the [Young's modulus](https://en.wikipedia.org/wiki/Young%27s_modulus "Young's modulus") of the material. The wave equation becomes
${\displaystyle {\frac {\partial ^{2}u(x,t)}{\partial t^{2}}}={\frac {EAL}{M}}{\frac {\partial ^{2}u(x,t)}{\partial x^{2}}}.}$${\displaystyle {\frac {\partial ^{2}u(x,t)}{\partial t^{2}}}={\frac {EAL}{M}}{\frac {\partial ^{2}u(x,t)}{\partial x^{2}}}.}$

${\displaystyle AL}$${\displaystyle AL}$ is equal to the volume of the bar, and therefore
${\displaystyle {\frac {AL}{M}}={\frac {1}{\rho }},}$${\displaystyle {\frac {AL}{M}}={\frac {1}{\rho }},}$
where ${\displaystyle \rho }$${\displaystyle \rho }$ is the density of the material. The wave equation reduces to
${\displaystyle {\frac {\partial ^{2}u(x,t)}{\partial t^{2}}}={\frac {E}{\rho }}{\frac {\partial ^{2}u(x,t)}{\partial x^{2}}}.}$${\displaystyle {\frac {\partial ^{2}u(x,t)}{\partial t^{2}}}={\frac {E}{\rho }}{\frac {\partial ^{2}u(x,t)}{\partial x^{2}}}.}$

The speed of a stress wave in a bar is therefore ${\displaystyle {\sqrt {E/\rho }}}$${\displaystyle {\sqrt {E/\rho }}}$.

### General solution

#### Algebraic approach

For the one-dimensional wave equation a relatively simple general solution may be found. Defining new variables
${\displaystyle {\begin{aligned}\xi &=x-ct,\\\eta &=x+ct\end{aligned}}}$${\displaystyle {\begin{aligned}\xi &=x-ct,\\\eta &=x+ct\end{aligned}}}$
changes the wave equation into
${\displaystyle {\frac {\partial ^{2}u}{\partial \xi \partial \eta }}(x,t)=0,}$${\displaystyle {\frac {\partial ^{2}u}{\partial \xi \partial \eta }}(x,t)=0,}$
which leads to the general solution
${\displaystyle u(x,t)=F(\xi )+G(\eta )=F(x-ct)+G(x+ct).}$${\displaystyle u(x,t)=F(\xi )+G(\eta )=F(x-ct)+G(x+ct).}$

In other words, the solution is the sum of a right-traveling function ${\displaystyle F}$${\displaystyle F}$ and a left-traveling function ${\displaystyle G}$${\displaystyle G}$. "Traveling" means that the shape of these individual arbitrary functions with respect to x stays constant, however, the functions are translated left and right with time at the speed ${\displaystyle c}$${\displaystyle c}$. This was derived by [Jean le Rond d'Alembert](https://en.wikipedia.org/wiki/Jean_le_Rond_d%27Alembert "Jean le Rond d'Alembert").

Another way to arrive at this result is to factor the wave equation using two first-order [differential operators:](https://en.wikipedia.org/wiki/Differential_operator "Differential operator")
${\displaystyle \left[{\frac {\partial }{\partial t}}-c{\frac {\partial }{\partial x}}\right]\left[{\frac {\partial }{\partial t}}+c{\frac {\partial }{\partial x}}\right]u=0.}$${\displaystyle \left[{\frac {\partial }{\partial t}}-c{\frac {\partial }{\partial x}}\right]\left[{\frac {\partial }{\partial t}}+c{\frac {\partial }{\partial x}}\right]u=0.}$
Then, for our original equation, we can define
${\displaystyle v\equiv {\frac {\partial u}{\partial t}}+c{\frac {\partial u}{\partial x}},}$${\displaystyle v\equiv {\frac {\partial u}{\partial t}}+c{\frac {\partial u}{\partial x}},}$
and find that we must have
${\displaystyle {\frac {\partial v}{\partial t}}-c{\frac {\partial v}{\partial x}}=0.}$${\displaystyle {\frac {\partial v}{\partial t}}-c{\frac {\partial v}{\partial x}}=0.}$

This [advection equation](https://en.wikipedia.org/wiki/Advection_equation "Advection equation") can be solved by interpreting it as telling us that the [directional derivative](https://en.wikipedia.org/wiki/Directional_derivative "Directional derivative") of ${\displaystyle v}$${\displaystyle v}$ in the ${\displaystyle (1,-c)}$${\displaystyle (1,-c)}$ direction is 0. This means that the value of ${\displaystyle v}$${\displaystyle v}$ is constant on [characteristic](https://en.wikipedia.org/wiki/Method_of_characteristics "Method of characteristics") lines of the form *x* + *ct* = *x*0, and thus that ${\displaystyle v}$${\displaystyle v}$ must depend only on *x* + *ct*, that is, have the form *H*(*x* + *ct*). Then, to solve the first (inhomogenous) equation relating ${\displaystyle v}$${\displaystyle v}$ to u, we can note that its homogenous solution must be a function of the form *F*(*x* - *ct*), by logic similar to the above. Guessing a particular solution of the form *G*(*x* + *ct*), we find that

${\displaystyle \left[{\frac {\partial }{\partial t}}+c{\frac {\partial }{\partial x}}\right]G(x+ct)=H(x+ct).}$${\displaystyle \left[{\frac {\partial }{\partial t}}+c{\frac {\partial }{\partial x}}\right]G(x+ct)=H(x+ct).}$

Expanding out the left side, rearranging terms, then using the change of variables *s* = *x* + *ct* simplifies the equation to

${\displaystyle G'(s)={\frac {H(s)}{2c}}.}$${\displaystyle G'(s)={\frac {H(s)}{2c}}.}$

This means we can find a particular solution *G* of the desired form by integration. Thus, we have again shown that u obeys *u*(*x*, *t*) = *F*(*x* - *ct*) + *G*(*x* + *ct*).

For an [initial-value problem](https://en.wikipedia.org/wiki/Initial-value_problem "Initial-value problem"), the arbitrary functions F and G can be determined to satisfy initial conditions:
${\displaystyle u(x,0)=f(x),}$${\displaystyle u(x,0)=f(x),}$${\displaystyle u\_{t}(x,0)=g(x).}$${\displaystyle u\_{t}(x,0)=g(x).}$

The result is [d'Alembert's formula](https://en.wikipedia.org/wiki/D%27Alembert%27s_formula "D'Alembert's formula"):
${\displaystyle u(x,t)={\frac {f(x-ct)+f(x+ct)}{2}}+{\frac {1}{2c}}\int \_{x-ct}^{x+ct}g(s)\,ds.}$${\displaystyle u(x,t)={\frac {f(x-ct)+f(x+ct)}{2}}+{\frac {1}{2c}}\int \_{x-ct}^{x+ct}g(s)\,ds.}$

In the classical sense, if *f*(*x*) ∈ *Ck*, and *g*(*x*) ∈ *C**k*−1, then *u*(*t*, *x*) ∈ *Ck*. However, the waveforms F and G may also be [generalized functions](https://en.wikipedia.org/wiki/Generalized_functions "Generalized functions"), such as the delta-function. In that case, the solution may be interpreted as an impulse that travels to the right or the left.

The basic wave equation is a [linear differential equation](https://en.wikipedia.org/wiki/Linear_differential_equation "Linear differential equation"), and so it will adhere to the [superposition principle](https://en.wikipedia.org/wiki/Superposition_principle "Superposition principle"). This means that the net displacement caused by two or more waves is the sum of the displacements which would have been caused by each wave individually. In addition, the behavior of a wave can be analyzed by breaking up the wave into components, e.g. the [Fourier transform](https://en.wikipedia.org/wiki/Fourier_transform "Fourier transform") breaks up a wave into sinusoidal components.

#### Plane-wave eigenmodes

Another way to solve the one-dimensional wave equation is to first analyze its frequency [eigenmodes](https://en.wikipedia.org/wiki/Eigenmodes "Eigenmodes"). A so-called eigenmode is a solution that oscillates in time with a well-defined *constant* angular frequency ω, so that the temporal part of the wave function takes the form *e*−*iωt* = cos(*ωt*) − *i* sin(*ωt*), and the amplitude is a function *f*(*x*) of the spatial variable x, giving a [separation of variables](https://en.wikipedia.org/wiki/Separation_of_variables "Separation of variables") for the wave function:
${\displaystyle u\_{\omega }(x,t)=e^{-i\omega t}f(x).}$${\displaystyle u\_{\omega }(x,t)=e^{-i\omega t}f(x).}$

This produces an [ordinary differential equation](https://en.wikipedia.org/wiki/Ordinary_differential_equation "Ordinary differential equation") for the spatial part *f*(*x*):
${\displaystyle {\frac {\partial ^{2}u\_{\omega }}{\partial t^{2}}}={\frac {\partial ^{2}}{\partial t^{2}}}\left(e^{-i\omega t}f(x)\right)=-\omega ^{2}e^{-i\omega t}f(x)=c^{2}{\frac {\partial ^{2}}{\partial x^{2}}}\left(e^{-i\omega t}f(x)\right).}$${\displaystyle {\frac {\partial ^{2}u\_{\omega }}{\partial t^{2}}}={\frac {\partial ^{2}}{\partial t^{2}}}\left(e^{-i\omega t}f(x)\right)=-\omega ^{2}e^{-i\omega t}f(x)=c^{2}{\frac {\partial ^{2}}{\partial x^{2}}}\left(e^{-i\omega t}f(x)\right).}$

Therefore,
${\displaystyle {\frac {d^{2}}{dx^{2}}}f(x)=-\left({\frac {\omega }{c}}\right)^{2}f(x),}$${\displaystyle {\frac {d^{2}}{dx^{2}}}f(x)=-\left({\frac {\omega }{c}}\right)^{2}f(x),}$
which is precisely an [eigenvalue equation](https://en.wikipedia.org/wiki/Eigenvalue_equation "Eigenvalue equation") for *f*(*x*), hence the name eigenmode. Known as the [Helmholtz equation](https://en.wikipedia.org/wiki/Helmholtz_equation "Helmholtz equation"), it has the well-known [plane-wave](https://en.wikipedia.org/wiki/Plane-wave "Plane-wave") solutions
${\displaystyle f(x)=Ae^{\pm ikx},}$${\displaystyle f(x)=Ae^{\pm ikx},}$
with [wave number](https://en.wikipedia.org/wiki/Wave_number "Wave number") *k* = *ω*/*c*.

The total wave function for this eigenmode is then the linear combination
${\displaystyle u\_{\omega }(x,t)=e^{-i\omega t}\left(Ae^{-ikx}+Be^{ikx}\right)=Ae^{-i(kx+\omega t)}+Be^{i(kx-\omega t)},}$${\displaystyle u\_{\omega }(x,t)=e^{-i\omega t}\left(Ae^{-ikx}+Be^{ikx}\right)=Ae^{-i(kx+\omega t)}+Be^{i(kx-\omega t)},}$
where complex numbers A, B depend in general on any initial and boundary conditions of the problem.

Eigenmodes are useful in constructing a full solution to the wave equation, because each of them evolves in time trivially with the [phase factor](https://en.wikipedia.org/wiki/Phase_factor "Phase factor") ${\displaystyle e^{-i\omega t},}$${\displaystyle e^{-i\omega t},}$ so that a full solution can be decomposed into an [eigenmode expansion](https://en.wikipedia.org/wiki/Eigenmode_expansion "Eigenmode expansion"):
${\displaystyle u(x,t)=\int \_{-\infty }^{\infty }s(\omega )u\_{\omega }(x,t)\,d\omega ,}$${\displaystyle u(x,t)=\int \_{-\infty }^{\infty }s(\omega )u\_{\omega }(x,t)\,d\omega ,}$
or in terms of the plane waves,
${\displaystyle {\begin{aligned}u(x,t)&=\int \_{-\infty }^{\infty }s\_{+}(\omega )e^{-i(kx+\omega t)}\,d\omega +\int \_{-\infty }^{\infty }s\_{-}(\omega )e^{i(kx-\omega t)}\,d\omega \\&=\int \_{-\infty }^{\infty }s\_{+}(\omega )e^{-ik(x+ct)}\,d\omega +\int \_{-\infty }^{\infty }s\_{-}(\omega )e^{ik(x-ct)}\,d\omega \\&=F(x-ct)+G(x+ct),\end{aligned}}}$${\displaystyle {\begin{aligned}u(x,t)&=\int \_{-\infty }^{\infty }s\_{+}(\omega )e^{-i(kx+\omega t)}\,d\omega +\int \_{-\infty }^{\infty }s\_{-}(\omega )e^{i(kx-\omega t)}\,d\omega \\&=\int \_{-\infty }^{\infty }s\_{+}(\omega )e^{-ik(x+ct)}\,d\omega +\int \_{-\infty }^{\infty }s\_{-}(\omega )e^{ik(x-ct)}\,d\omega \\&=F(x-ct)+G(x+ct),\end{aligned}}}$
which is exactly in the same form as in the algebraic approach. Functions *s*±(*ω*) are known as the [Fourier component](https://en.wikipedia.org/wiki/Fourier_component "Fourier component") and are determined by initial and boundary conditions. This is a so-called [frequency-domain](https://en.wikipedia.org/wiki/Frequency-domain "Frequency-domain") method, alternative to direct [time-domain](https://en.wikipedia.org/wiki/Time-domain "Time-domain") propagations, such as [FDTD](https://en.wikipedia.org/wiki/FDTD "FDTD") method, of the [wave packet](https://en.wikipedia.org/wiki/Wave_packet "Wave packet") *u*(*x*, *t*), which is complete for representing waves in absence of time dilations. Completeness of the Fourier expansion for representing waves in the presence of time dilations has been challenged by [chirp](https://en.wikipedia.org/wiki/Chirp "Chirp") wave solutions allowing for time variation of ω. The chirp wave solutions seem particularly implied by very large but previously inexplicable radar residuals in the [flyby anomaly](https://en.wikipedia.org/wiki/Flyby_anomaly "Flyby anomaly") and differ from the sinusoidal solutions in being receivable at any distance only at proportionally shifted frequencies and time dilations, corresponding to past chirp states of the source.

## Vectorial wave equation in three space dimensions

The vectorial wave equation (from which the scalar wave equation can be directly derived) can be obtained by applying a force equilibrium to an [infinitesimal](https://en.wikipedia.org/wiki/Infinitesimal "Infinitesimal") [volume element](https://en.wikipedia.org/wiki/Volume_element "Volume element"). If the medium has a modulus of elasticity ${\displaystyle E}$${\displaystyle E}$ that is homogeneous (i.e. independent of ${\displaystyle \mathbf {x} }$${\displaystyle \mathbf {x} }$) within the volume element, then its stress tensor is given by ${\displaystyle \mathbf {T} =E\nabla \mathbf {u} }$${\displaystyle \mathbf {T} =E\nabla \mathbf {u} }$, for a vectorial elastic deflection ${\displaystyle \mathbf {u} (\mathbf {x} ,t)}$${\displaystyle \mathbf {u} (\mathbf {x} ,t)}$. The local equilibrium of:

1. the tension force ${\displaystyle \operatorname {div} \mathbf {T} =\nabla \cdot (E\nabla \mathbf {u} )=E\Delta \mathbf {u} }$${\displaystyle \operatorname {div} \mathbf {T} =\nabla \cdot (E\nabla \mathbf {u} )=E\Delta \mathbf {u} }$ due to deflection ${\displaystyle \mathbf {u} }$${\displaystyle \mathbf {u} }$, and
2. the inertial force ${\displaystyle \rho \partial ^{2}\mathbf {u} /\partial t^{2}}$${\displaystyle \rho \partial ^{2}\mathbf {u} /\partial t^{2}}$ caused by the local acceleration ${\displaystyle \partial ^{2}\mathbf {u} /\partial t^{2}}$${\displaystyle \partial ^{2}\mathbf {u} /\partial t^{2}}$

can be written as ${\displaystyle \rho {\frac {\partial ^{2}\mathbf {u} }{\partial t^{2}}}-E\Delta \mathbf {u} =\mathbf {0} .}$${\displaystyle \rho {\frac {\partial ^{2}\mathbf {u} }{\partial t^{2}}}-E\Delta \mathbf {u} =\mathbf {0} .}$

By merging density ${\displaystyle \rho }$${\displaystyle \rho }$ and elasticity module ${\displaystyle E,}$${\displaystyle E,}$ the sound velocity ${\displaystyle c={\sqrt {E/\rho }}}$${\displaystyle c={\sqrt {E/\rho }}}$ results (material law). After insertion, follows the well-known governing wave equation for a homogeneous medium:
${\displaystyle {\frac {\partial ^{2}\mathbf {u} }{\partial t^{2}}}-c^{2}\Delta \mathbf {u} ={\boldsymbol {0}}.}$${\displaystyle {\frac {\partial ^{2}\mathbf {u} }{\partial t^{2}}}-c^{2}\Delta \mathbf {u} ={\boldsymbol {0}}.}$
(Note: Instead of vectorial ${\displaystyle \mathbf {u} (\mathbf {x} ,t),}$${\displaystyle \mathbf {u} (\mathbf {x} ,t),}$ only scalar ${\displaystyle u(x,t)}$${\displaystyle u(x,t)}$ can be used, i.e. waves are travelling only along the ${\displaystyle x}$${\displaystyle x}$ axis, and the scalar wave equation follows as ${\displaystyle {\frac {\partial ^{2}u}{\partial t^{2}}}-c^{2}{\frac {\partial ^{2}u}{\partial x^{2}}}=0}$${\displaystyle {\frac {\partial ^{2}u}{\partial t^{2}}}-c^{2}{\frac {\partial ^{2}u}{\partial x^{2}}}=0}$.)

The above vectorial partial differential equation of the 2nd order delivers two mutually independent solutions. From the quadratic velocity term ${\displaystyle c^{2}=(+c)^{2}=(-c)^{2}}$${\displaystyle c^{2}=(+c)^{2}=(-c)^{2}}$ can be seen that there are two waves travelling in opposite directions ${\displaystyle +c}$${\displaystyle +c}$ and ${\displaystyle -c}$${\displaystyle -c}$ are possible, hence results the designation "two-way wave equation".
It can be shown for plane [longitudinal wave](https://en.wikipedia.org/wiki/Longitudinal_wave "Longitudinal wave") propagation that the synthesis of two [one-way wave equations](https://en.wikipedia.org/wiki/One-way_wave_equation "One-way wave equation") leads to a general two-way wave equation. For ${\displaystyle \nabla \mathbf {c} =\mathbf {0} ,}$${\displaystyle \nabla \mathbf {c} =\mathbf {0} ,}$ special two-wave equation with the d'Alembert operator results:
${\displaystyle \left({\frac {\partial }{\partial t}}-\mathbf {c} \cdot \nabla \right)\left({\frac {\partial }{\partial t}}+\mathbf {c} \cdot \nabla \right)\mathbf {u} =\left({\frac {\partial ^{2}}{\partial t^{2}}}+(\mathbf {c} \cdot \nabla )\mathbf {c} \cdot \nabla \right)\mathbf {u} =\left({\frac {\partial ^{2}}{\partial t^{2}}}+(\mathbf {c} \cdot \nabla )^{2}\right)\mathbf {u} =\mathbf {0} .}$${\displaystyle \left({\frac {\partial }{\partial t}}-\mathbf {c} \cdot \nabla \right)\left({\frac {\partial }{\partial t}}+\mathbf {c} \cdot \nabla \right)\mathbf {u} =\left({\frac {\partial ^{2}}{\partial t^{2}}}+(\mathbf {c} \cdot \nabla )\mathbf {c} \cdot \nabla \right)\mathbf {u} =\left({\frac {\partial ^{2}}{\partial t^{2}}}+(\mathbf {c} \cdot \nabla )^{2}\right)\mathbf {u} =\mathbf {0} .}$
For ${\displaystyle \nabla \mathbf {c} =\mathbf {0} ,}$${\displaystyle \nabla \mathbf {c} =\mathbf {0} ,}$ this simplifies to
${\displaystyle \left({\frac {\partial ^{2}}{\partial t^{2}}}+c^{2}\Delta \right)\mathbf {u} =\mathbf {0} .}$${\displaystyle \left({\frac {\partial ^{2}}{\partial t^{2}}}+c^{2}\Delta \right)\mathbf {u} =\mathbf {0} .}$
Therefore, the vectorial 1st-order [one-way wave equation](https://en.wikipedia.org/wiki/One-way_wave_equation "One-way wave equation") with waves travelling in a pre-defined propagation direction ${\displaystyle \mathbf {c} }$${\displaystyle \mathbf {c} }$ results as
${\displaystyle {\frac {\partial \mathbf {u} }{\partial t}}-\mathbf {c} \cdot \nabla \mathbf {u} =\mathbf {0} .}$${\displaystyle {\frac {\partial \mathbf {u} }{\partial t}}-\mathbf {c} \cdot \nabla \mathbf {u} =\mathbf {0} .}$

## Scalar wave equation in three space dimensions

[![](//upload.wikimedia.org/wikipedia/commons/thumb/6/60/Leonhard_Euler_2.jpg/250px-Leonhard_Euler_2.jpg)](https://en.wikipedia.org/wiki/File:Leonhard_Euler_2.jpg)

Swiss mathematician and physicist [Leonhard Euler](https://en.wikipedia.org/wiki/Leonhard_Euler "Leonhard Euler") (b. 1707) discovered the wave equation in three space dimensions.

A solution of the initial-value problem for the wave equation in three space dimensions can be obtained from the corresponding solution for a spherical wave. The result can then be also used to obtain the same solution in two space dimensions.

### Spherical waves

To obtain a solution with constant frequencies, apply the [Fourier transform](https://en.wikipedia.org/wiki/Fourier_transform "Fourier transform")
${\displaystyle \Psi (\mathbf {r} ,t)=\int \_{-\infty }^{\infty }\Psi (\mathbf {r} ,\omega )e^{-i\omega t}\,d\omega ,}$${\displaystyle \Psi (\mathbf {r} ,t)=\int \_{-\infty }^{\infty }\Psi (\mathbf {r} ,\omega )e^{-i\omega t}\,d\omega ,}$
which transforms the wave equation into an [elliptic partial differential equation](https://en.wikipedia.org/wiki/Elliptic_partial_differential_equation "Elliptic partial differential equation") of the form:
${\displaystyle \left(\nabla ^{2}+{\frac {\omega ^{2}}{c^{2}}}\right)\Psi (\mathbf {r} ,\omega )=0.}$${\displaystyle \left(\nabla ^{2}+{\frac {\omega ^{2}}{c^{2}}}\right)\Psi (\mathbf {r} ,\omega )=0.}$

This is the [Helmholtz equation](https://en.wikipedia.org/wiki/Helmholtz_equation "Helmholtz equation") and can be solved using [separation of variables](https://en.wikipedia.org/wiki/Separation_of_variables "Separation of variables"). In [spherical coordinates](https://en.wikipedia.org/wiki/Spherical_coordinates "Spherical coordinates") this leads to a separation of the radial and angular variables, writing the solution as:
${\displaystyle \Psi (\mathbf {r} ,\omega )=\sum \_{l,m}f\_{lm}(r)Y\_{lm}(\theta ,\phi ).}$${\displaystyle \Psi (\mathbf {r} ,\omega )=\sum \_{l,m}f\_{lm}(r)Y\_{lm}(\theta ,\phi ).}$
The angular part of the solution take the form of [spherical harmonics](https://en.wikipedia.org/wiki/Spherical_harmonics "Spherical harmonics") and the radial function satisfies:
${\displaystyle \left[{\frac {d^{2}}{dr^{2}}}+{\frac {2}{r}}{\frac {d}{dr}}+k^{2}-{\frac {l(l+1)}{r^{2}}}\right]f\_{l}(r)=0.}$${\displaystyle \left[{\frac {d^{2}}{dr^{2}}}+{\frac {2}{r}}{\frac {d}{dr}}+k^{2}-{\frac {l(l+1)}{r^{2}}}\right]f\_{l}(r)=0.}$
independent of ${\displaystyle m}$${\displaystyle m}$, with ${\displaystyle k^{2}=\omega ^{2}/c^{2}}$${\displaystyle k^{2}=\omega ^{2}/c^{2}}$. Substituting
${\displaystyle f\_{l}(r)={\frac {1}{\sqrt {r}}}u\_{l}(r),}$${\displaystyle f\_{l}(r)={\frac {1}{\sqrt {r}}}u\_{l}(r),}$
transforms the equation into
${\displaystyle \left[{\frac {d^{2}}{dr^{2}}}+{\frac {1}{r}}{\frac {d}{dr}}+k^{2}-{\frac {(l+{\frac {1}{2}})^{2}}{r^{2}}}\right]u\_{l}(r)=0,}$${\displaystyle \left[{\frac {d^{2}}{dr^{2}}}+{\frac {1}{r}}{\frac {d}{dr}}+k^{2}-{\frac {(l+{\frac {1}{2}})^{2}}{r^{2}}}\right]u\_{l}(r)=0,}$
which is the [Bessel equation](https://en.wikipedia.org/wiki/Bessel_equation "Bessel equation").

#### Example

Consider the case *l* = 0. Then there is no angular dependence and the amplitude depends only on the radial distance, i.e., Ψ(**r**, *t*) → *u*(*r*, *t*). In this case, the wave equation reduces to[*[clarification needed](https://en.wikipedia.org/wiki/Wikipedia:Please_clarify "Wikipedia:Please clarify")*]${\displaystyle \left(\nabla ^{2}-{\frac {1}{c^{2}}}{\frac {\partial ^{2}}{\partial t^{2}}}\right)\Psi (\mathbf {r} ,t)=0,}$${\displaystyle \left(\nabla ^{2}-{\frac {1}{c^{2}}}{\frac {\partial ^{2}}{\partial t^{2}}}\right)\Psi (\mathbf {r} ,t)=0,}$
or
${\displaystyle \left({\frac {\partial ^{2}}{\partial r^{2}}}+{\frac {2}{r}}{\frac {\partial }{\partial r}}-{\frac {1}{c^{2}}}{\frac {\partial ^{2}}{\partial t^{2}}}\right)u(r,t)=0.}$${\displaystyle \left({\frac {\partial ^{2}}{\partial r^{2}}}+{\frac {2}{r}}{\frac {\partial }{\partial r}}-{\frac {1}{c^{2}}}{\frac {\partial ^{2}}{\partial t^{2}}}\right)u(r,t)=0.}$

This equation can be rewritten as
${\displaystyle {\frac {\partial ^{2}(ru)}{\partial t^{2}}}-c^{2}{\frac {\partial ^{2}(ru)}{\partial r^{2}}}=0,}$${\displaystyle {\frac {\partial ^{2}(ru)}{\partial t^{2}}}-c^{2}{\frac {\partial ^{2}(ru)}{\partial r^{2}}}=0,}$
where the quantity *ru* satisfies the one-dimensional wave equation. Therefore, there are solutions in the form${\displaystyle u(r,t)={\frac {1}{r}}F(r-ct)+{\frac {1}{r}}G(r+ct),}$${\displaystyle u(r,t)={\frac {1}{r}}F(r-ct)+{\frac {1}{r}}G(r+ct),}$
where F and G are general solutions to the one-dimensional wave equation and can be interpreted as respectively an outgoing and incoming spherical waves. The outgoing wave can be generated by a [point source](https://en.wikipedia.org/wiki/Point_source "Point source"), and they make possible sharp signals whose form is altered only by a decrease in amplitude as r increases (see an illustration of a spherical wave on the top right). Such waves exist only in cases of space with odd dimensions.[*[citation needed](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed "Wikipedia:Citation needed")*]

For physical examples of solutions to the 3D wave equation that possess angular dependence, see [dipole radiation](https://en.wikipedia.org/wiki/Dipole_radiation "Dipole radiation").

#### Monochromatic spherical wave

[![](//upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Spherical_Wave.gif/250px-Spherical_Wave.gif)](https://en.wikipedia.org/wiki/File:Spherical_Wave.gif)

Cut-away of spherical wavefronts, with a wavelength of 10 units, propagating from a point source

Although the word "monochromatic" is not exactly accurate, since it refers to light or [electromagnetic radiation](https://en.wikipedia.org/wiki/Electromagnetic_radiation "Electromagnetic radiation") with well-defined frequency, the spirit is to discover the eigenmode of the wave equation in three dimensions. Following the derivation in the previous section on [plane-wave eigenmodes](#Plane-wave_eigenmodes), if we again restrict our solutions to spherical waves that oscillate in time with well-defined *constant* angular frequency ω, then the transformed function *ru*(*r*, *t*) has simply plane-wave solutions:${\displaystyle ru(r,t)=Ae^{i(\omega t\pm kr)},}$${\displaystyle ru(r,t)=Ae^{i(\omega t\pm kr)},}$
or
${\displaystyle u(r,t)={\frac {A}{r}}e^{i(\omega t\pm kr)}.}$${\displaystyle u(r,t)={\frac {A}{r}}e^{i(\omega t\pm kr)}.}$

From this we can observe that the peak intensity of the spherical-wave oscillation, characterized as the squared wave amplitude
${\displaystyle I=|u(r,t)|^{2}={\frac {|A|^{2}}{r^{2}}},}$${\displaystyle I=|u(r,t)|^{2}={\frac {|A|^{2}}{r^{2}}},}$
drops at the rate proportional to 1/*r*2, an example of the [inverse-square law](https://en.wikipedia.org/wiki/Inverse-square_law "Inverse-square law").

### Solution of a general initial-value problem

The wave equation is linear in u and is left unaltered by translations in space and time. Therefore, we can generate a great variety of solutions by translating and summing spherical waves. Let *φ*(*ξ*, *η*, *ζ*) be an arbitrary function of three independent variables, and let the spherical wave form F be a [delta function](https://en.wikipedia.org/wiki/Delta_function "Delta function"). Let a family of spherical waves have center at (*ξ*, *η*, *ζ*), and let r be the radial distance from that point. Thus

${\displaystyle r^{2}=(x-\xi )^{2}+(y-\eta )^{2}+(z-\zeta )^{2}.}$${\displaystyle r^{2}=(x-\xi )^{2}+(y-\eta )^{2}+(z-\zeta )^{2}.}$

If u is a superposition of such waves with weighting function φ, then
${\displaystyle u(t,x,y,z)={\frac {1}{4\pi c}}\iiint \varphi (\xi ,\eta ,\zeta ){\frac {\delta (r-ct)}{r}}\,d\xi \,d\eta \,d\zeta ;}$${\displaystyle u(t,x,y,z)={\frac {1}{4\pi c}}\iiint \varphi (\xi ,\eta ,\zeta ){\frac {\delta (r-ct)}{r}}\,d\xi \,d\eta \,d\zeta ;}$
the denominator 4*πc* is a convenience.

From the definition of the delta function, u may also be written as
${\displaystyle u(t,x,y,z)={\frac {t}{4\pi }}\iint \_{S}\varphi (x+ct\alpha ,y+ct\beta ,z+ct\gamma )\,d\omega ,}$${\displaystyle u(t,x,y,z)={\frac {t}{4\pi }}\iint \_{S}\varphi (x+ct\alpha ,y+ct\beta ,z+ct\gamma )\,d\omega ,}$
where α, β, and γ are coordinates on the unit sphere S, and ω is the area element on S. This result has the interpretation that *u*(*t*, *x*) is t times the mean value of φ on a sphere of radius *ct* centered at x:
${\displaystyle u(t,x,y,z)=tM\_{ct}[\varphi ].}$${\displaystyle u(t,x,y,z)=tM\_{ct}[\varphi ].}$

It follows that
${\displaystyle u(0,x,y,z)=0,\quad u\_{t}(0,x,y,z)=\varphi (x,y,z).}$${\displaystyle u(0,x,y,z)=0,\quad u\_{t}(0,x,y,z)=\varphi (x,y,z).}$

The mean value is an even function of t, and hence if
${\displaystyle v(t,x,y,z)={\frac {\partial }{\partial t}}{\big (}tM\_{ct}[\varphi ]{\big )},}$${\displaystyle v(t,x,y,z)={\frac {\partial }{\partial t}}{\big (}tM\_{ct}[\varphi ]{\big )},}$
then
${\displaystyle v(0,x,y,z)=\varphi (x,y,z),\quad v\_{t}(0,x,y,z)=0.}$${\displaystyle v(0,x,y,z)=\varphi (x,y,z),\quad v\_{t}(0,x,y,z)=0.}$

These formulas provide the solution for the initial-value problem for the wave equation. They show that the solution at a given point P, given (*t*, *x*, *y*, *z*) depends only on the data on the sphere of radius *ct* that is intersected by the **[light cone](https://en.wikipedia.org/wiki/Light_cone "Light cone")** drawn backwards from P. It does *not* depend upon data on the interior of this sphere. Thus the interior of the sphere is a [lacuna](https://en.wikipedia.org/wiki/Petrovsky_lacuna "Petrovsky lacuna") for the solution. This phenomenon is called **[Huygens' principle](https://en.wikipedia.org/wiki/Huygens%27_principle "Huygens' principle")**. It is only true for odd numbers of space dimension, where for one dimension the integration is performed over the boundary of an interval with respect to the [Dirac measure](https://en.wikipedia.org/wiki/Dirac_measure "Dirac measure").

## Scalar wave equation in two space dimensions

In two space dimensions, the wave equation is

${\displaystyle u\_{tt}=c^{2}\left(u\_{xx}+u\_{yy}\right).}$${\displaystyle u\_{tt}=c^{2}\left(u\_{xx}+u\_{yy}\right).}$

We can use the three-dimensional theory to solve this problem if we regard u as a function in three dimensions that is independent of the third dimension. If

${\displaystyle u(0,x,y)=0,\quad u\_{t}(0,x,y)=\phi (x,y),}$${\displaystyle u(0,x,y)=0,\quad u\_{t}(0,x,y)=\phi (x,y),}$

then the three-dimensional solution formula becomes

${\displaystyle u(t,x,y)=tM\_{ct}[\phi ]={\frac {t}{4\pi }}\iint \_{S}\phi (x+ct\alpha ,\,y+ct\beta )\,d\omega ,}$${\displaystyle u(t,x,y)=tM\_{ct}[\phi ]={\frac {t}{4\pi }}\iint \_{S}\phi (x+ct\alpha ,\,y+ct\beta )\,d\omega ,}$

where α and β are the first two coordinates on the unit sphere, and d*ω* is the area element on the sphere. This integral may be rewritten as a [double integral](https://en.wikipedia.org/wiki/Multiple_integral "Multiple integral") over the disc D with center (*x*, *y*) and radius *ct*:

${\displaystyle u(t,x,y)={\frac {1}{2\pi c}}\iint \_{D}{\frac {\phi (x+\xi ,y+\eta )}{\sqrt {(ct)^{2}-\xi ^{2}-\eta ^{2}}}}d\xi \,d\eta .}$${\displaystyle u(t,x,y)={\frac {1}{2\pi c}}\iint \_{D}{\frac {\phi (x+\xi ,y+\eta )}{\sqrt {(ct)^{2}-\xi ^{2}-\eta ^{2}}}}d\xi \,d\eta .}$

It is apparent that the solution at (*t*, *x*, *y*) depends not only on the data on the light cone where
${\displaystyle (x-\xi )^{2}+(y-\eta )^{2}=c^{2}t^{2},}$${\displaystyle (x-\xi )^{2}+(y-\eta )^{2}=c^{2}t^{2},}$
but also on data that are interior to that cone.

## Scalar wave equation in general dimension and Kirchhoff's formulae

We want to find solutions to *utt* − Δ*u* = 0 for *u* : **R***n* × (0, ∞) → **R** with *u*(*x*, 0) = *g*(*x*) and *ut*(*x*, 0) = *h*(*x*).

### Odd dimensions

Assume *n* ≥ 3 is an odd integer, and *g* ∈ *C**m*+1(**R***n*), *h* ∈ *Cm*(**R***n*) for *m* = (*n* + 1)/2. Let *γn* = 1 × 3 × 5 × ⋯ × (*n* − 2) and let

${\displaystyle u(x,t)={\frac {1}{\gamma \_{n}}}\left[\partial \_{t}\left({\frac {1}{t}}\partial \_{t}\right)^{\frac {n-3}{2}}\left(t^{n-2}{\frac {1}{|\partial B\_{t}(x)|}}\int \_{\partial B\_{t}(x)}g\,dS\right)+\left({\frac {1}{t}}\partial \_{t}\right)^{\frac {n-3}{2}}\left(t^{n-2}{\frac {1}{|\partial B\_{t}(x)|}}\int \_{\partial B\_{t}(x)}h\,dS\right)\right]}$${\displaystyle u(x,t)={\frac {1}{\gamma \_{n}}}\left[\partial \_{t}\left({\frac {1}{t}}\partial \_{t}\right)^{\frac {n-3}{2}}\left(t^{n-2}{\frac {1}{|\partial B\_{t}(x)|}}\int \_{\partial B\_{t}(x)}g\,dS\right)+\left({\frac {1}{t}}\partial \_{t}\right)^{\frac {n-3}{2}}\left(t^{n-2}{\frac {1}{|\partial B\_{t}(x)|}}\int \_{\partial B\_{t}(x)}h\,dS\right)\right]}$

Then

* ${\displaystyle u\in C^{2}{\big (}\mathbf {R} ^{n}\times [0,\infty ){\big )}}$${\displaystyle u\in C^{2}{\big (}\mathbf {R} ^{n}\times [0,\infty ){\big )}}$,
* ${\displaystyle u\_{tt}-\Delta u=0}$${\displaystyle u\_{tt}-\Delta u=0}$ in ${\displaystyle \mathbf {R} ^{n}\times (0,\infty )}$${\displaystyle \mathbf {R} ^{n}\times (0,\infty )}$,
* ${\displaystyle \lim \_{(x,t)\to (x^{0},0)}u(x,t)=g(x^{0})}$${\displaystyle \lim \_{(x,t)\to (x^{0},0)}u(x,t)=g(x^{0})}$,
* ${\displaystyle \lim \_{(x,t)\to (x^{0},0)}u\_{t}(x,t)=h(x^{0})}$${\displaystyle \lim \_{(x,t)\to (x^{0},0)}u\_{t}(x,t)=h(x^{0})}$.

### Even dimensions

Assume *n* ≥ 2 is an even integer and *g* ∈ *C**m*+1(**R***n*), *h* ∈ *Cm*(**R***n*), for *m* = (*n* + 2)/2. Let *γn* = 2 × 4 × ⋯ × *n* and let

${\displaystyle u(x,t)={\frac {1}{\gamma \_{n}}}\left[\partial \_{t}\left({\frac {1}{t}}\partial \_{t}\right)^{\frac {n-2}{2}}\left(t^{n}{\frac {1}{|B\_{t}(x)|}}\int \_{B\_{t}(x)}{\frac {g}{(t^{2}-|y-x|^{2})^{\frac {1}{2}}}}dy\right)+\left({\frac {1}{t}}\partial \_{t}\right)^{\frac {n-2}{2}}\left(t^{n}{\frac {1}{|B\_{t}(x)|}}\int \_{B\_{t}(x)}{\frac {h}{(t^{2}-|y-x|^{2})^{\frac {1}{2}}}}dy\right)\right]}$${\displaystyle u(x,t)={\frac {1}{\gamma \_{n}}}\left[\partial \_{t}\left({\frac {1}{t}}\partial \_{t}\right)^{\frac {n-2}{2}}\left(t^{n}{\frac {1}{|B\_{t}(x)|}}\int \_{B\_{t}(x)}{\frac {g}{(t^{2}-|y-x|^{2})^{\frac {1}{2}}}}dy\right)+\left({\frac {1}{t}}\partial \_{t}\right)^{\frac {n-2}{2}}\left(t^{n}{\frac {1}{|B\_{t}(x)|}}\int \_{B\_{t}(x)}{\frac {h}{(t^{2}-|y-x|^{2})^{\frac {1}{2}}}}dy\right)\right]}$

then

* *u* ∈ *C*2(**R***n* × [0, ∞))
* *utt* − Δ*u* = 0 in **R***n* × (0, ∞)
* ${\displaystyle \lim \_{(x,t)\to (x^{0},0)}u(x,t)=g(x^{0})}$${\displaystyle \lim \_{(x,t)\to (x^{0},0)}u(x,t)=g(x^{0})}$
* ${\displaystyle \lim \_{(x,t)\to (x^{0},0)}u\_{t}(x,t)=h(x^{0})}$${\displaystyle \lim \_{(x,t)\to (x^{0},0)}u\_{t}(x,t)=h(x^{0})}$

## Green's function

Consider the inhomogeneous wave equation in ${\displaystyle 1+D}$${\displaystyle 1+D}$ dimensions${\displaystyle (\partial \_{tt}-c^{2}\nabla ^{2})u=s(t,x)}$${\displaystyle (\partial \_{tt}-c^{2}\nabla ^{2})u=s(t,x)}$By rescaling time, we can set wave speed ${\displaystyle c=1}$${\displaystyle c=1}$.

Since the wave equation ${\displaystyle (\partial \_{tt}-\nabla ^{2})u=s(t,x)}$${\displaystyle (\partial \_{tt}-\nabla ^{2})u=s(t,x)}$ has order 2 in time, there are two [impulse responses](https://en.wikipedia.org/wiki/Impulse_response "Impulse response"): an acceleration impulse and a velocity impulse. The effect of inflicting an acceleration impulse is to suddenly change the wave velocity ${\displaystyle \partial \_{t}u}$${\displaystyle \partial \_{t}u}$. The effect of inflicting a velocity impulse is to suddenly change the wave displacement ${\displaystyle u}$${\displaystyle u}$.

For acceleration impulse, ${\displaystyle s(t,x)=\delta ^{D+1}(t,x)}$${\displaystyle s(t,x)=\delta ^{D+1}(t,x)}$ where ${\displaystyle \delta }$${\displaystyle \delta }$ is the [Dirac delta function](https://en.wikipedia.org/wiki/Dirac_delta_function "Dirac delta function"). The solution to this case is called the [Green's function](https://en.wikipedia.org/wiki/Green%27s_function "Green's function") ${\displaystyle G}$${\displaystyle G}$ for the wave equation.

For velocity impulse, ${\displaystyle s(t,x)=\partial \_{t}\delta ^{D+1}(t,x)}$${\displaystyle s(t,x)=\partial \_{t}\delta ^{D+1}(t,x)}$, so if we solve the Green function ${\displaystyle G}$${\displaystyle G}$, the solution for this case is just ${\displaystyle \partial \_{t}G}$${\displaystyle \partial \_{t}G}$.[*[citation needed](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed "Wikipedia:Citation needed")*]

### Duhamel's principle

The main use of Green's functions is to solve [initial value problems](https://en.wikipedia.org/wiki/Initial_value_problem "Initial value problem") by [Duhamel's principle](https://en.wikipedia.org/wiki/Duhamel%27s_principle "Duhamel's principle"), both for the homogeneous and the inhomogeneous case.

Given the Green function ${\displaystyle G}$${\displaystyle G}$, and initial conditions ${\displaystyle u(0,x),\partial \_{t}u(0,x)}$${\displaystyle u(0,x),\partial \_{t}u(0,x)}$, the solution to the homogeneous wave equation is${\displaystyle u=(\partial \_{t}G)\ast u+G\ast \partial \_{t}u}$${\displaystyle u=(\partial \_{t}G)\ast u+G\ast \partial \_{t}u}$where the asterisk is [convolution](https://en.wikipedia.org/wiki/Convolution "Convolution") in space. More explicitly, ${\displaystyle u(t,x)=\int (\partial \_{t}G)(t,x-x')u(0,x')dx'+\int G(t,x-x')(\partial \_{t}u)(0,x')dx'.}$${\displaystyle u(t,x)=\int (\partial \_{t}G)(t,x-x')u(0,x')dx'+\int G(t,x-x')(\partial \_{t}u)(0,x')dx'.}$For the inhomogeneous case, the solution has one additional term by convolution over spacetime:${\displaystyle \iint \_{t'<t}G(t-t',x-x')s(t',x')dt'dx'.}$${\displaystyle \iint \_{t'<t}G(t-t',x-x')s(t',x')dt'dx'.}$

### Solution by Fourier transform

By a [Fourier transform](https://en.wikipedia.org/wiki/Fourier_transform "Fourier transform"),${\displaystyle {\hat {G}}(\omega )={\frac {1}{-\omega \_{0}^{2}+\omega \_{1}^{2}+\cdots +\omega \_{D}^{2}}},\quad G(t,x)={\frac {1}{(2\pi )^{D+1}}}\int {\hat {G}}(\omega )e^{+i\omega \_{0}t+i{\vec {\omega }}\cdot {\vec {x}}}d\omega \_{0}d{\vec {\omega }}.}$${\displaystyle {\hat {G}}(\omega )={\frac {1}{-\omega \_{0}^{2}+\omega \_{1}^{2}+\cdots +\omega \_{D}^{2}}},\quad G(t,x)={\frac {1}{(2\pi )^{D+1}}}\int {\hat {G}}(\omega )e^{+i\omega \_{0}t+i{\vec {\omega }}\cdot {\vec {x}}}d\omega \_{0}d{\vec {\omega }}.}$The ${\displaystyle \omega \_{0}}$${\displaystyle \omega \_{0}}$ term can be integrated by the [residue theorem](https://en.wikipedia.org/wiki/Residue_theorem "Residue theorem"). It would require us to perturb the integral slightly either by ${\displaystyle +i\epsilon }$${\displaystyle +i\epsilon }$ or by ${\displaystyle -i\epsilon }$${\displaystyle -i\epsilon }$, because it is an [improper integral](https://en.wikipedia.org/wiki/Improper_integral "Improper integral"). One perturbation gives the forward solution, and the other the backward solution. The forward solution gives${\displaystyle G(t,x)={\frac {1}{(2\pi )^{D}}}\int {\frac {\sin(\|{\vec {\omega }}\|t)}{\|{\vec {\omega }}\|}}e^{i{\vec {\omega }}\cdot {\vec {x}}}d{\vec {\omega }},\quad \partial \_{t}G(t,x)={\frac {1}{(2\pi )^{D}}}\int \cos(\|{\vec {\omega }}\|t)e^{i{\vec {\omega }}\cdot {\vec {x}}}d{\vec {\omega }}.}$${\displaystyle G(t,x)={\frac {1}{(2\pi )^{D}}}\int {\frac {\sin(\|{\vec {\omega }}\|t)}{\|{\vec {\omega }}\|}}e^{i{\vec {\omega }}\cdot {\vec {x}}}d{\vec {\omega }},\quad \partial \_{t}G(t,x)={\frac {1}{(2\pi )^{D}}}\int \cos(\|{\vec {\omega }}\|t)e^{i{\vec {\omega }}\cdot {\vec {x}}}d{\vec {\omega }}.}$The integral can be solved by analytically continuing the [Poisson kernel](https://en.wikipedia.org/wiki/Poisson_kernel "Poisson kernel"), giving${\displaystyle G(t,x)=\lim \_{\epsilon \rightarrow 0^{+}}{\frac {C\_{D}}{D-1}}\operatorname {Im} \left[\|x\|^{2}-(t-i\epsilon )^{2}\right]^{-(D-1)/2}}$${\displaystyle G(t,x)=\lim \_{\epsilon \rightarrow 0^{+}}{\frac {C\_{D}}{D-1}}\operatorname {Im} \left[\|x\|^{2}-(t-i\epsilon )^{2}\right]^{-(D-1)/2}}$where ${\displaystyle C\_{D}=\pi ^{-(D+1)/2}\Gamma ((D+1)/2)}$${\displaystyle C\_{D}=\pi ^{-(D+1)/2}\Gamma ((D+1)/2)}$ is half the surface area of a ${\displaystyle (D+1)}$${\displaystyle (D+1)}$-dimensional [hypersphere](https://en.wikipedia.org/wiki/N-sphere "N-sphere").

### Solutions in particular dimensions

We can relate the Green's function in ${\displaystyle D}$${\displaystyle D}$ dimensions to the Green's function in ${\displaystyle D+n}$${\displaystyle D+n}$ dimensions (lowering the dimension is possible in any case, raising is possible in spherical symmetry).

#### Lowering dimensions

Given a function ${\displaystyle s(t,x)}$${\displaystyle s(t,x)}$ and a solution ${\displaystyle u(t,x)}$${\displaystyle u(t,x)}$ of a differential equation in ${\displaystyle (1+D)}$${\displaystyle (1+D)}$ dimensions, we can trivially extend it to ${\displaystyle (1+D+n)}$${\displaystyle (1+D+n)}$ dimensions by setting the additional ${\displaystyle n}$${\displaystyle n}$ dimensions to be constant:
${\displaystyle s(t,x\_{1:D},x\_{D+1:D+n})=s(t,x\_{1:D}),\quad u(t,x\_{1:D},x\_{D+1:D+n})=u(t,x\_{1:D}).}$${\displaystyle s(t,x\_{1:D},x\_{D+1:D+n})=s(t,x\_{1:D}),\quad u(t,x\_{1:D},x\_{D+1:D+n})=u(t,x\_{1:D}).}$Since the Green's function is constructed from ${\displaystyle s}$${\displaystyle s}$ and ${\displaystyle u}$${\displaystyle u}$, the Green's function in ${\displaystyle (1+D+n)}$${\displaystyle (1+D+n)}$ dimensions integrates to the Green's function in ${\displaystyle (1+D)}$${\displaystyle (1+D)}$ dimensions:
${\displaystyle G\_{D}(t,x\_{1:D})=\int \_{\mathbb {R} ^{n}}G\_{D+n}(t,x\_{1:D},x\_{D+1:D+n})d^{n}x\_{D+1:D+n}.}$${\displaystyle G\_{D}(t,x\_{1:D})=\int \_{\mathbb {R} ^{n}}G\_{D+n}(t,x\_{1:D},x\_{D+1:D+n})d^{n}x\_{D+1:D+n}.}$

#### Raising dimensions

The Green's function in ${\displaystyle D}$${\displaystyle D}$ dimensions can be related to the Green's function in ${\displaystyle D+2}$${\displaystyle D+2}$ dimensions. By spherical symmetry,
${\displaystyle G\_{D}(t,r)=\int \_{\mathbb {R} ^{2}}G\_{D+2}(t,{\sqrt {r^{2}+y^{2}+z^{2}}})dydz.}$${\displaystyle G\_{D}(t,r)=\int \_{\mathbb {R} ^{2}}G\_{D+2}(t,{\sqrt {r^{2}+y^{2}+z^{2}}})dydz.}$
Integrating in polar coordinates,
${\displaystyle G\_{D}(t,r)=2\pi \int \_{0}^{\infty }G\_{D+2}(t,{\sqrt {r^{2}+q^{2}}})qdq=2\pi \int \_{r}^{\infty }G\_{D+2}(t,q')q'dq',}$${\displaystyle G\_{D}(t,r)=2\pi \int \_{0}^{\infty }G\_{D+2}(t,{\sqrt {r^{2}+q^{2}}})qdq=2\pi \int \_{r}^{\infty }G\_{D+2}(t,q')q'dq',}$
where in the last equality we made the change of variables ${\displaystyle q'={\sqrt {r^{2}+q^{2}}}}$${\displaystyle q'={\sqrt {r^{2}+q^{2}}}}$. Thus, we obtain the recurrence relation${\displaystyle G\_{D+2}(t,r)=-{\frac {1}{2\pi r}}\partial \_{r}G\_{D}(t,r).}$${\displaystyle G\_{D+2}(t,r)=-{\frac {1}{2\pi r}}\partial \_{r}G\_{D}(t,r).}$

### Solutions in *D = 1, 2, 3*

When ${\displaystyle D=1}$${\displaystyle D=1}$, the integrand in the Fourier transform is the [sinc function](https://en.wikipedia.org/wiki/Sinc_function "Sinc function")${\displaystyle {\begin{aligned}G\_{1}(t,x)&={\frac {1}{2\pi }}\int \_{\mathbb {R} }{\frac {\sin(|\omega |t)}{|\omega |}}e^{i\omega x}d\omega \\&={\frac {1}{2\pi }}\int \operatorname {sinc} (\omega )e^{i\omega {\frac {x}{t}}}d\omega \\&={\frac {\operatorname {sgn}(t-x)+\operatorname {sgn}(t+x)}{4}}\\&={\begin{cases}{\frac {1}{2}}\theta (t-|x|)\quad t>0\\-{\frac {1}{2}}\theta (-t-|x|)\quad t<0\end{cases}}\end{aligned}}}$${\displaystyle {\begin{aligned}G\_{1}(t,x)&={\frac {1}{2\pi }}\int \_{\mathbb {R} }{\frac {\sin(|\omega |t)}{|\omega |}}e^{i\omega x}d\omega \\&={\frac {1}{2\pi }}\int \operatorname {sinc} (\omega )e^{i\omega {\frac {x}{t}}}d\omega \\&={\frac {\operatorname {sgn} (t-x)+\operatorname {sgn} (t+x)}{4}}\\&={\begin{cases}{\frac {1}{2}}\theta (t-|x|)\quad t>0\\-{\frac {1}{2}}\theta (-t-|x|)\quad t<0\end{cases}}\end{aligned}}}$
where ${\displaystyle \operatorname {sgn} }$${\displaystyle \operatorname {sgn} }$ is the [sign function](https://en.wikipedia.org/wiki/Sign_function "Sign function") and ${\displaystyle \theta }$${\displaystyle \theta }$ is the [unit step function](https://en.wikipedia.org/wiki/Heaviside_step_function "Heaviside step function").

The dimension can be raised to give the ${\displaystyle D=3}$${\displaystyle D=3}$ case${\displaystyle G\_{3}(t,r)={\frac {\delta (t-r)}{4\pi r}}}$${\displaystyle G\_{3}(t,r)={\frac {\delta (t-r)}{4\pi r}}}$and similarly for the backward solution. This can be integrated down by one dimension to give the ${\displaystyle D=2}$${\displaystyle D=2}$ case${\displaystyle G\_{2}(t,r)=\int \_{\mathbb {R} }{\frac {\delta (t-{\sqrt {r^{2}+z^{2}}})}{4\pi {\sqrt {r^{2}+z^{2}}}}}dz={\frac {\theta (t-r)}{2\pi {\sqrt {t^{2}-r^{2}}}}}}$${\displaystyle G\_{2}(t,r)=\int \_{\mathbb {R} }{\frac {\delta (t-{\sqrt {r^{2}+z^{2}}})}{4\pi {\sqrt {r^{2}+z^{2}}}}}dz={\frac {\theta (t-r)}{2\pi {\sqrt {t^{2}-r^{2}}}}}}$

### Wavefronts and wakes

In ${\displaystyle D=1}$${\displaystyle D=1}$ case, the Green's function solution is the sum of two wavefronts ${\displaystyle {\frac {\operatorname {sgn}(t-x)}{4}}+{\frac {\operatorname {sgn}(t+x)}{4}}}$${\displaystyle {\frac {\operatorname {sgn} (t-x)}{4}}+{\frac {\operatorname {sgn} (t+x)}{4}}}$ moving in opposite directions.

In odd dimensions, the forward solution is nonzero only at ${\displaystyle t=r}$${\displaystyle t=r}$. As the dimensions increase, the shape of wavefront becomes increasingly complex, involving higher derivatives of the Dirac delta function. For example,${\displaystyle {\begin{aligned}&G\_{1}={\frac {1}{2c}}\theta (\tau )\\&G\_{3}={\frac {1}{4\pi c^{2}}}{\frac {\delta (\tau )}{r}}\\&G\_{5}={\frac {1}{8\pi ^{2}c^{2}}}\left({\frac {\delta (\tau )}{r^{3}}}+{\frac {\delta ^{\prime }(\tau )}{cr^{2}}}\right)\\&G\_{7}={\frac {1}{16\pi ^{3}c^{2}}}\left(3{\frac {\delta (\tau )}{r^{4}}}+3{\frac {\delta ^{\prime }(\tau )}{cr^{3}}}+{\frac {\delta ^{\prime \prime }(\tau )}{c^{2}r^{2}}}\right)\end{aligned}}}$${\displaystyle {\begin{aligned}&G\_{1}={\frac {1}{2c}}\theta (\tau )\\&G\_{3}={\frac {1}{4\pi c^{2}}}{\frac {\delta (\tau )}{r}}\\&G\_{5}={\frac {1}{8\pi ^{2}c^{2}}}\left({\frac {\delta (\tau )}{r^{3}}}+{\frac {\delta ^{\prime }(\tau )}{cr^{2}}}\right)\\&G\_{7}={\frac {1}{16\pi ^{3}c^{2}}}\left(3{\frac {\delta (\tau )}{r^{4}}}+3{\frac {\delta ^{\prime }(\tau )}{cr^{3}}}+{\frac {\delta ^{\prime \prime }(\tau )}{c^{2}r^{2}}}\right)\end{aligned}}}$where ${\displaystyle \tau =t-r}$${\displaystyle \tau =t-r}$, and the wave speed ${\displaystyle c}$${\displaystyle c}$ is restored.

In even dimensions, the forward solution is nonzero in ${\displaystyle r\leq t}$${\displaystyle r\leq t}$, the entire region behind the wavefront becomes nonzero, called a [wake](https://en.wikipedia.org/wiki/Wake_(physics) "Wake (physics)"). The wake has equation:${\displaystyle G\_{D}(t,x)=(-1)^{1+D/2}{\frac {1}{(2\pi )^{D/2}}}{\frac {1}{c^{D}}}{\frac {\theta (t-r/c)}{\left(t^{2}-r^{2}/c^{2}\right)^{(D-1)/2}}}}$${\displaystyle G\_{D}(t,x)=(-1)^{1+D/2}{\frac {1}{(2\pi )^{D/2}}}{\frac {1}{c^{D}}}{\frac {\theta (t-r/c)}{\left(t^{2}-r^{2}/c^{2}\right)^{(D-1)/2}}}}$The wavefront itself also involves increasingly higher derivatives of the Dirac delta function.

This means that a general [Huygens' principle](https://en.wikipedia.org/wiki/Huygens%E2%80%93Fresnel_principle "Huygens–Fresnel principle") – the wave displacement at a point ${\displaystyle (t,x)}$${\displaystyle (t,x)}$ in spacetime depends only on the state at points on [characteristic rays](https://en.wikipedia.org/wiki/Method_of_characteristics "Method of characteristics") passing ${\displaystyle (t,x)}$${\displaystyle (t,x)}$ – only holds in odd dimensions. A physical interpretation is that signals transmitted by waves remain undistorted in odd dimensions, but distorted in even dimensions.

**Hadamard's conjecture** states that this generalized Huygens' principle still holds in all odd dimensions even when the coefficients in the wave equation are no longer constant. It is not strictly correct, but it is correct for certain families of coefficients

## Problems with boundaries

### One space dimension

#### Reflection and transmission at the boundary of two media

For an incident wave traveling from one medium (where the wave speed is *c*1) to another medium (where the wave speed is *c*2), one part of the wave will transmit into the second medium, while another part reflects back into the other direction and stays in the first medium. The amplitude of the transmitted wave and the reflected wave can be calculated by using the continuity condition at the boundary.

Consider the component of the incident wave with an [angular frequency](https://en.wikipedia.org/wiki/Angular_frequency "Angular frequency") of ω, which has the waveform
${\displaystyle u^{\text{inc}}(x,t)=Ae^{i(k\_{1}x-\omega t)},\quad A\in \mathbb {C} .}$${\displaystyle u^{\text{inc}}(x,t)=Ae^{i(k\_{1}x-\omega t)},\quad A\in \mathbb {C} .}$
At *t* = 0, the incident reaches the boundary between the two media at *x* = 0. Therefore, the corresponding reflected wave and the transmitted wave will have the waveforms
${\displaystyle u^{\text{refl}}(x,t)=Be^{i(-k\_{1}x-\omega t)},\quad u^{\text{trans}}(x,t)=Ce^{i(k\_{2}x-\omega t)},\quad B,C\in \mathbb {C} .}$${\displaystyle u^{\text{refl}}(x,t)=Be^{i(-k\_{1}x-\omega t)},\quad u^{\text{trans}}(x,t)=Ce^{i(k\_{2}x-\omega t)},\quad B,C\in \mathbb {C} .}$
The continuity condition at the boundary is
${\displaystyle u^{\text{inc}}(0,t)+u^{\text{refl}}(0,t)=u^{\text{trans}}(0,t),\quad u\_{x}^{\text{inc}}(0,t)+u\_{x}^{\text{ref}}(0,t)=u\_{x}^{\text{trans}}(0,t).}$${\displaystyle u^{\text{inc}}(0,t)+u^{\text{refl}}(0,t)=u^{\text{trans}}(0,t),\quad u\_{x}^{\text{inc}}(0,t)+u\_{x}^{\text{ref}}(0,t)=u\_{x}^{\text{trans}}(0,t).}$
This gives the equations
${\displaystyle A+B=C,\quad A-B={\frac {k\_{2}}{k\_{1}}}C={\frac {c\_{1}}{c\_{2}}}C,}$${\displaystyle A+B=C,\quad A-B={\frac {k\_{2}}{k\_{1}}}C={\frac {c\_{1}}{c\_{2}}}C,}$
and we have the reflectivity and transmissivity
${\displaystyle {\frac {B}{A}}={\frac {c\_{2}-c\_{1}}{c\_{2}+c\_{1}}},\quad {\frac {C}{A}}={\frac {2c\_{2}}{c\_{2}+c\_{1}}}.}$${\displaystyle {\frac {B}{A}}={\frac {c\_{2}-c\_{1}}{c\_{2}+c\_{1}}},\quad {\frac {C}{A}}={\frac {2c\_{2}}{c\_{2}+c\_{1}}}.}$
When *c*2 < *c*1, the reflected wave has a [reflection phase change](https://en.wikipedia.org/wiki/Reflection_phase_change "Reflection phase change") of 180°, since *B*/*A* < 0. The energy conservation can be verified by
${\displaystyle {\frac {B^{2}}{c\_{1}}}+{\frac {C^{2}}{c\_{2}}}={\frac {A^{2}}{c\_{1}}}.}$${\displaystyle {\frac {B^{2}}{c\_{1}}}+{\frac {C^{2}}{c\_{2}}}={\frac {A^{2}}{c\_{1}}}.}$
The above discussion holds true for any component, regardless of its angular frequency of ω.

The limiting case of *c*2 = 0 corresponds to a "fixed end" that does not move, whereas the limiting case of *c*2 → ∞ corresponds to a "free end".

#### The Sturm–Liouville formulation

A flexible string that is stretched between two points *x* = 0 and *x* = *L* satisfies the wave equation for *t* > 0 and 0 < *x* < *L*. On the boundary points, u may satisfy a variety of boundary conditions. A general form that is appropriate for applications is

${\displaystyle {\begin{aligned}-u\_{x}(t,0)+au(t,0)&=0,\\u\_{x}(t,L)+bu(t,L)&=0,\end{aligned}}}$${\displaystyle {\begin{aligned}-u\_{x}(t,0)+au(t,0)&=0,\\u\_{x}(t,L)+bu(t,L)&=0,\end{aligned}}}$

where a and b are non-negative. The case where u is required to vanish at an endpoint (i.e. "fixed end") is the limit of this condition when the respective a or b approaches infinity. The method of [separation of variables](https://en.wikipedia.org/wiki/Separation_of_variables "Separation of variables") consists in looking for solutions of this problem in the special form
${\displaystyle u(t,x)=T(t)v(x).}$${\displaystyle u(t,x)=T(t)v(x).}$

A consequence is that
${\displaystyle {\frac {T''}{c^{2}T}}={\frac {v''}{v}}=-\lambda .}$${\displaystyle {\frac {T''}{c^{2}T}}={\frac {v''}{v}}=-\lambda .}$

The [eigenvalue](https://en.wikipedia.org/wiki/Eigenvalue "Eigenvalue") λ must be determined so that there is a non-trivial solution of the boundary-value problem
${\displaystyle {\begin{aligned}v''+\lambda v=0,&\\-v'(0)+av(0)&=0,\\v'(L)+bv(L)&=0.\end{aligned}}}$${\displaystyle {\begin{aligned}v''+\lambda v=0,&\\-v'(0)+av(0)&=0,\\v'(L)+bv(L)&=0.\end{aligned}}}$

This is a special case of the general problem of [Sturm–Liouville theory](https://en.wikipedia.org/wiki/Sturm%E2%80%93Liouville_theory "Sturm–Liouville theory"). If a and b are positive, the eigenvalues are all positive, and the solutions are [trigonometric functions](https://en.wikipedia.org/wiki/Trigonometric_functions "Trigonometric functions"). A solution that satisfies square-integrable initial conditions for u and *ut* can be obtained from expansion of these functions in the appropriate trigonometric series.

### Several space dimensions

[![](//upload.wikimedia.org/wikipedia/commons/e/e9/Drum_vibration_mode12.gif)](https://en.wikipedia.org/wiki/File:Drum_vibration_mode12.gif)

A solution of the wave equation in two dimensions with a zero-displacement boundary condition along the entire outer edge

The one-dimensional initial-boundary value theory may be extended to an arbitrary number of space dimensions. Consider a domain D in m-dimensional x space, with boundary B. Then the wave equation is to be satisfied if x is in D, and *t* > 0. On the boundary of D, the solution u shall satisfy

${\displaystyle {\frac {\partial u}{\partial n}}+au=0,}$${\displaystyle {\frac {\partial u}{\partial n}}+au=0,}$

where n is the unit outward normal to B, and a is a non-negative function defined on B. The case where u vanishes on B is a limiting case for a approaching infinity. The initial conditions are

${\displaystyle u(0,x)=f(x),\quad u\_{t}(0,x)=g(x),}$${\displaystyle u(0,x)=f(x),\quad u\_{t}(0,x)=g(x),}$

where f and g are defined in D. This problem may be solved by expanding f and g in the eigenfunctions of the Laplacian in D, which satisfy the boundary conditions. Thus the eigenfunction v satisfies

${\displaystyle \nabla \cdot \nabla v+\lambda v=0}$${\displaystyle \nabla \cdot \nabla v+\lambda v=0}$

in D, and

${\displaystyle {\frac {\partial v}{\partial n}}+av=0}$${\displaystyle {\frac {\partial v}{\partial n}}+av=0}$

on B.

In the case of two space dimensions, the eigenfunctions may be interpreted as the modes of vibration of a drumhead stretched over the boundary B. If B is a circle, then these eigenfunctions have an angular component that is a trigonometric function of the polar angle θ, multiplied by a [Bessel function](https://en.wikipedia.org/wiki/Bessel_function "Bessel function") (of integer order) of the radial component. Further details are in [Helmholtz equation](https://en.wikipedia.org/wiki/Helmholtz_equation "Helmholtz equation").

If the boundary is a sphere in three space dimensions, the angular components of the eigenfunctions are [spherical harmonics](https://en.wikipedia.org/wiki/Spherical_harmonics "Spherical harmonics"), and the radial components are [Bessel functions](https://en.wikipedia.org/wiki/Bessel_function "Bessel function") of half-integer order.

## Inhomogeneous wave equation in one dimension

The inhomogeneous wave equation in one dimension is
${\displaystyle u\_{tt}(x,t)-c^{2}u\_{xx}(x,t)=s(x,t)}$${\displaystyle u\_{tt}(x,t)-c^{2}u\_{xx}(x,t)=s(x,t)}$
with initial conditions
${\displaystyle u(x,0)=f(x),}$${\displaystyle u(x,0)=f(x),}$
${\displaystyle u\_{t}(x,0)=g(x).}$${\displaystyle u\_{t}(x,0)=g(x).}$

The function *s*(*x*, *t*) is often called the source function because in practice it describes the effects of the sources of waves on the medium carrying them. Physical examples of source functions include the force driving a wave on a string, or the charge or current density in the [Lorenz gauge](https://en.wikipedia.org/wiki/Lorenz_gauge "Lorenz gauge") of [electromagnetism](https://en.wikipedia.org/wiki/Electromagnetism "Electromagnetism").

One method to solve the initial-value problem (with the initial values as posed above) is to take advantage of a special property of the wave equation in an odd number of space dimensions, namely that its solutions respect causality. That is, for any point (*xi*, *ti*), the value of *u*(*xi*, *ti*) depends only on the values of *f*(*xi* + *cti*) and *f*(*xi* − *cti*) and the values of the function *g*(*x*) between (*xi* − *cti*) and (*xi* + *cti*). This can be seen in [d'Alembert's formula](https://en.wikipedia.org/wiki/D%27Alembert%27s_formula "D'Alembert's formula"), stated above, where these quantities are the only ones that show up in it. Physically, if the maximum propagation speed is c, then no part of the wave that cannot propagate to a given point by a given time can affect the amplitude at the same point and time.

In terms of finding a solution, this causality property means that for any given point on the line being considered, the only area that needs to be considered is the area encompassing all the points that could causally affect the point being considered. Denote the area that causally affects point (*xi*, *ti*) as *RC*. Suppose we integrate the inhomogeneous wave equation over this region:
${\displaystyle \iint \_{R\_{C}}{\big (}c^{2}u\_{xx}(x,t)-u\_{tt}(x,t){\big )}\,dx\,dt=\iint \_{R\_{C}}s(x,t)\,dx\,dt.}$${\displaystyle \iint \_{R\_{C}}{\big (}c^{2}u\_{xx}(x,t)-u\_{tt}(x,t){\big )}\,dx\,dt=\iint \_{R\_{C}}s(x,t)\,dx\,dt.}$

To simplify this greatly, we can use [Green's theorem](https://en.wikipedia.org/wiki/Green%27s_theorem "Green's theorem") to simplify the left side to get the following:
${\displaystyle \int \_{L\_{0}+L\_{1}+L\_{2}}{\big (}{-}c^{2}u\_{x}(x,t)\,dt-u\_{t}(x,t)\,dx{\big )}=\iint \_{R\_{C}}s(x,t)\,dx\,dt.}$${\displaystyle \int \_{L\_{0}+L\_{1}+L\_{2}}{\big (}{-}c^{2}u\_{x}(x,t)\,dt-u\_{t}(x,t)\,dx{\big )}=\iint \_{R\_{C}}s(x,t)\,dx\,dt.}$

The left side is now the sum of three line integrals along the bounds of the causality region. These turn out to be fairly easy to compute:
${\displaystyle \int \_{x\_{i}-ct\_{i}}^{x\_{i}+ct\_{i}}-u\_{t}(x,0)\,dx=-\int \_{x\_{i}-ct\_{i}}^{x\_{i}+ct\_{i}}g(x)\,dx.}$${\displaystyle \int \_{x\_{i}-ct\_{i}}^{x\_{i}+ct\_{i}}-u\_{t}(x,0)\,dx=-\int \_{x\_{i}-ct\_{i}}^{x\_{i}+ct\_{i}}g(x)\,dx.}$

In the above, the term to be integrated with respect to time disappears because the time interval involved is zero, thus *dt* = 0.

For the other two sides of the region, it is worth noting that *x* ± *ct* is a constant, namely *xi* ± *cti*, where the sign is chosen appropriately. Using this, we can get the relation d*x* ± *c*d*t* = 0, again choosing the right sign:
${\displaystyle {\begin{aligned}\int \_{L\_{1}}{\big (}{-}c^{2}u\_{x}(x,t)\,dt-u\_{t}(x,t)\,dx{\big )}&=\int \_{L\_{1}}{\big (}cu\_{x}(x,t)\,dx+cu\_{t}(x,t)\,dt{\big )}\\&=c\int \_{L\_{1}}\,du(x,t)\\&=cu(x\_{i},t\_{i})-cf(x\_{i}+ct\_{i}).\end{aligned}}}$${\displaystyle {\begin{aligned}\int \_{L\_{1}}{\big (}{-}c^{2}u\_{x}(x,t)\,dt-u\_{t}(x,t)\,dx{\big )}&=\int \_{L\_{1}}{\big (}cu\_{x}(x,t)\,dx+cu\_{t}(x,t)\,dt{\big )}\\&=c\int \_{L\_{1}}\,du(x,t)\\&=cu(x\_{i},t\_{i})-cf(x\_{i}+ct\_{i}).\end{aligned}}}$

And similarly for the final boundary segment:
${\displaystyle {\begin{aligned}\int \_{L\_{2}}{\big (}{-}c^{2}u\_{x}(x,t)\,dt-u\_{t}(x,t)\,dx{\big )}&=-\int \_{L\_{2}}{\big (}cu\_{x}(x,t)\,dx+cu\_{t}(x,t)\,dt{\big )}\\&=-c\int \_{L\_{2}}\,du(x,t)\\&=cu(x\_{i},t\_{i})-cf(x\_{i}-ct\_{i}).\end{aligned}}}$${\displaystyle {\begin{aligned}\int \_{L\_{2}}{\big (}{-}c^{2}u\_{x}(x,t)\,dt-u\_{t}(x,t)\,dx{\big )}&=-\int \_{L\_{2}}{\big (}cu\_{x}(x,t)\,dx+cu\_{t}(x,t)\,dt{\big )}\\&=-c\int \_{L\_{2}}\,du(x,t)\\&=cu(x\_{i},t\_{i})-cf(x\_{i}-ct\_{i}).\end{aligned}}}$

Adding the three results together and putting them back in the original integral gives
${\displaystyle {\begin{aligned}\iint \_{R\_{C}}s(x,t)\,dx\,dt&=-\int \_{x\_{i}-ct\_{i}}^{x\_{i}+ct\_{i}}g(x)\,dx+cu(x\_{i},t\_{i})-cf(x\_{i}+ct\_{i})+cu(x\_{i},t\_{i})-cf(x\_{i}-ct\_{i})\\&=2cu(x\_{i},t\_{i})-cf(x\_{i}+ct\_{i})-cf(x\_{i}-ct\_{i})-\int \_{x\_{i}-ct\_{i}}^{x\_{i}+ct\_{i}}g(x)\,dx.\end{aligned}}}$${\displaystyle {\begin{aligned}\iint \_{R\_{C}}s(x,t)\,dx\,dt&=-\int \_{x\_{i}-ct\_{i}}^{x\_{i}+ct\_{i}}g(x)\,dx+cu(x\_{i},t\_{i})-cf(x\_{i}+ct\_{i})+cu(x\_{i},t\_{i})-cf(x\_{i}-ct\_{i})\\&=2cu(x\_{i},t\_{i})-cf(x\_{i}+ct\_{i})-cf(x\_{i}-ct\_{i})-\int \_{x\_{i}-ct\_{i}}^{x\_{i}+ct\_{i}}g(x)\,dx.\end{aligned}}}$

Solving for *u*(*xi*, *ti*), we arrive at
${\displaystyle u(x\_{i},t\_{i})={\frac {f(x\_{i}+ct\_{i})+f(x\_{i}-ct\_{i})}{2}}+{\frac {1}{2c}}\int \_{x\_{i}-ct\_{i}}^{x\_{i}+ct\_{i}}g(x)\,dx+{\frac {1}{2c}}\int \_{0}^{t\_{i}}\int \_{x\_{i}-c(t\_{i}-t)}^{x\_{i}+c(t\_{i}-t)}s(x,t)\,dx\,dt.}$${\displaystyle u(x\_{i},t\_{i})={\frac {f(x\_{i}+ct\_{i})+f(x\_{i}-ct\_{i})}{2}}+{\frac {1}{2c}}\int \_{x\_{i}-ct\_{i}}^{x\_{i}+ct\_{i}}g(x)\,dx+{\frac {1}{2c}}\int \_{0}^{t\_{i}}\int \_{x\_{i}-c(t\_{i}-t)}^{x\_{i}+c(t\_{i}-t)}s(x,t)\,dx\,dt.}$

In the last equation of the sequence, the bounds of the integral over the source function have been made explicit. Looking at this solution, which is valid for all choices (*xi*, *ti*) compatible with the wave equation, it is clear that the first two terms are simply d'Alembert's formula, as stated above as the solution of the homogeneous wave equation in one dimension. The difference is in the third term, the integral over the source.

## Further generalizations

### Elastic waves

The elastic wave equation (also known as the [Navier–Cauchy equation](https://en.wikipedia.org/wiki/Linear_elasticity#Elastodynamics_in_terms_of_displacements "Linear elasticity")) in three dimensions describes the propagation of waves in an [isotropic](https://en.wikipedia.org/wiki/Isotropic "Isotropic") [homogeneous](https://en.wikipedia.org/wiki/Homogeneity_(physics) "Homogeneity (physics)") [elastic](https://en.wikipedia.org/wiki/Elastic_(solid_mechanics) "Elastic (solid mechanics)") medium. Most solid materials are elastic, so this equation describes such phenomena as [seismic waves](https://en.wikipedia.org/wiki/Seismic_waves "Seismic waves") in the [Earth](https://en.wikipedia.org/wiki/Earth "Earth") and [ultrasonic](https://en.wikipedia.org/wiki/Ultrasound "Ultrasound") waves used to detect flaws in materials. While linear, this equation has a more complex form than the equations given above, as it must account for both longitudinal and transverse motion:
${\displaystyle \rho {\ddot {\mathbf {u} }}=\mathbf {f} +(\lambda +2\mu )\nabla (\nabla \cdot \mathbf {u} )-\mu \nabla \times (\nabla \times \mathbf {u} ),}$${\displaystyle \rho {\ddot {\mathbf {u} }}=\mathbf {f} +(\lambda +2\mu )\nabla (\nabla \cdot \mathbf {u} )-\mu \nabla \times (\nabla \times \mathbf {u} ),}$
where:

:   λ and μ are the so-called [Lamé parameters](https://en.wikipedia.org/wiki/Lam%C3%A9_parameters "Lamé parameters") describing the elastic properties of the medium,
:   ρ is the density,
:   **f** is the source function (driving force),
:   **u** is the displacement vector.

By using ∇ × (∇ × **u**) = ∇(∇ ⋅ **u**) − ∇ ⋅ ∇ **u** = ∇(∇ ⋅ **u**) − ∆**u**, the elastic wave equation can be rewritten into the more common form of the Navier–Cauchy equation.

Note that in the elastic wave equation, both force and displacement are [vector](https://en.wikipedia.org/wiki/Vector_(geometry) "Vector (geometry)") quantities. Thus, this equation is sometimes known as the vector wave equation.
As an aid to understanding, the reader will observe that if **f** and ∇ ⋅ **u** are set to zero, this becomes (effectively) Maxwell's equation for the propagation of the [electric field](https://en.wikipedia.org/wiki/Electric_field "Electric field") **E**, which has only transverse waves.

### Dispersion relation

In [dispersive](https://en.wikipedia.org/wiki/Dispersion_(optics) "Dispersion (optics)") wave phenomena, the speed of wave propagation varies with the wavelength of the wave, which is reflected by a [dispersion relation](https://en.wikipedia.org/wiki/Dispersion_relation "Dispersion relation")

${\displaystyle \omega =\omega (\mathbf {k} ),}$${\displaystyle \omega =\omega (\mathbf {k} ),}$

where ω is the [angular frequency](https://en.wikipedia.org/wiki/Angular_frequency "Angular frequency"), and **k** is the [wavevector](https://en.wikipedia.org/wiki/Wavevector "Wavevector") describing [plane-wave](https://en.wikipedia.org/wiki/Plane-wave "Plane-wave") solutions. For light waves, the dispersion relation is *ω* = ±*c* |**k**|, but in general, the constant speed c gets replaced by a variable [phase velocity](https://en.wikipedia.org/wiki/Phase_velocity "Phase velocity"):

${\displaystyle v\_{\text{p}}={\frac {\omega (k)}{k}}.}$${\displaystyle v\_{\text{p}}={\frac {\omega (k)}{k}}.}$

## See also

* [Acoustic attenuation](https://en.wikipedia.org/wiki/Acoustic_attenuation "Acoustic attenuation")
* [Acoustic wave equation](https://en.wikipedia.org/wiki/Acoustic_wave_equation "Acoustic wave equation")
* [Bateman transform](https://en.wikipedia.org/wiki/Bateman_transform "Bateman transform")
* [Electromagnetic wave equation](https://en.wikipedia.org/wiki/Electromagnetic_wave_equation "Electromagnetic wave equation")
* [Helmholtz equation](https://en.wikipedia.org/wiki/Helmholtz_equation "Helmholtz equation")
* [Inhomogeneous electromagnetic wave equation](https://en.wikipedia.org/wiki/Inhomogeneous_electromagnetic_wave_equation "Inhomogeneous electromagnetic wave equation")
* [Laplace operator](https://en.wikipedia.org/wiki/Laplace_operator "Laplace operator")
* [Mathematics of oscillation](https://en.wikipedia.org/wiki/Mathematics_of_oscillation "Mathematics of oscillation")
* [Maxwell's equations](https://en.wikipedia.org/wiki/Maxwell%27s_equations "Maxwell's equations")
* [Schrödinger equation](https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation "Schrödinger equation")
* [Standing wave](https://en.wikipedia.org/wiki/Standing_wave "Standing wave")
* [Vibrations of a circular membrane](https://en.wikipedia.org/wiki/Vibrations_of_a_circular_membrane "Vibrations of a circular membrane")
* [Wheeler–Feynman absorber theory](https://en.wikipedia.org/wiki/Wheeler%E2%80%93Feynman_absorber_theory "Wheeler–Feynman absorber theory")

## Notes

1. Speiser, David. *[Discovering the Principles of Mechanics 1600–1800](https://books.google.com/books?id=9uf97reZZCUC&pg=PA191)*, p. 191 (Basel: Birkhäuser, 2008).
2. Tipler, Paul and Mosca, Gene. *[Physics for Scientists and Engineers, Volume 1: Mechanics, Oscillations and Waves; Thermodynamics](https://books.google.com/books?id=upa42dyhf38C&pg=PA470)*, pp. 470–471 (Macmillan, 2004).
3. [Eric W. Weisstein](https://en.wikipedia.org/wiki/Eric_W._Weisstein "Eric W. Weisstein"). ["d'Alembert's Solution"](http://mathworld.wolfram.com/dAlembertsSolution.html). [MathWorld](https://en.wikipedia.org/wiki/MathWorld "MathWorld"). Retrieved 2009-01-21.
4. D'Alembert (1747) ["Recherches sur la courbe que forme une corde tenduë mise en vibration"](https://books.google.com/books?id=lJQDAAAAMAAJ&pg=PA214) (Researches on the curve that a tense cord forms [when] set into vibration), *Histoire de l'académie royale des sciences et belles lettres de Berlin*, vol. 3, p. 214–219.
   * See also: D'Alembert (1747) ["Suite des recherches sur la courbe que forme une corde tenduë mise en vibration"](https://books.google.com/books?id=lJQDAAAAMAAJ&pg=PA220) (Further researches on the curve that a tense cord forms [when] set into vibration), *Histoire de l'académie royale des sciences et belles lettres de Berlin*, vol. 3, p. 220–249.
   * See also: D'Alembert (1750) ["Addition au mémoire sur la courbe que forme une corde tenduë mise en vibration,"](https://books.google.com/books?id=m5UDAAAAMAAJ&pg=PA355) *Histoire de l'académie royale des sciences et belles lettres de Berlin*, vol. 6, p. 355–360.
5. ["First and second order linear wave equations"](https://web.archive.org/web/20171215022442/http://math.arizona.edu/~kglasner/math456/linearwave.pdf) (PDF). *math.arizona.edu*. Archived from [the original](http://math.arizona.edu/~kglasner/math456/linearwave.pdf) (PDF) on 2017-12-15.
6. V. Guruprasad (2015). "Observational evidence for travelling wave modes bearing distance proportional shifts". *[EPL](https://en.wikipedia.org/wiki/Europhysics_Letters "Europhysics Letters")*. **110** (5) 54001. [arXiv](https://en.wikipedia.org/wiki/ArXiv_(identifier) "ArXiv (identifier)"):[1507.08222](https://arxiv.org/abs/1507.08222). [Bibcode](https://en.wikipedia.org/wiki/Bibcode_(identifier) "Bibcode (identifier)"):[2015EL....11054001G](https://ui.adsabs.harvard.edu/abs/2015EL....11054001G). [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.1209/0295-5075/110/54001](https://doi.org/10.1209%2F0295-5075%2F110%2F54001). [S2CID](https://en.wikipedia.org/wiki/S2CID_(identifier) "S2CID (identifier)") [42285652](https://api.semanticscholar.org/CorpusID:42285652).
7. Bschorr, Oskar; Raida, Hans-Joachim (April 2021). ["Spherical One-Way Wave Equation"](https://doi.org/10.3390%2Facoustics3020021). *Acoustics*. **3** (2): 309–315. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.3390/acoustics3020021](https://doi.org/10.3390%2Facoustics3020021). [![](//upload.wikimedia.org/wikipedia/commons/thumb/e/e1/CC_BY_icon.svg/60px-CC_BY_icon.svg.png)](https://en.wikipedia.org/wiki/File:CC_BY_icon.svg) Text was copied from this source, which is available under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
8. Raida, Hans-Joachim (October 2022). ["One-Way Wave Operator"](https://doi.org/10.3390%2Facoustics4040053). *Acoustics*. **4** (4): 885–893. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.3390/acoustics4040053](https://doi.org/10.3390%2Facoustics4040053).
9. Bschorr, Oskar; Raida, Hans-Joachim (December 2021). ["Factorized One-way Wave Equations"](https://doi.org/10.3390%2Facoustics3040045). *Acoustics*. **3** (4): 714–722. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.3390/acoustics3040045](https://doi.org/10.3390%2Facoustics3040045).
10. Jackson, John David (14 August 1998). *Classical Electrodynamics* (3rd ed.). Wiley. p. 425. [ISBN](https://en.wikipedia.org/wiki/ISBN_(identifier) "ISBN (identifier)") [978-0-471-30932-1](https://en.wikipedia.org/wiki/Special:BookSources/978-0-471-30932-1 "Special:BookSources/978-0-471-30932-1").
11. [Atiyah, Bott & Gårding 1970](#CITEREFAtiyahBottGårding1970), pp. 109–189.
12. [Atiyah, Bott & Gårding 1973](#CITEREFAtiyahBottGårding1973), pp. 145–206.
13. [Evans 2010](#CITEREFEvans2010), pp. 70–80.
14. Barnett, Alex H. (December 28, 2006). ["Greens Functions for the Wave Equation"](https://users.flatironinstitute.org/~ahb/notes/waveequation.pdf) (PDF). *users.flatironinstitute.org*. Retrieved August 25, 2024.
15. ["The green function of the wave equation"](http://julian.tau.ac.il/bqs/em/green.pdf) (PDF). *julian.tau.ac.il*. Retrieved 2024-09-03.
16. Taylor, Michael E. (2023), Taylor, Michael E. (ed.), ["The Laplace Equation and Wave Equation"](https://link.springer.com/chapter/10.1007/978-3-031-33859-5_2), *Partial Differential Equations I: Basic Theory*, Applied Mathematical Sciences, vol. 115, Cham: Springer International Publishing, pp. 137–205, [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.1007/978-3-031-33859-5\_2](https://doi.org/10.1007%2F978-3-031-33859-5_2), [ISBN](https://en.wikipedia.org/wiki/ISBN_(identifier) "ISBN (identifier)") [978-3-031-33859-5](https://en.wikipedia.org/wiki/Special:BookSources/978-3-031-33859-5 "Special:BookSources/978-3-031-33859-5"), retrieved 2024-08-20`{{citation}}`: CS1 maint: work parameter with ISBN ([link](https://en.wikipedia.org/wiki/Category:CS1_maint:_work_parameter_with_ISBN "Category:CS1 maint: work parameter with ISBN"))
17. Soodak, Harry; Tiersten, Martin S. (1993-05-01). ["Wakes and waves in N dimensions"](https://pubs.aip.org/ajp/article/61/5/395/1054318/Wakes-and-waves-in-N-dimensions). *American Journal of Physics*. **61** (5): 395–401. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_(identifier) "Bibcode (identifier)"):[1993AmJPh..61..395S](https://ui.adsabs.harvard.edu/abs/1993AmJPh..61..395S). [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.1119/1.17230](https://doi.org/10.1119%2F1.17230). [ISSN](https://en.wikipedia.org/wiki/ISSN_(identifier) "ISSN (identifier)") [0002-9505](https://search.worldcat.org/issn/0002-9505).
18. Courant, Richard; Hilbert, David (2009). *Methods of mathematical physics. 2: Partial differential equations / by R. Courant* (2. repr ed.). Weinheim: Wiley-VCH. [ISBN](https://en.wikipedia.org/wiki/ISBN_(identifier) "ISBN (identifier)") [978-0-471-50439-9](https://en.wikipedia.org/wiki/Special:BookSources/978-0-471-50439-9 "Special:BookSources/978-0-471-50439-9").

## References

* Flint, H.T. (1929) "Wave Mechanics" Methuen & Co. Ltd. London.
* [Atiyah, M. F.](https://en.wikipedia.org/wiki/Michael_Atiyah "Michael Atiyah"); [Bott, R.](https://en.wikipedia.org/wiki/Raoul_Bott "Raoul Bott"); [Gårding, L.](https://en.wikipedia.org/wiki/Lars_G%C3%A5rding "Lars Gårding") (1970). "Lacunas for hyperbolic differential operators with constant coefficients I". *Acta Mathematica*. **124**: 109–189. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.1007/BF02394570](https://doi.org/10.1007%2FBF02394570). [ISSN](https://en.wikipedia.org/wiki/ISSN_(identifier) "ISSN (identifier)") [0001-5962](https://search.worldcat.org/issn/0001-5962).
* Atiyah, M. F.; Bott, R.; Gårding, L. (1973). "Lacunas for hyperbolic differential operators with constant coefficients. II". *Acta Mathematica*. **131**: 145–206. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.1007/BF02392039](https://doi.org/10.1007%2FBF02392039). [ISSN](https://en.wikipedia.org/wiki/ISSN_(identifier) "ISSN (identifier)") [0001-5962](https://search.worldcat.org/issn/0001-5962).
* [R. Courant](https://en.wikipedia.org/wiki/Richard_Courant "Richard Courant"), [D. Hilbert](https://en.wikipedia.org/wiki/David_Hilbert "David Hilbert"), *Methods of Mathematical Physics, vol II*. Interscience (Wiley) New York, 1962.
* [Evans, Lawrence C.](https://en.wikipedia.org/wiki/Lawrence_C._Evans "Lawrence C. Evans") (2010). *Partial Differential Equations*. Providence (R.I.): American Mathematical Soc. [ISBN](https://en.wikipedia.org/wiki/ISBN_(identifier) "ISBN (identifier)") [978-0-8218-4974-3](https://en.wikipedia.org/wiki/Special:BookSources/978-0-8218-4974-3 "Special:BookSources/978-0-8218-4974-3").
* "[Linear Wave Equations](http://eqworld.ipmnet.ru/en/solutions/lpde/wave-toc.pdf)", *EqWorld: The World of Mathematical Equations.*
* "[Nonlinear Wave Equations](http://eqworld.ipmnet.ru/en/solutions/npde/npde-toc2.pdf)", *EqWorld: The World of Mathematical Equations.*
* William C. Lane, "[MISN-0-201 The Wave Equation and Its Solutions](http://www.physnet.org/modules/pdf_modules/m201.pdf)", *[Project PHYSNET](http://www.physnet.org)*.

## External links

[![](//upload.wikimedia.org/wikipedia/en/thumb/4/4a/Commons-logo.svg/40px-Commons-logo.svg.png)](https://en.wikipedia.org/wiki/File:Commons-logo.svg)

Wikimedia Commons has media related to [Wave equation](https://commons.wikimedia.org/wiki/Category:Wave_equation "commons:Category:Wave equation").

* [Nonlinear Wave Equations](http://demonstrations.wolfram.com/NonlinearWaveEquations/) by [Stephen Wolfram](https://en.wikipedia.org/wiki/Stephen_Wolfram "Stephen Wolfram") and Rob Knapp, [Nonlinear Wave Equation Explorer](http://demonstrations.wolfram.com/NonlinearWaveEquationExplorer/) by [Wolfram Demonstrations Project](https://en.wikipedia.org/wiki/Wolfram_Demonstrations_Project "Wolfram Demonstrations Project").
* Mathematical aspects of wave equations are discussed on the [Dispersive PDE Wiki](http://tosio.math.toronto.edu/wiki/index.php/Main_Page) [Archived](https://web.archive.org/web/20070425131659/http://tosio.math.toronto.edu/wiki/index.php/Main_Page) 2007-04-25 at the [Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine "Wayback Machine").
* Graham W Griffiths and William E. Schiesser (2009). [Linear and nonlinear waves](http://www.scholarpedia.org/article/Linear_and_nonlinear_waves). [Scholarpedia](http://www.scholarpedia.org/), 4(7):4308. [doi:10.4249/scholarpedia.4308](https://dx.doi.org/10.4249/scholarpedia.4308)
