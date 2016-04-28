import pylab
from pylab import plot, show

num_list = [1000, 2000, 3000, 4000]
efficiency_base = [3.9, 20.47, 46.8, 84.74]
efficiency_k_16 = [0.71, 3.409, 7.33, 13.16]
efficiency_k_32 = [1.59, 6.05, 12.97, 22.84]
efficiency_k_64 = [3.08, 10.38, 23.74, 40.99]
efficiency_k_128 = [5.68, 17.07, 46.57, 82.28]


pylab.plot(num_list, efficiency_base, linewidth=2)
pylab.plot(num_list, efficiency_k_16, linewidth=2)
pylab.plot(num_list, efficiency_k_32, linewidth=2)
pylab.plot(num_list, efficiency_k_64, linewidth=2)
pylab.plot(num_list, efficiency_k_128, linewidth=2)

pylab.legend(["True baseline", "16-minhash", "32-minhash", "64-minhash", "128-minhash"], loc="best")
pylab.xlabel("Number of training data files")
pylab.ylabel("Time (s)")
pylab.grid()
pylab.title("User-based Scalability.")
pylab.show()

k = [16, 32, 64, 128]
efficacy_file_1 = [0.016527185384238089, 0.0067315254570407346, 0.0045616141863935537, 0.0022533151795511518]
efficacy_file_2 = [0.029201436492323523, 0.013940626389981406, 0.0054920859413397794, 0.0027376600417975457]
efficacy_file_3 = [0.029157404321428743, 0.013102836341813445, 0.0087439010064185151, 0.0039411831223372081]
efficacy_file_4 = [0.038989833734401971, 0.019994200726294879, 0.0094844224241476538, 0.0060008176411226058]

pylab.plot(k, efficacy_file_1, linewidth=2)
pylab.plot(k, efficacy_file_2, linewidth=2)
pylab.plot(k, efficacy_file_3, linewidth=2)
pylab.plot(k, efficacy_file_4, linewidth=2)

pylab.legend(["1000 records", "2000 records", "3000 records", "4000 records"], loc="best")
pylab.xlabel("Number of Hash functions (k)")
pylab.ylabel("Mean-squared error")
pylab.grid()
pylab.title("Efficacy.")
pylab.show()


support = [0.025, 0.03, 0.04, 0.05]
num_rules = [346, 100, 28, 12]
plot(support, num_rules, linewidth=2)
pylab.xlabel("Value of support")
pylab.ylabel("Number of rules found")
pylab.grid()
pylab.title("Impact of support (1000 transactions).")
pylab.show()

num_list = [1000, 2000, 3000, 4000]
t = [1.52, 4.38, 9.66, 16.99]
pylab.plot(num_list, t, linewidth=2)
pylab.xlabel("Number of training data files")
pylab.ylabel("Time (s)")
pylab.grid()
pylab.title("Item-based Scalability.")  # partially because num of rules also decrease
pylab.show()
