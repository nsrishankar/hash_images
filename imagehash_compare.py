# Compare a set of images to see similarity using hashing.
# Goal is to possibly check if the generator actually creates new images not in the training set for GANS
# Need to add upper thresholding to ignore small differences and recheck
import sys
# Housekeeping
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages') # Python3/ROS/Opencv clash
import cv2
import numpy as np
from matplotlib import pyplot as plt
# Hashing type: Difference hash
# First the image is converted to grayscale and downsized
# There are two hashes: row, column hashes:
#	a. For a row, Compare cells. If the next/right cell value is greater than the previous, the output is 1.
#	b. For a column, Compare cells. If the next/bottom cell value is greater than the previous, the output is 1.
# Concatenate the bit-values.

# Grayscale+Downsize
def image_manip(raw_image,downsample_size):
	raw_image=cv2.cvtColor(raw_image,cv2.COLOR_BGR2GRAY) # Grayscale
	raw_image=cv2.resize(raw_image,downsample_size,interpolation=cv2.INTER_NEAREST) # Downsample
	return raw_image.flatten()

# Difference hashfor row/column
def diff_hash(raw_image,downsample_sz):
	row=0
	column=0
	for y in range(downsample_sz):
		for x in range(downsample_sz):
			list_position=((downsample_sz+1)*y)+x
			
			try:
				row_bit=raw_image[list_position]<raw_image[list_position+1] # Bool check 1 or 0 for next row comparison
				column_bit=raw_image[list_position]<raw_image[list_position+downsample_sz+1] # Bool check 1 or 0 for next column comparison

				row=row << 1 | row_bit 
				
				column=column << 1 | column_bit
			except IndexError:
				continue
	# Return row, column hashes concatenated
	return row<<(downsample_sz**2)|column

# Find hamming distance between two hash values/ count different bits
def bit_hashcompare(im1_hash,im2_hash):
	bitwise_xor=bin(im1_hash^im2_hash)
	return bitwise_xor.count('1')

if __name__=="__main__":
	# Basic comparisons
	im1=cv2.imread("image_compare_images/im1.jpg")
	im2=cv2.imread("image_compare_images/im2.jpg")
	im3=cv2.imread("image_compare_images/im3.jpg")
	im4=cv2.imread("image_compare_images/im3.jpg")
	
	downsample_dim=(25,25)
	
	im1_hash=diff_hash(raw_image=image_manip(raw_image=im1,downsample_size=downsample_dim),downsample_sz=downsample_dim[0]-1)
	im2_hash=diff_hash(raw_image=image_manip(raw_image=im2,downsample_size=downsample_dim),downsample_sz=downsample_dim[0]-1)
	im3_hash=diff_hash(raw_image=image_manip(raw_image=im3,downsample_size=downsample_dim),downsample_sz=downsample_dim[0]-1)
	im4_hash=diff_hash(raw_image=image_manip(raw_image=im4,downsample_size=downsample_dim),downsample_sz=downsample_dim[0]-1)
	
	distance_im11=bit_hashcompare(im1_hash,im1_hash)
	distance_im12=bit_hashcompare(im1_hash,im2_hash)
	distance_im13=bit_hashcompare(im1_hash,im3_hash)
	distance_im14=bit_hashcompare(im1_hash,im4_hash)
	
	print("Same image distance ",distance_im11)
	print("Similar images (different color scale) flipped distance ", distance_im12)
	print("Same dog breed but different dogs distance ", distance_im13)
	print("Different dog breed distance ", distance_im14)