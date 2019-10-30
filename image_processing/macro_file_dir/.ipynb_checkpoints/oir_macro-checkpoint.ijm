input="input_data/";
filename="181019_raft1_A01_G001_0001.oir"
run("Bio-Formats Importer", "open=["+ input + filename +"] view=Hyperstack split_channels stack_order=XYCZT");
selectWindow("181019_raft1_A01_G001_0001.oir - C=0");
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", "tif_files/MAX_181019_raft1_A01_G001_0001.oir - C=0.tif");
close();
close();
selectWindow("181019_raft1_A01_G001_0001.oir - C=1");
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", "tif_files/MAX_181019_raft1_A01_G001_0001.oir - C=1.tif");
close();
close();
selectWindow("181019_raft1_A01_G001_0001.oir - C=2");
run("Z Project...", "projection=[Max Intensity]");
saveAs("Tiff", "tif_files/MAX_181019_raft1_A01_G001_0001.oir - C=2.tif");
close();
close();
