import random
import numpy
import matplotlib.pyplot as plt

def algorithm():

	not_all_in_room = True

	counter = 0
	prisoners = []

	for i in range(100):
		prisoners.append(0)



	while not_all_in_room:

		counter += 1
		prisoner_index = random.randint(0,99)

		prisoners[prisoner_index] += 1

		not_all_in_room = False
		for prisoner in prisoners:
			if prisoner == 0:
				not_all_in_room = True


	return counter

if __name__ == '__main__':

	largest_count = None

	counts = []

	for i in range(10000):
		count = algorithm()
		if largest_count is None:
			largest_count = count
		elif count > largest_count:
			largest_count = count

		counts.append(count)

	print(largest_count)

	#print(counts)

	# Choose how many bins you want here
	num_bins = 100

	# Use the histogram function to bin the data
	#counts, bin_edges = np.histogram(counts, bins=num_bins, normed=True)

	# Now find the cdf
	#cdf = np.cumsum(counts)

	values, bins, _ = plt.hist(counts, bins=num_bins)
	area = sum(numpy.diff(bins)*values)

	print(bins)

	#sub_area = sum(numpy.diff(bins[0:90])*values)

	#percentage = sub_area / area

	#print(bins[90])
	#print(area)
	#print(sub_area)
	#print(percentage)

	# And finally plot the cdf
	# plt.plot(bin_edges[1:], cdf)




	plt.show()
