import os
from argparse import ArgumentParser

#parser = ArgumentParser()
#arser.add_argument("--include", help="Path to training sample", default=)
#args=parser.parse_args()
#print(args.include)


names = ["QCD", "Glu"]

dcap = "dcap://grid-dcap-extern.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/user/anovak"
srm = "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/anovak"
dirs = os.popen("gfal-ls "+srm).read().split("\n")

print "Processsing directories starting with: ", names
print "======================================="
all_files = []
for i, d in enumerate(dirs):
	dir_files = []
	if d[0:3] not in names: continue
	print d
	sd = os.popen("gfal-ls "+srm+"/"+d).read().replace("\n", "")
	sd2 = os.popen("gfal-ls "+srm+"/"+d+"/"+sd).read().replace("\n", "")
	sd3 = os.popen("gfal-ls "+srm+"/"+d+"/"+sd+"/"+sd2).read().replace("\n", "")
	files = os.popen("gfal-ls "+srm+"/"+d+"/"+sd+"/"+sd2+"/"+sd3).read().split("\n")

	path = dcap+"/"+d+"/"+sd+"/"+sd2+"/"+sd3
	for f in files:
		if not f.endswith("root"): continue
		all_files.append(path+"/"+f)
		dir_files.append(path+"/"+f)


	with open("files_lists/"+d+".txt", 'w') as f:
	        f.write('\n'.join(dir_files))
        #print 'Write training/validation files to %s' % os.path.join(inputdir, 'train_val_samples.txt')