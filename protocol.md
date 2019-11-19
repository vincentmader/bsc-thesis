
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
TODO:
  * make 1d plots for different resolutions, compare -> first plot in BA
    * should converge/stop changing for higher resolutions -> use 5c/rH ?
  * make plots for different values of e
    * accretion starts after ~500 orbits (when gap stops changing)
    * plot \dot{m} vs. e
  * compare gap for different values of e
    * compare e_gap with e_planet (they vary independently)
  * understand kelvin-helmholtz instabilities at gap edge
    -> different for different masses (-> gap widths) and viscosities


















