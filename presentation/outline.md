OUTLINE
=======
  * welcome to today's group meeting
    where I'm going to tell you about some of the things 
    that I did for my bachelor's thesis
  * we'll look into the accretion of gas onto planets on eccentric orbits
  * probably this group meeting will be a bit shorter than usual
    since I'm using this presentation also in my bachelor exam.
  * if it's ok with you, it would be awesome if you 
    saved your questions and feedback for the end,
    so the format is the same as during the bachelor exam

  * effect of eccentricity on the accretion rate
  * why is this interesting? 
    * many exoplanets have been discovered in recent years 
    * large set of planets allows statistical analysis
    * planet formation models can be tested against the discovered planet pop.
    * models are run in simulations -> population of planets is created
      -> called planet population synthesis
    * rely on simplified models 
    * accretion routine assumed to be not dependent on a planet's orbital eccentricity 
    * (e.g. Ida: hot Jupiters; )
    * using FARGO2D1D to construct a simplified disk model, 
      I'll show you that it could be advantageous to include the 
      eccentricity into the accretion routine in future studies

  * overview:
    * first I'll shortly talk about the numerical methods that I used
      and what resolution I chose
    * afterwards we'll look into the temporal evolution of a disk,
      formation of a gap,
      and how a planet's mass and orbital eccentricity
      influence the gap structure 
    * as well as the accretion rate of gas onto the planet
    * migration (TODO)
      (since all simulations up to this point will be with constant e and a)

  * FARGO2D1D algorithm 
    * is basically an n-body-solver, which uses a 
      5th order Runge-Kutta algorithm to determine the motion of the planet
      combined with a fluid dynamics subroutine for the gas
    * disk is modeled as an array of grid cells
      * rows correspond to radial position, 
        columns to angular/azimuthal position
      * the planet is placed in a 2D grid
        * disk is approximately axisymmetric,
          since influence of planet on disk due to 
          gravity weakens with distance,
        => surrounded by a 1D grid
        * this way, we can get accurate results for both the regions around 
          the planet as well as the overall disk structure with relatively
          low computation times
      * there is only one planet in the disk at any given time
      * planet is positioned at r=1 in the beginning 
      * planet is not initialized in a single timestep: -> tapering
      * accretion wait
      * migration is turned off, semimajor axis stays constant
      * aspect ratio is set to a constant value of 0.05
      * gas density follows a simple power law 
      * viscosity alpha parameter is set to 10^-2
      -> did also look at different viscosities,
         & different H/R, sigma slope
    * planet
      * is placed at r=1 code units, which corresponds to the semimajor axis 
        of Jupiter (approximately 5.2 AU)
      * accretion routine after each time step
        * calculate accretion rate using the principle of Willy Kley (1999)
        * calculate it with Machida's principle (2010)
        * take the smaller of the two
        * remove the gas from the disk via Kley's principle
    * resolution 
      * simulate disk over 500 orbits, no accretion 
      * do this for different numbers of grid cells per Hill radius 
        * 2.5 -> artifacts near the center
          * the color scale shows the logarithm of the surface density
        * 5 -> artifacts disappear
        * 10 -> which is of course beautiful, but computationally constraining
          (factor 8 in integration time for each resolution doubling)
      * overall structure is very similar
      * chose 5 cells per Hill radius,
        seems to be a good trade-off between integration time and accuracy

  * polar plot of the simulated disk
    showing the surface density over time
    * for eccentricity zero (1 Jupiter mass)
      * the planet forms a gap in the disk 
      * planet exchanges angular momentum with the gas in the disk 
        via gravity
        * it takes momentum from gas particles that are further inwards 
        * and gives momentum to those that are further outwards
      * leads to depletion of gas near the planet's orbit
    * for high eccentricity (TODO: which eccentricity?)
  * gap profile for different masses over time 
    * most massive planets form the deepest and widest gaps
    * we can take a look at the mass of the planets after these 2500 orbits
    * local density maximum inside the planet's Hill sphere
  * gap profile for different eccentricies over time 
    * gas density is averaged over the azimuthal angle phi
  * mass accretion over time for different eccentricies

  * migration
    * Kozai: eccentricity fluctuates between disk and planet
    * type I: planet can't open gap 
    * type II: planet can open gap

  * gap eccentricity vs planet eccentricity
    * heavy planet can excite eccentricity (center of mass shifts)
    * eccentric planets can also excite the disk's eccentricity 
      -> rückkopplung
  
  * why is this interesting?
    * studies of n-body-simulations often do not account for the eccentricity 
      in the formulation of the accretion routine

  * references

It occurs when the natural frequency of the radial (i.e. in and out in the 
direction of the centre) component of motion of a star in its orbit is the 
same as the frequency of passage of the star through the maxima of the 
gravitational potential associated with the spiral pattern. If the star is 
moving around the centre faster than, and overtakes, the spiral pattern, 
then an inner Lindblad resonance occurs; if the pattern is moving faster than 
the star around the centre, then an outer Lindblad resonance occurs. At an 
inner resonance, energy is fed into the orbits of the stars from the 
spiral pattern, and vice versa at an outer resonance.
