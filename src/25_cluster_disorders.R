abbrevs=as.matrix(read.table('abbrevs_numbered.txt',sep=";"))
disdata=as.matrix(read.table('disorder_voxel_data.txt',col.names=abbrevs))

d <- dist(t(disdata), method = "euclidean") # distance matrix
fit <- hclust(d, method="ward") 
plot(fit,hang=-1) # display dendogram

