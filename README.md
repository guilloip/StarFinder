# StarFinder

Jul 3rth 2021:

This program was created for a challenge in Facebook's Python Programmers [beginners] group.  Find the 4 brigthest stars in a picture

The picture is field.jpg

I used CV2 library for Python (of openCV), for image processing, and pyplot for plotting histograms.

Even though CV2 and numpy has its histograms function, I did mine by myself.

This software must not be taken as a profesional tool, it is only for learning python and OpenCV.  Better software and criteria could be found to achieve this task

General Steps:

1) Transform RGB image to a Gray scale image using CV functions.
2) Do a binary threshold to the gray scale image to make easier find brighter ones
    
    Only 2 levels: 0 (LOW) and 255(HI).  The threshold limit was 220 
3) I considered a star as the set of HI pixels whose distance are lower than a certain value R (from now, the radious of the star).
   
   For each pixel in the thresholded image, I try to find if there were an already set of pixels (star), that were near enogh to consider that pixel part of that star. If it were the case, I just added that pixel to that star (set of pixels), else, I created a new star with that pixel.
   
   Later, I calculated the position X,Y of each found star as the mean values of all pixel's coordinates in that set.
4) For each found star, I determined some kind of "bright" based in the sum of the values of the pixels in the gray scale image within a rectangle of 2Rx2R centered in its coordinates.
   
   In order to be fare with those stars that could be too near to the image's border (that might have less pixels), I divided the sum in the number of pixels considerated for each case. 
   
   So Brightness = sum val(img[i,j])/n for (i,j) in (x-R to x+R, y-R to y+R) that were inside the image, and n is the total of pixels inside de image. 
   
5) finally, to sort them, I created a dictionary {star:bightness} and sorted it by values in reverse order, keeping the 4 best.

Extra Files:

field.jpg

gra_field.png

histrogram(gray)

threshold_fiel.png

histogram(thresh..)

last output screen (maybe in JPG or TXT)


