import numpy as np
import Nsound as ns
from extractWig import readWIG
import sys

total_time = 30		# the length of track in seconds
sample_rate = 5000	# the sample rate to use

min_freq = 20		# the minimum frequency to use
max_freq = 20000	# the maximum frequency to use

window_size = 1000	# the sequence window size to use in bp
sample_len = 0.5 	# the length of each sample (in sec)


def main() :

	# set up buffers to hold ouput
	buf1 = ns.Buffer()
	buf2 = ns.Buffer()
	buf3 = ns.Buffer()
	buf4 = ns.Buffer()

	# set up generators and instruments to create output
	gen = ns.Generator ( sample_rate )
	organ = ns.OrganPipe ( sample_rate )

	# override default sample rate
	ns.Wavefile.setDefaultSampleRate ( sample_rate )

	# the length of sequence to be used
	mySeqLength = int(window_size * ( total_time / sample_len ))

	myWigVector = readWIG ( sys.argv[1] )

	minWigVal = np.min ( myWigVector )
	maxWigVal = np.max ( myWigVector )

	# transform wig scores into frequencies, using a linear scale:
	freqVector1 = [ min_freq + ( ( (wigVal - minWigVal) / maxWigVal ) * max_freq)  for wigVal in myWigVector[ 0:mySeqLength] ]
	freqVector2 = [ min_freq + ( ( (wigVal - minWigVal) / maxWigVal ) * max_freq)  for wigVal in myWigVector[ mySeqLength:(2*mySeqLength)] ]
	freqVector3 = [ min_freq + ( ( (wigVal - minWigVal) / maxWigVal ) * max_freq)  for wigVal in myWigVector[ (2*mySeqLength):(3*mySeqLength)]]

	num_samples = int(total_time / sample_len)

	for sample_index in range ( num_samples ) :

		startIndex = sample_index * window_size
		endIndex = startIndex + window_size

		value1 = np.mean ( freqVector1[startIndex:endIndex] )
		value2 = np.mean ( freqVector2[startIndex:endIndex] )
		value3 = np.mean ( freqVector3[startIndex:endIndex] )

		buf1 << gen.drawSine ( sample_len, value1 )
		buf2 << gen.drawSine(sample_len, gen.drawLine(sample_len, 0.5*np.abs(value1-value2), 0.5*np.abs(value3-value2)))
		buf3 << organ.play ( sample_len, value3)

	# normalize each buffer
	buf1.normalize ()
	buf2.normalize ()
	buf3.normalize ()

	buf1.writeWavefile ( "output1.wav" )
	buf2.writeWavefile ( "output2.wav" )
	buf3.writeWavefile ( "output3.wav" )

	buf4 = (.5 * buf1) + buf3
	buf4.normalize()
	buf4.writeWavefile ( "output_1_3_combined.wav" )

	buf4 = (.8 * buf1) + buf2
	buf4.normalize()
	buf4.writeWavefile ( "output_1_2_combined.wav" )

	buf4 = (.3 * buf1) + (.6 * buf2) + buf3
	buf4.normalize()
	buf4.writeWavefile ( "output_1_2_3_combined.wav" )

if __name__ == "__main__" : main()