
DAILY PROTOCOL
==============
Arising questions are marked with a !Q! tag to make them easily searchable.

Mon, 2019-11-04, DAY 001
------------------------
  * come to MPIA at 09:30, meet with Dr. Bitsch
  * get electronic key & cafeteria card
  * bureaucracy: contract, insurance, cv, laufzettel
  * meet Camille, PhD student of Dr. Bitsch
  * get USB stick from Camille: FARGO2D1D software, information about it
  * play around with software
  * meet with Camille: she explained FARGO, setup parameters, disk physics
  * leave at 18:30

Tue, 2019-11-05, DAY 002
------------------------
  * come to MPIA at 09:30, play around with simulation data
  * meet with Camille: setup of VPN, connection to cluster, slurm
  * run low resolution simulations: one with eccentricity e=0, one with e=.1
  * setup plotting method: once in rectangular grid, once in polar coords
  * leave at 17:30

Wed, 2019-11-06, DAY 003
------------------------
  * come to MPIA at 09:30
  * setup plotting of 1D data, all 3 plots are now displayed together in one png
  * run more low res simulations: e=.05, e=.25, e=.5
  * calculate Hill radius for current setup: M=1, m=6e-5, a=1
    =>  rH = 0.027
  * Hill radius is supposed to correspond to 5 numerical cells
    =>  1 cell = 0.0054
  * planet sits at a = 1
    =>  184 cells between star and planet
  * with Rmin = 0. and Rmax = 3. this leads to Nrad = 551
  * to keep a ratio Nsec/Nrad = 2, I choose Nsec = 1102
  * multiple simulations are started, with e=[0, 0.05, 0.1, 0.15, 0.2, 0.25]
  * leave at 16:30
!Q!
  Hill radius is calculated for a specific semi-major axis a.
  How does this work out if the planet's orbit is eccentric and a != const. ?
  => a = const. even for e != 0, I got that wrong
  => rH != const. only if 
    * mass changes: if it gets bigger, rH gets bigger => no problem
    * migration turned on: can be a problem, might need to look into that

Thu, 2019-11-07, DAY 004
------------------------
  * come to MPIA at 09:30
  * start writing method to calculate planet mass after each time step
  * first idea: mass in Hill sphere
  * second idea: mass in cell occupied by planet
  * leads to kind of weird results, mass is decreasing with time
  * I need to find out whether I can get the planet mass directly from outfiles
  * talk to Bertram after lunch
  * Betriebsbeirat colloquium
!Q! 
  What is the best way to get the planet's mass at a specific iteration step ?
  I tried getting the mass in cell occupied by planet => decreases with time (?)
  => can't get it from cell, cell is much much bigger than planet
    * smoothing of potential, no 1/r, but 1/(r+ε), I should look that up
  => there are two parts of the algorithm:
    * n-body-solver for planet and star
    * fluid dynamics for gas in potential of star with disturbance of planet
    * accretion rate is determined, then mass is taken from Hill sphere & added
  => mass can be found in the output file 'planet1.dat', column idx 5
!Q!
  What do I need to do about the Projektpraktikum-Anmeldung ?
  => Bertram does not know, but will sign the form if I get it (google, uni)
!Q!
  How do I compare accretion rates for different eccentricities?
  * do simulations for different values of e
  * then compare mass at a specific time -> see planet1.dat file
TODO:
  * (1) find out best value for Hill radius, for this:
    * simulation of planet with ~1 MJ without accretion
    * do this for [2.5, 5, 10] cells per Hill radius
  * (2) then look at disk evolution for different masses, still no accretion
    * choose r = 1 comp. unit (i.e. 5.2 AU)
    * masses [1, 3, 5, (10)] MJ
    * a few hundred orbits need until equilibrium => simulate 2000-3000 orbits
    * output every 50 orbits
  * do this for e=0 and e=0.2

Fri, 2019-11-08, DAY 005
------------------------
  * feeling sick, not going to the MPIA today
  * start simulations from home: (1) from TODO above

Mon, 2019-11-11, DAY 006
------------------------
  * not going to MPIA, need to work on FP today
  * I started simulations for (2) from TODO above the day before yesterday
  * fix 2D polar coordinates plot: had to change from deg to rad
  * continue working on plotting, modularize into multiple functions

Tue, 2019-11-12, DAY 007
------------------------
  * only shortly went to MPIA, still have to do a lot of FP today

Wed, 2019-11-13, DAY 008
------------------------
  * FP Nachbesprechung for Optics

Thu, 2019-11-14, DAY 009
------------------------
  * write Python function: plot \dot{m} as function of eccentricity 
  * talk to Bertram
    * Planet sollte an einem Ort stehen bleiben
      warum bewegt er sich? Bild alle DT* 2\pi?
    * Einheiten von σ? Msun / comp.unit^2 ?
    * habe noch mehr Simulationen am Laufen
      -> andere Werte von e
      -> plot von \dot{m}=f(e)
  * PSF group meeting: how to work with ALMA data, presentation by Nicolas
  * Abgabe des Laufzettels im Sekretariat
  * fix 1d plot (use ascii files, look whether that resolves the issue)

Fri, 2019-11-15, DAY 010
------------------------
  * not going to MPIA today, FP Nachbesprechung Elektronik & Röntgen-Laue

Mon, 2019-11-18, DAY 011
------------------------
  * try simulating 2d with rotating frame, to keep planet fixed
    -> use frame parameter C (corotating)

Tue, 2019-11-19, DAY 012
------------------------
  * make 1d plots for different resolutions
  * update structure of latex project

Wed, 2019-11-20, Day 013
------------------------
  * write theory part in latex
  * general structure of documents

Thu, 2019-11-21, Day 014
------------------------
  * simulation for 7.5 cells per rH finished, include that in plot
  * group meeting, presentation by Camille on gas accretion onto planets

Fri, 2019-11-22, Day 015
------------------------
  * meet with Bertram
    * which nr of cells per rH shall I take? (-> one of the first plots in BA)
    -> 5 should be ok, only differs significantly for very low r, gap converges
    * how shall I determine eccentricities of gap to compare with e of planet?
    -> pressure gradient peaks, look into slide 13 of Camille's GM presentation
    -> determine gap eccentricity as function of planet eccentricity and mass
    -> also determine gap depth
    * which parameters shall in total be varied for BA? (in order of significance)
    -> e, m0, α, H/R, Machida, density profile (-> look at Crida 2006 paper)
    -> for this, do σ/σunp (unperturbed w/o planet, same Nrad, Nsec small, e.g. 2)
    -> also do a plot comparing σ and σunp
    * is it normal that my simulations don't save files every 50 orbits?
    -> nope, need to look into that
    * how will planet with e.g. a=1 and e=0.2 move?
    -> 0.8 <= r <= 1.2

Mon, 2019-11-25, Day 16
-----------------------
  * fix 1D plot in collage, did not plot r against Σ, but ridx against Σ
  * simulations with frame rotation option C (corotating) still not 
    giving outputs other than for 0th timestep, which is strange.
    I restarted them after talking to Bertram, but still they don't give
    outputs... So I start all of them again, this time with frame rotation 
    option F (fixed angular velocity for rotation, set to 1)

Tue, 2019-11-26, Day 017
------------------------
  * continue a little with theory

Wed, 2019-11-27, Day 018
------------------------
  * cluster chrashed -> restart simulations with fixed frame angular velocity

Thu, 2019-11-28, Day 019
------------------------
  * continue with analysis of gap eccentricities

Fri, 2019-11-29, Day 020
------------------------
  * some simulations for fixed frame rotation are finished 
  -> a bit weird, planet is still moving in graph even for e=0

Mon, 2019-12-02, Day 021
------------------------
  * some simulations on cluster are still not producing results, restarting:
    * 0mj      -> restarting once with planet mass 0, once without planet at all
    * 1mj_e.25
    * 1mj_e.30
    * 20mj_e.2
    * 50mj_e.2 
  * make plot for accretion vs eccentricity, seems to be ~e^2 behavior
  * make plots for accretion vs time, seems to be ~e^.5 behavior

Tue, 2019-12-03, Day 022
------------------------
  * make plots for Hill sphere in grid

Wed, 2019-12-04, Day 023
------------------------
  * minor changes 

Thu, 2019-12-05, Day 024
------------------------
  * compare mass accretion for different planet eccentricities
    * plot mass increase m/m0 vs. eccentricity at fixed time (after 2500 orbits)
    * do the same for accretion rate dm/dt vs. eccentricity
  * meet with Bertram
  * group meeting

Fri, 2019-12-06, Day 025
------------------------
  * FP

Mon, 2019-12-09, Day 026
------------------------
  * FP

Tue, 2019-12-10, Day 027
------------------------
  * FP

Wed, 2019-12-11, Day 028
------------------------
  * start rewriting project
    -> config files, simulation parameters, ...

Thu, 2019-12-12, Day 029
------------------------
  * group meeting
  * continue restructuring project

Fri, 2019-12-13, Day 030
------------------------
  * fixed bug where planet was not drawn at radial distance 1
    (reason for bug: wrong radial boundaries returned from sim_params function)
  * implemented drawing of gap boundaries in 2D gas densities plot
    * various values of distances can be given
    * this distance is used to search in the vicinity of the planet for
      maxima of gas pressure, which can be calculated from gas density.
    * pressure maxima correspond to edges of disk
    -> disk width, depth and eccentricity can be calculated later on
  * fixed bug where planet was not shown in the center of the plot
    this bug was due to the fact that
      arctan(φ_1) = arctan(φ_2)
    for angles φ_1 and φ_2 in opposing quadrants, it was fixed by comparing the 
    sign of the y-position with the value of φ and shifting by 2π when needed.

Mon, 2019-12-16, Day 031
------------------------
  * rewrite large portions of project
    -> more modular, separation into packages
    -> more reusable
    -> better documentation (comments & doc strings)

Tue, 2019-12-17, Day 032
------------------------
  * plot accretion vs viscosity parameter alpha
  * talk to Bertram
    * changes since last time:
      * project structure, more modular, better documentation
      * gap drawn for search distances of 5 and 10 rH
      * can now track planet location
      -> planet centered in cartesian plots
      * accretion rate plotted against time, mass, eccentricity, viscosity
  * run simulations for 10000 orbits (e=0,0.1,0.2,0.3; m=1,2,5 MJ)

Wed, 2019-12-18, Day 033
------------------------

Thu, 2019-12-19, Day 034
------------------------

Fri, 2019-12-20, Day 035
------------------------

Thu, 2020-01-18, Day 036
------------------------
  * stuff that I did during the holidays:
    * plot 1D gas density vs. radial distance after tapering has finished
    * write function to calculate gap eccentricity from gap boundaries











QUESTIONS

  * why does fixed frame rotation Ω=1 not lead to static images in φ-direction
  * what exactly does DT do? currently using DT=2π
  * why does velocity increase after 10 images? (at the same time as acc. starts)
    -> planet moves inwards

TODO

  * in total vary e, m0, α, H/R, Machida factor, density profile
    * for density profile look into paper Crida 2006

    * e (initial eccentricity of planet orbit)
      * (DONE) plot final planet mass vs. eccentricity
        * do this for e >= 0.3
      * (?) plot accretion rate vs. eccentricity
        * fix y-scale

    * m0 (initial planet mass)
      * plot final planet mass vs. initial planet mass
        * fix bug where only two sim_ids are displayed
        * fix y-scale
      * plot accretion rate vs. initial planet mass
        * fix y-scale

    * α (disk gas viscosity)
      * (DONE) plot final planet mass vs. gas viscosity
        * do this for different eccentricities and different masses? 
        -> did crash for e != 0

    * H/R (disk aspect ratio)

    * Machida factor

    * initial density profile

    * planet core mass
      * earlier sims were run with 33% mass in core, 10-15% is more realistic
      -> show that it does not make a big difference

  * compare σ with σunp (unperturbed)
    * run simulation without planet, why not working atm?
    * do all analysis with σ/σunp

  * compare gap for different values of e and m0
    * calculate gap eccentricity
      * determine gap edges from logarithmic pressure gradient
      * look for other possibilities (W. Kley und Daniel Thun, Numerical ...)
      * CFL condition for gap formation
    * calculate gap depth/width
    * plot both as a function of planet eccentricity and initial mass
    * look for gap in different ranges around planet, e.g. 5 & 10 rH

  * for dm/dt vs e and m/m0 vs t: const. multiplicative factor between curves?
  * look at radial center of mass, evolution, moves outwards ?

  * (DONE) make python config/info file, where parameters can be imported from

  * plots: make consistent
    * same number of digits after comma for m0 and e
    * axis ticks in scientific mode

  * what is going on in the center of the grid?

MAYBE:

  * compare structure of 2D Σ for different values of eccentricity
    * plot 2D data
    * compare gap profile & eccentricity (see above)
    * compare spiral arms (?)
    * look into turbulences at gap edge (Kelvin-Helmholtz instabilities)
      * these vary with planet mass (-> gap width) and disk viscosity

