## NOTES: 

  If you full fill a task, add [x], i..e,
  
  [x] bla

## TEST:

    [x] Create a TESTS folder.

      [partial x] Add scripts that shows the tests.
      		- one script and resulting plot added
      
      [x] Consider to add examples that uses bifrost_fft.py as well as 
      	 the test that you are doing for the various waves where the 
	 result must be 1 or 0. 

      [partial x] Add real test, i.e., from one simulation that shows a map of height, i.e., z axis vs 
      frequency where you do average of the FFT in x and y. This might be included as a new
      function (without the plot.imshow()) in the code. 

## Style:


## Documentation:

    [] Fill README.md with information related to this library.

    [x] Consider use github wiki for a more complete documentation
      (at least for the bifrost.md). This can be found here
      (https://github.com/Cbaharav/carmel-updates/wiki). This will allow
      various sections. You may want to add some of information in the
      poster you did for the AGU meeting. 

        #  wiki 
	  [x] Great first step! you are fast... 
	      
	      [] Give me a tour how to do git-wiki ;=D

          [] Consider to use (https://www.lmsal.com/iris_science/doc?cmd=dcur&proj_num=IS0124&file_type=pdf)
             for guidance of what could be included so you
             know which other information you could add.
	     	 [] Add new page about bifrost.py, i.e., things that one could do with import helita.sim.bifrost as br. 

## New code:

    [x] Layout looks nice!
    
    [] I think you forgot to commit your changes... I dont see a new update of the code. So, I can't test this...

    [x] Reduce some empty space (leave at most one empty line). In addition, dont leave
       the empty line between the description below each function. **reduced as much as possible, some required by pep8**

       	   [autpep8 keeps on inserting double blank lines when I delete this one] There is still one case with double blank lines (line 21). 
	   JMS Interesting. ...

    [x] Add a definition of the following functions: singleCudaRun, linearTimeInterp, singleRun, threadTask

    [x] test should be in test file not here. 

       [x] I don't think you need test flag in get_fft since dd.preTransform and freq are already define. right?
       		[] note to self: issue- without test flag, get_fft doesn't change preTransform if running on the same FFTData object (regardless of whether snaps, slices, or quantity have changed)
       	  

     [x] self.freq should not be in linearTimeInterp instead in get_fft
     
          [x] I think it would be nice to have evenDt and evenTimes in self. Also important if 
	  you move self.freq in get_fft. 
	  
     [] Add spatial power spectrum functions in a similar way as you did for the time axis. 
     Please, come over my office I'll explain  in detail

## Bifrost.py

    [x] Did you merged your bifrost.py with the one in Helita? If so, delete the one here. 

    [] You may want to move bifrostdoc.md into my helita fork. Or even better, in the helita wiki. 
