import numpy as np

def tester(test_this, true_disp):
	true_disp = true_disp/8
	test = (test_this - true_disp).reshape(-1)
	mde = test.mean()
	testsq = ((test_this - true_disp) ** 2).reshape(-1)
	mse = testsq.mean()

	print("Mean disparity error:", mde, "\n", "Mean sqared error:", mse)
	stdev = np.std(test)

	print("Standard deviation of disparity error:", stdev)
	i=0

	for x in test:
		if abs(x)>=3:
			i += 1
	p = i/len(test)

	print("Number and fraction of large errors (error ≥ 3 pixels):", i, p)
	return [mde, mse, stdev, i, p]