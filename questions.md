
QUESTIONS
=========



building & running the algorithm
--------------------------------

### building the algorithm
First, the source code has to be compiled. For this, go to './fargo2d1d/src/'.

To clean everything up, do 	
  `make mrproper`

To build sequential, on 1 core, do
  `make BUILD=sequential` 

To build in parallel, on N cores, do
  `make BUILD=parallel`

### running the algorithm
To run sequential, go to './fargo2d1d/' and do
  `./fargo2D1D in/template.par`

To run in parallel, go to './fargo2d1d/' and do
  `mpirun -np #cores ./fargo2D1D -m in/template.par`

For the number of cores, just for an example, I have a resolution of
  * Nr = 802
  * Nphi = 1158
with a 2D grid ranging from 0.15 to 4.5, I run on 6 cores and it takes me
~2 weeks for the simulation to be done for
  * DT = 3.1415
  * Ntot = 10000
  * Nint = 200
(50 outputs with an output every 100 orbits)

### building the algorithm on the MPIA cluster

First, you have to connect to the bachelor-vis node of the MPIA cluster
  `ssh -Y mader@bachelor-vis`

Your personal simulation files are located attention
  `/mnt/beegfs/bachelor/groups/bitsch/users/mader/`

Building works almost exactly as is does locally, but first you have to
load openmpi by doing:
  `module load openmpi-4.0.1`

And then you can 
  `make mrproper`

and
  `make BUILD=parallel`

### running the algorithm on the MPIA cluster (submitting a simulation)
To submit a simulation to the SLURM queue, you have to login onto another node
  `ssh -Y mader@bachelor-login`
After setting up your personal simulation files, simulations can be submitted
by doing
  `sbatch submit.sh`
To check on the status of the queue, you can do
  `squeue`
or if you only want to see your own simulations
  `squeue -u mader`

More info:
On the USB stick, you also have a submit.sh file.
This is a submission file for the Bachelor.

The cluster uses SLURM. 			!! find out about SLURM
When you will log in, you will be given different links with
information about how it works. Take a look at this one in particular:

  * https://otrs.mpia.de/otrs/public.pl?Action=PublicFAQZoom;ItemID=197

where you also have a link toward some script examples.
In the one I gave you (which is the one I use), you just have to specify the
name of the job, the partition you want to run on (debug or four-wks),
your email address if you want to receive an email when the jobs
start/fail/complete and the number of cores you want to run the code on.

Just pay attention to write the same number in the --ntasks
and in the mpirun -np lines.





## MPIA cluster pw: 7UkFEY4RH_-w

