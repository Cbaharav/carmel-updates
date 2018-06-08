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

      [x] Add real test, i.e., from one simulation that shows a map of height, i.e., z axis vs 
      frequency where you do average of the FFT in x and y. This might be included as a new
      function (without the plot.imshow()) in the code.

      [x] Both test looks good, except that I would be nice if you add some comments 
      of what is doing the different code lines. 

      [] Question: Could you tell me what do you see in the simulation case?
      

## Style:


## Documentation:

    [] Fill README.md with information related to this library.

        #  wiki 
	  [x] Great first step! you are fast... 
	      
	      [] Give me a tour how to do git-wiki ;=D

          [] Consider to use (https://www.lmsal.com/iris_science/doc?cmd=dcur&proj_num=IS0124&file_type=pdf)
             for guidance of what could be included so you
             know which other information you could add.
	     	 [] Add new page about bifrost.py, i.e., things that one could do with import helita.sim.bifrost as br. 

     # READOCS: 
       - Good job! Impressive that you did everything from scratch. I may need some guidence. 
       I also created my account. You can include me (same as my github jumasy). 
       Defenetily I'll use this for the next intern this summer.

       [x] Right now you did most of the documentation, I hope Tiago (and of course I) will complete/add information there. 
       so you could put as a list of contributors: i.e., for now By Carmel Baharav, Juan Martinez-Sykora & Tiago M. D. Pereira

       [x] Could you add a note that most of the most updated versions (and the functionality less reliable) done in bifrost.py, ebysus.py and 
       and bifrost related are in https://github.com/jumasy/helita.git fork. 

       [x] Add that if iix, iiy or iiz is not specified it will read all the numerical domain along the x, y and/or z axis, respectively. 
       
       [x] If you know how to get some keys, i.e., time, axis information, dz, dx, dy among others. Add those in the Getting Variables & Quantities

       [x] Add short list of variable available (computed and non computed). 

       About bq_t5_tool
       
       [x] Also useful for ebysus simulations. 

       [x] The Bifrost code is not publicly available yet, consequently the bq_t5_tool is not availeble neither. Make this clear. 

       [x] I could not play the movie...  
 		- should be fixed now (hopefully)
		- let me know if there's any specific variable/setup (like data min/max instead of image min/max) that I should use for the movie instead of the current one

## New code:

    [x] Layout looks nice!
    
    [] I think you forgot to commit your changes... I dont see a new update of the code. So, I can't test this...

     [] Add spatial power spectrum functions in a similar way as you did for the time axis. 
     Please, come over my office I'll explain  in detail

     	     [] Add fft for each axis

     	     [] Add fft for cylindrical and sperical axis and integrated in angle. 

	     [] Add a function that goes through time (for the space case) and in height (for the 
	     temporal one) doing the average of the ffts. 
    	     
## Bifrost.py

    [] You may want to move bifrostdoc.md into my helita fork. Or even better, in the helita wiki. 
