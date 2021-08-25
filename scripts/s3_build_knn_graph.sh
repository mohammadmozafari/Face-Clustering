python_file='./src/s3_build_knn_graph.py'

feat_path1='./data/IJB-B/512.fea.npy'
feat_path2='./data/YoutubeFaces-Subset-Results/features_1_18796_.npy'

k1=50
k2=500

alg1='brute'
alg2='kd_tree'
alg3='ball_tree'

out_path1='./data/IJB-B/knn.npy'
out_path2='./data/YoutubeFaces-Subset-Results/knn_bt.npy'

python $python_file --feat_path $feat_path2 --k $k2 --alg $alg3 --out_path $out_path2