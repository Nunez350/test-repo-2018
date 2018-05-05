#Tianai
from ROOT import TH1D, gRandom

h1 = TH1D("hist","histogram",100,-5,5)
for i in xrange(10000):
	hist = gRandom.Gaus()
	h1.Fill(hist)
h1.Draw()
