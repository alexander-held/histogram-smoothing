import ROOT


def print_bins(nbins, h):
    for i in range(nbins):
        print(h.GetBinContent(i + 1), end="  ")
    print()


nbins = 5
bin_content = [10, 12, 16, 13, 16]
h = ROOT.TH1F("h", "h", nbins, 0, 5)

for i in range(nbins):
    h.SetBinContent(i + 1, bin_content[i])

print_bins(nbins, h)
h.Smooth()
print_bins(nbins, h)
