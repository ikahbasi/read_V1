# read_V1
This is simple python code to read ascii acceleration data (V1 file) in seismology 

This code is too simple :) but work enough for me

I just try to make first work in github

    This code has 3 simple function for read,write and plot V1-file in v1.py
    (file.V1 is strong motion or acceleration data of earthquake)
    
        1)read_v1
            >>> path = 'path-of-file/namefile'
            
            # obspy_out: defult to False
            >>> asciis = read_v1(path)
            
            # if you have obspy python package you can
            >>> asciis, st = read_v1(path, obspy_out=True)
            
            # asciis has all 3 component
            # asciis = [[comp1, time1, acc1],[comp2, time2, acc2],[comp3, time3, acc3]]
        
        2)v1_write_2column_file
            >>> v1_write_2column_file(asciis)
            # write 3 files with name of component in current directory 
    
        3)plot_v1
            >>> plot_v1(asciis)
            # save image 'output.png' in current directory
            
        Please send me any file.V1 that makes error to improve improve efficiency.
