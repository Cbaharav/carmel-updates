## NOTES: 

  If you full fill a task, add [x], i..e,
  
  [x] bla

## TEST:

    [x] Create a TESTS folder.

      [] Add scripts that shows the tests.
      
      [] Consider to add examples that uses bifrost_fft.py as well as 
      	 the test that you are doing for the various waves where the 
	 result must be 1 or 0. 

## Style:

    [] Make sure that you fullfil pep8 (I dobout that lines 61, 133, 134, 141, 163
       are within pep8 rules). 
    

## Documentation:

    [] Fill README.md with information related to this library.

    [] Consider use github wiki for a more complete documentation
      (at least for the bifrost.md). This can be found here
      (https://github.com/Cbaharav/carmel-updates/wiki). This will allow
      various sections. You may want to add some of information in the
      poster you did for the AGU meeting. 

        # BIFROST.md:

          [] Add description of other flags in python setup.py install, e.g., --developer ...

          [] BifrostData Objects -> BifrostData class, change
              in the document each time that you mention BifrostData Objects it
              should be BifrostData class.

          [] Consider to use (https://www.lmsal.com/iris_science/doc?cmd=dcur&proj_num=IS0124&file_type=pdf)
             for guidance of what could be included so you
             know which other information you could add.

        # TheInternFiles.md: (I also took the liberty to comment on this ;-D)

          [] typo: houses -> uses

          [] stuff: be more specific if you can.

          [] setenv HELITA "~/helita-master/helita" is not needed

          [] You may want to list other servers: Kyoto, Kona, Yale, Karmeliet,
               Thor 

## New code:

    [x] Layout looks nice!

    [] Reduce some empty space (leave at most one empty line). In addition, dont leave
       the empty line between the description below each function.

    [] Add a very short # comment for relevant variables in the code, e.g.,
       self.preCompFunc, self.preCompShape, self.transformed_dev, self.api,
       self.thr, self.found

    [] Is there any special reason fftHelper, threadIt, task, are functions of another
       function?. If possible, take it out from get_fft as independent functions.
       They could be out of the class, towards the end of the file if you like.
       It would be nice if you make a more meaning full name of all these three functions.

    [] use_gpu rewrites found. I though found is a flag if the machina has GPUs and CUDA. 
       Suggestion: 

	    def run_gpu(self, choice=True):
	    	'''
		activates the module that uses CUDA
		'''
		self.use_gpu = choice

	If you do so, make sure that you change line 117 accordingly. 

     [] I see several prints. This might be useful but sometimes is anyoing to see
     	every time these prints. Alternative. Add a flag in __init__ (verbose) if this one is 
	True, then does the prints, i.e., 

	      if verbose: 
	      	 print(... 
	      

## Bifrost.py

    [] Did you merged your bifrost.py with the one in Helita? If so, delete the one here. 

    [] You may want to move bifrostdoc.md into my helita fork. Or even better, in the helita wiki. 